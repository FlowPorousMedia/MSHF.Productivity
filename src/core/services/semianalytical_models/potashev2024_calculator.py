import math
from typing import List, Tuple
import mpmath
import numpy as np
from scipy.integrate import quad, trapezoid, simpson
from mpmath import ellipe, ellipf
import cmath
import time

from src.core.models.characteristic_data import CharacteristicData
from src.core.models.init_data.initial_data import InitialData
from src.core.models.input_data.input_data import InputData
from src.core.services.dimless_converter import DimlessConverter
from src.core.services.fracture_worker import calc_lm_lp


class Potashev2024Calculator:

    class SectorData:
        def __init__(self):
            self.ld: float = None
            self.rc: float = None
            self.H: float = None
            self.is_outer: bool = None
            self.char_data: CharacteristicData = None

        def __eq__(self, other) -> bool:
            if not isinstance(other, Potashev2024Calculator.SectorData):
                return False

            return (
                math.isclose(self.ld, other.ld, rel_tol=1e-9, abs_tol=1e-12)
                and math.isclose(self.rc, other.rc, rel_tol=1e-9, abs_tol=1e-12)
                and math.isclose(self.H, other.H, rel_tol=1e-9, abs_tol=1e-12)
                and self.is_outer == other.is_outer
                and self.char_data == other.char_data
            )

        def __hash__(self) -> int:
            # Округляем float-поля до 10 знаков
            def safe_round(x):
                return round(x, 10) if x is not None else None

            return hash(
                (
                    safe_round(self.ld),
                    safe_round(self.rc),
                    safe_round(self.H),
                    self.is_outer,
                    self.char_data,  # Использует __hash__ CharacteristicData
                )
            )

    class SectorsWorker:
        def __init__(self):
            pass

        def get_unique_sectors(
            self, init_data: InitialData
        ) -> Tuple[List[List[int]], List["Potashev2024Calculator.SectorData"]]:
            unique_sectors: dict[Potashev2024Calculator.SectorData, int] = {}
            sectors: List[Potashev2024Calculator.SectorData] = []
            fracture_indices: List[List[int]] = []

            for i, fr in enumerate(init_data.fractures):
                indices_for_fracture = []
                for is_left in [True, False]:
                    for is_plus in [True, False]:
                        sector = self.__make_one_sector(init_data, i, is_left, is_plus)

                        if sector in sectors:
                            idx = unique_sectors[sector]
                        else:
                            idx = len(sectors)
                            sectors.append(sector)
                            unique_sectors[sector] = idx

                        indices_for_fracture.append(idx)

                fracture_indices.append(indices_for_fracture)

            return [fracture_indices, sectors]

        def __make_one_sector(
            self, init_data: InitialData, fract_index: int, is_left: bool, is_plus: bool
        ) -> "Potashev2024Calculator.SectorData":

            xf = (
                init_data.fractures[fract_index].len_p
                if is_plus
                else init_data.fractures[fract_index].len_m
            )

            char_data = CharacteristicData()
            char_data.x0 = xf
            char_data.pw = init_data.well.pw
            char_data.pr = init_data.reservoir.pr
            char_data.mu = init_data.fluid.mu
            char_data.perm = init_data.reservoir.perm

            sector_data = self.__get_sector_data(
                init_data, char_data, fract_index, is_left
            )
            sector_data.char_data = char_data
            sector_data.is_outer = (fract_index == 0 and is_left) or (
                fract_index == len(init_data.fractures) - 1 and not is_left
            )

            return sector_data

        def __get_sector_data(
            self,
            init_data: InitialData,
            char_data: CharacteristicData,
            fract_index: int,
            is_left: bool,
        ) -> "Potashev2024Calculator.SectorData":

            dim_conv = DimlessConverter(char_data)

            result = Potashev2024Calculator.SectorData()

            lm, lp = calc_lm_lp(init_data, fract_index, False)
            result.ld = dim_conv.make_dimless_geom(lm if is_left else lp)
            result.rc = dim_conv.make_dimless_geom(init_data.reservoir.rc)
            result.H = dim_conv.make_dimless_geom(init_data.reservoir.H)

            return result

    class InnerSectorCalculator:
        def __init__(self):
            pass

        def calc_rate(self, sector: "Potashev2024Calculator.SectorData") -> float:

            ld = sector.ld
            rc = sector.rc

            if rc < 1.0 + 0.75 * ld:
                return None

            Q = self.__Q(rc, ld)
            result = Q * sector.H

            # convert to dim
            q0 = sector.char_data.get_q0()
            result_dim = result * q0

            return result_dim

        def __A(self, x: float, ld: float) -> float:
            alp = 0.8 * ld + 0.025 if ld <= 0.5 else 0.45
            return x ** (-alp)

        def __lam(self, x: float, ld: float) -> float:
            return 1.0 + 1.65 * ld - x * (1 + 0.9 * ld)

        def __omega(self, l: float, x: float, ld: float) -> float:

            A = self.__A(x, ld)
            a = 0.116 * (1 - x) * np.log(22 * ld) + 0.474 * x
            b = 0.1 / np.sqrt(1 - x) + 1.0 / (1.0 + 10.0 * x) + 0.29 * ld - 0.56
            c = 1.0 / (15.0 * (1.0 - x**1.5)) + 0.72 * ld - 0.2
            d = 1.0 + 2.985 * (ld - 0.5) * x**15
            s = 0.053 * (4.0 * ld * (x - 1) + 9.6 * (x + 1))
            s2 = s**2
            log_lda = np.log(l * d / a)

            exponent = -((s2 - log_lda) ** 2) / (2.0 * s2)
            term2_cf = (b * np.sqrt(2.0)) / (s * l * d * np.sqrt(np.pi))
            term2 = term2_cf * np.exp(exponent)

            # Stabilize tanh computation
            tanh_arg = A * log_lda
            # tanh_arg = np.clip(tanh_arg, -100, 100)  # Prevent overflow
            term3 = (c - 1) * np.tanh(tanh_arg)

            return 0.5 * (1 + c + term2 + term3)

        def __J(self, x: float, rc: float, ld: float) -> float:
            inner_r = 1.0 + 0.75 * ld
            lam_val = self.__lam(x, ld)

            result_part1 = 0.0
            if rc > inner_r:
                delta = rc - inner_r
                result_part1 = delta / self.__omega(lam_val, x, ld)

            integral_result, _ = quad(
                lambda l: 1.0 / self.__omega(l, x, ld), 0.0, 1.0, limit=1000
            )

            result_part2 = lam_val * integral_result

            return 1.0 / (result_part1 + result_part2)

        def __Q(self, rc: float, ld: float) -> float:
            result, _ = quad(lambda x: self.__J(x, rc, ld), 0.0, 0.99999, limit=300)

            return result

    class OuterSectorCalculator:
        def __init__(self) -> None:
            pass

        def calc_rate(self, sector: "Potashev2024Calculator.SectorData") -> float:

            r = sector.rc
            Q = self.__Q(r)
            result = Q * sector.H

            # convert to dim
            q0 = sector.char_data.get_q0()
            result_dim = result * q0

            return result_dim

        def __calc_ro(self, r: float) -> float:
            return r + math.sqrt(r**2 - 1.0)

        def __calc_iEw(self, x: float, r: float) -> float:
            ro = self.__calc_ro(r)
            fi_val = math.log(ro)  # Real-valued
            m_val = 1.0 / (1.0 - x**2)  # Real-valued

            # Convert to mpmath numbers for precision
            fi_mp = mpmath.mpf(fi_val)
            m_mp = mpmath.mpf(m_val)

            # Compute I * EllipticE(I * fi, m)
            I = mpmath.mpc(0, 1)
            arg = I * fi_mp
            E_val = mpmath.ellipe(arg, m_mp)
            result = I * E_val

            # Check and handle imaginary part
            if not mpmath.almosteq(result.imag, 0.0, rel_eps=1e-5, abs_eps=1e-5):
                print(f"Warning: Im part in __calc_iEw: {result.imag}")
            return float(result.real)

        def __lam(self, x: float, r: float) -> float:
            iEw = self.__calc_iEw(x, r)
            l_rho = math.log(self.__calc_ro(r))
            numerator = math.cosh(2.0 * l_rho) - math.cos(2.0 * math.acos(x))
            denominator = 2.0 * (1.0 - x**2) + 2.0 * math.sinh(l_rho) ** 2
            part_one = numerator / denominator
            part_two = math.sqrt((1.0 - x**2) * part_one)
            return -iEw * part_two

        def __omega(self, phi: float, x: float, r: float) -> float:
            l_rho = math.log(self.__calc_ro(r))
            a = math.acos(x)  # Real-valued
            b = phi * l_rho  # Real-valued
            # Complex sine calculation
            sin_val = cmath.sin(a - 1j * b)
            abs_part = abs(sin_val)
            return abs_part / math.sqrt(1.0 - x**2)

        def __J(self, x: float, r: float) -> float:
            lam_val = self.__lam(x, r)
            integral_result, _ = quad(
                lambda l: (1.0 / lam_val) * self.__omega(l, x, r), -1.0, 0.0, limit=300
            )
            return integral_result

        def __Q(self, r: float) -> float:
            result, _ = quad(lambda x: self.__J(x, r), 0.0, 0.9999, limit=300)

            return result

    def __init__(self) -> None:
        self.__inner_calculator = Potashev2024Calculator.InnerSectorCalculator()
        self.__outer_calculator = Potashev2024Calculator.OuterSectorCalculator()

    def calc_q(self, init_data: InitialData) -> float:
        """ """
        sectors_worker = Potashev2024Calculator.SectorsWorker()
        # Получаем:
        #   fracture_indices - список из 4 индексов секторов для каждой трещины
        #   unique_sectors - список уникальных секторов
        fract_indices, sectors = sectors_worker.get_unique_sectors(init_data)

        sectors_q = []
        for sector in sectors:
            q = self.__calc_sector_q(sector)
            sectors_q.append(q)

        total_rate = 0.0
        for fracture_sectors in fract_indices:
            fract_rate = 0.0
            for sector_index in fracture_sectors:
                sector_rate = sectors_q[sector_index]
                if sector_rate is None:
                    fract_rate = 0.0
                    break
                else:
                    fract_rate += sector_rate

            total_rate += fract_rate

        return total_rate

    def __calc_sector_q(self, sector: "Potashev2024Calculator.SectorData") -> float:
        return (
            self.__outer_calculator.calc_rate(sector)
            if sector.is_outer
            else self.__inner_calculator.calc_rate(sector)
        )

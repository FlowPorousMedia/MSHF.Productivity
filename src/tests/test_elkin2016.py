import csv
from itertools import product
from pathlib import Path
import unittest
from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from src.core.models.init_data.fluid_initial_data import FluidInitialData
from src.core.models.init_data.fract_initial_data import FractInitialData
from src.core.models.init_data.initial_data import InitialData
from src.core.models.init_data.reservoir_initial_data import ReservoirInitialData
from src.core.models.init_data.well_initial_data import WellInitialData
from src.core.services.analyt_models.elkin2016_calculator import Elkin2016Calculator
from src.core.services.measurement_converter import MeasurementConverter


class TestElkin2016Calculator(unittest.TestCase):
    def setUp(self):
        """Initialize test data and calculator before each test"""
        self.calculator = Elkin2016Calculator()

    def test_calc_parametric_to_file(self) -> None:
        Ns = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        Ls = [200, 500, 800, 1000, 1500, 2000, 3000, 5000]
        xfs = [30, 40, 50, 60, 70, 80, 90, 100]
        Rs = [120, 150, 200, 300, 500]
        Ms = [0.1, 1, 10, 100]
        Hs = [5, 10, 20, 30, 40]

        output_dir = self.__define_output_dir()
        output_file = output_dir / "elkin2016_parametric_study.csv"

        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["N", "L", "xf", "R", "M", "H", "q"])

            total_combinations = (
                len(Ns) * len(Ls) * len(xfs) * len(Rs) * len(Ms) * len(Hs)
            )
            current = 0

            for N, L, xf, R, M, H in product(Ns, Ls, xfs, Rs, Ms, Hs):
                current += 1
                if current % 1000 == 0:
                    print(f"Progress: {current}/{total_combinations}")

                try:
                    init_data = self.__create_init_data(N, L, xf, R, M, H)
                    q = self.calculator.calc_q(init_data) * 60 * 60 * 24
                    writer.writerow([N, L, xf, R, M, H, q])
                except Exception as e:
                    print(f"Error for params {N}, {L}, {xf}, {R}, {M}, {H}: {str(e)}")
                    writer.writerow([N, L, xf, R, M, H, None])

    def test_sensitivity_analysis(self) -> None:
        # Определяем проблему для анализа чувствительности
        problem = {
            "num_vars": 6,
            "names": ["N", "L", "xf", "R", "M", "H"],
            "bounds": [
                [2, 10],
                [200, 5000],
                [30, 100],
                [120, 500],
                [0.1, 100],
                [5, 40],
            ],
        }

        # Генерируем выборки
        param_values = saltelli.sample(problem, 1000)

        # Округляем целочисленные параметры
        for i in range(param_values.shape[0]):
            # Округляем N, L, xf, R, H до целых
            param_values[i, 0] = round(param_values[i, 0])  # N
            param_values[i, 1] = round(param_values[i, 1])  # L
            param_values[i, 2] = round(param_values[i, 2])  # xf
            param_values[i, 3] = round(param_values[i, 3])  # R
            param_values[i, 5] = round(param_values[i, 5])  # H

        # Вычисляем отклик (q) для каждой комбинации
        responses = []
        for params in param_values:
            try:
                init_data = self.__create_init_data(*params)
                q_value = self.calculator.calc_q(init_data) * 60 * 60 * 24
                responses.append(q_value)
            except Exception as e:
                # В случае ошибки добавляем NaN
                print(f"Error for params {params}: {str(e)}")
                responses.append(float("nan"))

        # Анализируем чувствительность, игнорируя NaN значения
        valid_indices = ~np.isnan(responses)
        valid_responses = np.array(responses)[valid_indices]
        valid_params = param_values[valid_indices]

        # Обновляем problem для валидных данных
        valid_problem = problem.copy()
        valid_problem["num_vars"] = valid_params.shape[1]

        si = sobol.analyze(valid_problem, valid_responses)

        # Визуализируем результаты
        self.__plot_sensitivity_results(si, problem["names"])

        return si, valid_params, valid_responses

    def __create_init_data(self, N, L, xf, R, M, H) -> InitialData:
        mc = MeasurementConverter()

        result = InitialData()

        d = L / (2.0 * (N - 1))
        delta = 0.01  # 1 cm
        kr = 1e-13
        kf = M * kr * R / delta

        for i in range(int(N)):
            # fracture
            fract = FractInitialData()
            fract.len_p = xf
            fract.len_m = xf
            fract.width = 2.0 * delta
            fract.perm = kf
            fract.well_cross_coord = i * 2 * d
            result.fractures.append(fract)

        # resevoir
        reservoir = ReservoirInitialData()
        reservoir.rc = R
        reservoir.H = H
        reservoir.perm = kr
        reservoir.pr = mc.convert_atm_to_Pa(100)
        result.reservoir = reservoir

        # well
        well = WellInitialData()
        well.L = L
        well.rw = 0.08
        well.pw = mc.convert_atm_to_Pa(80)
        well.is_perforated = False
        result.well = well

        # fluid
        fluid = FluidInitialData()
        fluid.mu = 1e-3
        result.fluid = fluid

        return result

    def __define_output_dir(self) -> Path:
        # Get current test file's directory
        current_dir = Path(__file__).resolve().parent

        # Navigate to project root
        project_root = current_dir.parent.parent

        # Create 'out' directory if it doesn't exist
        output_dir = project_root / "out"
        output_dir.mkdir(exist_ok=True, parents=True)

        return output_dir

    def __plot_sensitivity_results(self, si, names):
        # Первый порядок чувствительности
        S1 = si["S1"]

        # Общая чувствительность
        ST = si["ST"]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # График первого порядка
        ax1.bar(names, S1)
        ax1.set_title("First-order sensitivity")
        ax1.set_ylabel("Sensitivity index")
        ax1.tick_params(axis="x", rotation=45)

        # График общей чувствительности
        ax2.bar(names, ST)
        ax2.set_title("Total-order sensitivity")
        ax2.set_ylabel("Sensitivity index")
        ax2.tick_params(axis="x", rotation=45)

        plt.tight_layout()
        plt.savefig("sensitivity_analysis.png")
        plt.close()

        # Выводим результаты в таблицу
        results_df = pd.DataFrame(
            {"Parameter": names, "First_Order": S1, "Total_Order": ST}
        ).sort_values("Total_Order", ascending=False)

        print("Sensitivity Analysis Results:")
        print(results_df.to_string(index=False))

from typing import List
import numpy as np

from src.core.models.init_data.initial_data import InitialData
from src.core.models.input_data.fract_input_data import FractInputData
from src.core.services.fracture_worker import calc_lm_lp


class Guo2009Calculator:
    def __init__(self) -> None:
        self.__ip: InitialData = None
        self.__zei: List[float] = []

    def calc_q(self, input_data: InitialData) -> float:
        self.__ip = input_data
        self.__update_ze()
        result = 0.0
        j_big_r = self.__calc_j_big_r()
        j_big_l = self.__calc_j_big_l()
        j_small_r = self.__calc_j_small_r()

        dp = self.__ip.get_dp()
        denominator = 1.0 / j_big_r + 1.0 / j_big_l + 1.0 / j_small_r
        result = dp / denominator

        return result

    def __calc_rl(self) -> float:
        n = len(self.__ip.fractures)
        xf_aver = np.average([fr.len_p for fr in self.__ip.fractures])
        ze_aver = self.__get_ze()

        numerator = 4.0 * n * ze_aver * xf_aver
        denominator = np.pi
        return np.sqrt(numerator / denominator)

    def __calc_j_big_r(self) -> float:
        def global_denominator() -> float:
            gamma = 1.781  # exponential of Euler's constant, dimensionless
            rl = self.__calc_rl()
            A = np.pi * rl**2
            c_a = self.__get_ca()
            # print(f'c_a = {c_a}')

            local_numerator = 4.0 * A
            local_denominator = gamma * c_a * rl**2
            value = np.log(local_numerator / local_denominator)
            visc = self.__ip.fluid.mu
            return 0.5 * value * visc

        k = self.__ip.reservoir.perm
        h = self.__ip.reservoir.H
        numerator = 2.0 * np.pi * k * h
        denominator = global_denominator()
        result = numerator / denominator
        return result

    def __calc_j_big_l(self) -> float:
        p = self.__ip

        def calc_ci(fr: FractInputData, ze) -> float:
            return (24 * self.__ip.reservoir.perm) / (ze * fr.width * fr.perm)

        result = 0.0
        const = 4.0  # 4.5e-3
        k = self.__ip.reservoir.perm
        mu = self.__ip.fluid.mu
        cf = const * k * p.reservoir.H / mu
        for i, fr in enumerate(self.__ip.fractures):
            ze = self.__zei[i]
            ci = calc_ci(fr, ze)
            numerator = 1 - np.exp(-np.sqrt(ci) * fr.len_p)
            denominator = ze * np.sqrt(ci)
            v = numerator / denominator
            result += v
        result *= cf
        return result

    def __calc_j_small_r(self) -> float:
        p = self.__ip
        result = 0.0
        const = np.pi / 6.0  # 5.9e-4
        mu = self.__ip.fluid.mu
        for fr in p.fractures:
            numerator = const * fr.perm * fr.width
            denominator = mu * (
                np.log(p.reservoir.H / (2.0 * p.well.rw)) + np.pi - 1.224
            )
            v = numerator / denominator
            result += v
        return result

    def __get_ca(self) -> float:
        rc = self.__ip.reservoir.rc
        ah = rc / self.__ip.reservoir.H

        n = len(self.__ip.fractures)
        lf = np.average([fr.len_p for fr in self.__ip.fractures])
        ze = self.__get_ze()
        ah = n * ze / lf

        table = [
            (3, 11.4948),
            (4, 5.3790),
            (6, 0.9935),
            (7, 0.4068),
            (8, 0.1632),
            (9, 6.44e-2),
            (10, 2.51e-2),
            (11, 9.69e-3),
            (12, 3.71e-3),
            (13, 1.41e-3),
            (14, 5.33e-4),
            (15, 2.00e-4),
            (16, 7.50e-5),
            (17, 2.80e-5),
            (18, 1.04e-5),
            (19, 3.85e-6),
            (20, 1.42e-6),
            (25, 9.46e-9),
            (29, 1.66e-11),
            (40, 2.28e-18),
            (67, 2.01e-27),
        ]

        # If ah value is less than the first element, return the minimum c2 value
        if ah < table[0][0]:
            # return min(table, key=lambda x: x[1])[1]
            return table[0][1]

        # If ah value is greater than the last element, return the maximum c2 value
        elif ah > table[-1][0]:
            # return max(table, key=lambda x: x[1])[1]
            return table[-1][1]

        # Find the two nearest values of c1
        for i in range(len(table) - 1):
            if table[i][0] <= ah <= table[i + 1][0]:
                c1_left, c2_left = table[i]
                c1_right, c2_right = table[i + 1]
                break

        # Perform linear interpolation
        ca = c2_left + (c2_right - c2_left) * (ah - c1_left) / (c1_right - c1_left)

        return ca

    def __update_ze(self) -> None:
        n = len(self.__ip.fractures)
        self.__zei.clear()
        for i in range(n):
            lm, lp = calc_lm_lp(self.__ip, i, account_rc=False)
            if i == 0:
                d = lp
            elif i == n - 1:
                d = lm
            else:
                d = (lp + lm) / 2.0
            self.__zei.append(d)

    def __get_ze(self) -> float:
        return np.average(self.__zei)

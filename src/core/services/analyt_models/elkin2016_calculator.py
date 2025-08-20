import numpy as np

from src.core.models.init_data.initial_data import InitialData
from src.core.services.fracture_worker import calc_lm_lp


class Elkin2016Calculator:
    def __init__(self) -> None:
        self.__ip: InitialData = None
        self.__xf: float = None
        self.__alpha: float = None

    def calc_q(self, init_data: InitialData) -> float:
        self.__ip = init_data
        self.__xf = self.__ip.fractures[0].len_p
        self.__alpha = 0.0

        q = self.__calc_q_inner()
        qd = self.__calc_q_outer()

        return q + qd

    def __calc_q_inner(self) -> float:
        a2 = self.__ip.reservoir.rc - self.__xf * np.cos(self.__alpha)
        cf = (
            2.0 * self.__ip.reservoir.perm * self.__ip.reservoir.H * self.__ip.well.L
        ) / (self.__ip.fluid.mu * a2)
        p0 = self.__calc_p0()
        a = self.__calc_a()

        part1 = ((1.0 + 2.0 * a) / (1.0 + a)) * (p0 / 2.0)
        part2 = (1.0 / (1.0 + a)) * (self.__ip.well.pw / 2.0)

        return cf * (self.__ip.reservoir.pr - part1 - part2)

    def __calc_q_outer(self) -> float:
        cf = (2.0 * np.pi * self.__ip.reservoir.perm * self.__ip.reservoir.H) / (
            self.__ip.fluid.mu
        )
        dp = self.__ip.get_dp()

        return (cf * dp) / (np.log((2.0 * self.__ip.reservoir.rc) / self.__xf))

    def __calc_p0(self) -> float:
        a = self.__calc_a()
        b_tilde = self.__calc_b_tilde()

        numer = self.__ip.reservoir.pr * (1 + a) - (0.5 - b_tilde) * self.__ip.well.pw
        denom = 0.5 + b_tilde + a

        return numer / denom

    def __calc_a(self) -> float:
        N = len(self.__ip.fractures)
        fcd = self.__ip.calc_fcd(0)
        numer = 2.0 * self.__xf * (N - 1) * np.cos(self.__alpha)
        denom = self.__ip.well.L * fcd

        return numer / denom

    def __calc_b_tilde(self) -> float:
        N = len(self.__ip.fractures)
        a1 = (N - 1) ** 2
        a2 = self.__ip.reservoir.rc - self.__xf * np.cos(self.__alpha)
        numer = 4.0 * a1 * self.__xf * a2
        denom = self.__ip.well.L**2 * np.cos(self.__alpha)

        return numer / denom

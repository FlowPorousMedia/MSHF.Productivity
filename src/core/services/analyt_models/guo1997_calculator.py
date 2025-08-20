import numpy as np

from src.core.models.init_data.initial_data import InitialData
from src.core.services.fracture_worker import calc_lm_lp


class Guo1997Calculator:
    def __init__(self) -> None:
        self.__ip: InitialData = None

    def calc_q(self, init_data: InitialData) -> float:
        self.__ip = init_data

        result = 0.0
        for i in range(len(self.__ip.fractures)):
            qf_plus = self.__calc_fract_wing(i, True)
            qf_minus = self.__calc_fract_wing(i, False)
            result += qf_plus + qf_minus

        return result

    def __calc_fract_wing(self, fract_index: int, is_plus: float) -> float:
        fr = self.__ip.fractures[fract_index]
        lf1, lf2 = calc_lm_lp(self.__ip, fract_index, True)
        xf = fr.len_p if is_plus else fr.len_m
        qf_left_shore = self.__calc_fract_wing_shore(fract_index, xf, lf1)
        qf_right_shore = self.__calc_fract_wing_shore(fract_index, xf, lf2)
        return qf_left_shore + qf_right_shore

    def __calc_fract_wing_shore(self, fract_index, xf, ze) -> float:
        res = self.__ip.reservoir

        dp = self.__ip.get_dp()
        mu = self.__ip.fluid.mu
        kr = res.perm
        c = self.__calc_c(fract_index, ze)
        part_exp = 1.0 - np.exp(-np.sqrt(c) * xf)
        part_cf = (2.0 * res.H * kr) / (mu * ze * np.sqrt(c))
        return part_cf * dp * part_exp

    def __calc_c(self, fract_index: int, ze: float) -> float:
        fr = self.__ip.fractures[fract_index]
        res = self.__ip.reservoir

        w = fr.width
        kf = fr.perm
        kr = res.perm

        return (2.0 * kr) / (w * ze * kf)

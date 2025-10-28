from typing import Any, Dict, List
import numpy as np
from src.core.models.calculator_settings import CalculatorSettings
from src.core.models.init_data.initial_data import InitialData
from src.core.services.fracture_worker import calc_lm_lp


class Li1996Calculator:

    def __init__(self) -> None:
        self.__init_data: InitialData = None
        self.__setts: CalculatorSettings = None
        self.__logs: List[Dict[str, Any]] = None

    def calc_q(
        self,
        init_data: InitialData,
        setts: CalculatorSettings,
        logs: List[Dict[str, Any]],
    ) -> float:
        """ """
        self.__init_data = init_data
        self.__setts = setts
        self.__logs = logs
        return self.__calc_total_rate()

    def __calc_total_rate(self) -> float:
        """ """
        result = 0.0
        for i in range(len(self.__init_data.fractures)):
            qf = self.__calc_fract_q(i)
            result += qf

        self.__init_data = None

        return result

    def __calc_fract_q(self, fract_index: int) -> float:
        dp = self.__init_data.get_dp()
        a = self.__calc_a(fract_index)
        result = 2 * dp / a

        return result

    def __calc_a(self, fract_index: int) -> float:
        return (
            self.__calc_a_perf(fract_index)
            if self.__init_data.well.is_perforated
            else self.__calc_a_no_perf(fract_index)
        )

    def __calc_a_no_perf(self, fract_index: int) -> float:
        result = 0.0

        fract = self.__init_data.fractures[fract_index]
        res = self.__init_data.reservoir
        well = self.__init_data.well

        rc = res.rc
        xf = fract.len_p
        h = res.H
        k = res.perm
        mu = self.__init_data.fluid.mu
        kf = fract.perm
        w = fract.width
        rw = well.rw

        lf1, lf2 = calc_lm_lp(
            self.__init_data, fract_index, self.__setts.Li96_account_rc
        )
        a1 = (rc - xf) / (k * h * (lf1 + lf2))
        a2 = 1.0 / (k * h * xf * (1.0 / lf1 + 1.0 / lf2))
        a3 = xf / (kf * h * w)
        a4_cf = 1.0 / (kf * w * np.pi)
        a4 = a4_cf * (np.log(h / (2.0 * rw)) - np.pi / 2.0)

        result = mu * (a1 + a2 + a3 + a4)

        return result

    def __calc_a_perf(self, fract_index: int) -> float:

        fract = self.__init_data.fractures[fract_index]
        res = self.__init_data.reservoir
        well = self.__init_data.well

        lf1, lf2 = calc_lm_lp(
            self.__init_data, fract_index, self.__setts.Li96_account_rc
        )
        rc = res.rc
        Ld = well.Ld
        xf = fract.len_p
        h = res.H
        k = res.perm
        mu = self.__init_data.fluid.mu
        kf = fract.perm
        w = fract.width
        rw = well.rw

        c = xf / h - 0.5 + 1.0 / np.pi * np.log(h / (2.0 * rw))
        a = 1.0 / (k * h * xf * (1.0 / lf1 + 1.0 / lf2)) + c / (kf * w)
        b = (k * Ld * (lf1 + lf2)) / c
        d = (rc - xf) / (k * h * (lf1 + lf2))

        return mu * (1.0 / (1.0 / a + b) + d)

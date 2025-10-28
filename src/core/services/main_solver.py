import time
from typing import Any, Dict, List
import numpy as np
import copy


from src.core.models.calculator_settings import CalculatorSettings
from src.core.models.init_data.initial_data import InitialData
from src.core.models.init_data.models_enum import ModelsEnum
from src.core.models.logcategory import LogCategory
from src.core.models.loglevel import LogLevel
from src.core.models.main_data import MainData
from src.core.models.result_data.model_result_data import ModelResultData
from src.core.models.result_data.result_data import ResultData
from src.core.models.result_data.result_type_enum import ResultTypeEnum
from src.core.services.analyt_models.elkin2016_calculator import Elkin2016Calculator
from src.core.services.analyt_models.guo1997_calculator import Guo1997Calculator
from src.core.services.analyt_models.guo2009_calculator import Guo2009Calculator
from src.core.services.analyt_models.li1996_calculator import Li1996Calculator
from src.core.services.log_worker import make_log
from src.core.services.param_data_worker import ParamDataWorker
from src.core.services.semianalytical_models.potashev2024_calculator import (
    Potashev2024Calculator,
)
from src.core.models.init_data.calc_over_param_enum import CalcParamTypeEnum


class MainSolver:
    def __init__(self):
        self.__result: MainData = None
        self.__logs: List[Dict[str, Any]] = None

    def calc(self, init_data: InitialData, logs: List[Dict[str, Any]]) -> MainData:
        self.__logs = logs

        result = MainData()
        result.initial_data = init_data
        result.result = ResultData()

        self.__result = result

        match self.__result.initial_data.settings.calc_settings.calc_type:
            case ResultTypeEnum.SIMPLE:
                self.__calc_simple()
            case ResultTypeEnum.PARAMETRIC:
                self.__calc_parametric()
            case _:
                print("only simple calc is available")

        return result

    def __calc_simple(self) -> None:
        self.__result.result.result_type = ResultTypeEnum.SIMPLE

        for calc_model in self.__result.initial_data.settings.calc_models:
            model_type = calc_model.tp
            q = self.__calc_model_q(model_type)
            model = ModelResultData()
            model.name = calc_model.name
            model.q_values = np.array([q])
            self.__result.result.models.append(model)

    def __calc_parametric(self) -> None:
        self.__result.result.result_type = ResultTypeEnum.PARAMETRIC
        original_init_data = copy.deepcopy(self.__result.initial_data)

        p1 = original_init_data.settings.calc_settings.calc_over_param1
        param_type = p1.param_type

        if param_type == CalcParamTypeEnum.FRACT_PERM:
            start_log = np.log10(p1.start_value)
            end_log = np.log10(p1.end_value)
            orig_values = np.logspace(start_log, end_log, num=p1.point_count)
        else:
            orig_values = np.linspace(p1.start_value, p1.end_value, p1.point_count)

        worker = ParamDataWorker()
        init_datas: List[InitialData] = []

        for user_value in orig_values:
            si_value = param_type.to_si(user_value)
            init_d = worker.create_initial_data(
                original_init_data,
                si_value,
                p1.param_type,
            )
            init_datas.append(init_d)

        for calc_model in original_init_data.settings.calc_models:
            start_time = time.perf_counter()
            model_type = calc_model.tp
            model = ModelResultData()
            model.name = calc_model.name
            model.q_values = []
            model.param1_type = p1.param_type
            model.param1_values = orig_values
            for init_d in init_datas:
                self.__result.initial_data = init_d
                q = self.__calc_model_q(model_type)
                model.q_values.append(q)
            self.__result.result.models.append(model)
            end_time = time.perf_counter()
            calc_time = end_time - start_time
            self.__logs.append(
                make_log(
                    f"{model.name} calculated in {calc_time:.2f} sec",
                    LogLevel.INFO,
                    LogCategory.CALCULATION,
                    True,
                )
            )

    def __calc_model_q(self, model_type: ModelsEnum) -> float:
        setts = CalculatorSettings()
        setts.Li96_account_rc = True
        calculator = None
        match model_type:
            case ModelsEnum.LI_1996:
                calculator = Li1996Calculator()
            case ModelsEnum.GUO_1997:
                calculator = Guo1997Calculator()
            case ModelsEnum.GUO_2009:
                calculator = Guo2009Calculator()
            case ModelsEnum.ELKIN_2016_12:
                calculator = Elkin2016Calculator()
            case ModelsEnum.POTASHEV_2024:
                calculator = Potashev2024Calculator()
            case _:
                Exception("calc model rate with unknown model type")

        q_dim_m3_sec = calculator.calc_q(self.__result.initial_data, setts, self.__logs)
        q_dim_m3_day = None
        if q_dim_m3_sec is not None:
            q_dim_m3_day = q_dim_m3_sec * 60 * 60 * 24
        return q_dim_m3_day

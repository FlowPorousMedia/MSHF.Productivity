from src.core.models.init_data.calc_over_param_enum import CalcParamTypeEnum
from src.core.models.result_data.result_type_enum import ResultTypeEnum


class ParametricSettings:
    def __init__(self):
        self.calc_type: ResultTypeEnum = ResultTypeEnum.SIMPLE
        self.tp: CalcParamTypeEnum = None
        self.start: float = None
        self.end: float = None
        self.point_count: int = None

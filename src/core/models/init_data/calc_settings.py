from src.core.models.init_data.calc_over_param import CalcOverParam
from src.core.models.result_data.result_type_enum import ResultTypeEnum


class CalcSettings:
    def __init__(self):
        self.calc_type: ResultTypeEnum = ResultTypeEnum.SIMPLE
        self.calc_over_param1: CalcOverParam = None
        self.calc_over_param2: CalcOverParam = None

    def to_dict(self) -> dict:
        return {
            "calc_type": self.calc_type.value,  # Получаем значение enum
            "calc_over_param1": (
                self.calc_over_param1.to_dict()
                if self.calc_over_param1 is not None
                else None
            ),
            "calc_over_param2": (
                self.calc_over_param2.to_dict()
                if self.calc_over_param2 is not None
                else None
            ),
        }

from typing import List

from src.core.models.init_data.calc_over_param_enum import CalcParamTypeEnum


class ModelResultData:
    def __init__(self):
        self.name: str = None
        self.q_values: List[float] = []
        self.param1_values: List[float] = []
        self.param1_type: CalcParamTypeEnum = None
        self.param2_values: List[float] = []
        self.param2_type: CalcParamTypeEnum = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "q_values": self.q_values,
            "param1_values": self.param1_values,
            "param1_type_value": (
                self.param1_type.value if self.param1_type is not None else None
            ),
            "param2_values": self.param2_values,
            "param2_type_value": (
                self.param2_type.value if self.param2_type is not None else None
            ),
        }

from src.core.models.init_data.calc_over_param_enum import CalcParamTypeEnum


class CalcOverParam:
    def __init__(self):
        self.param_type: CalcParamTypeEnum = None
        self.start_value: float = None
        self.end_value: float = None
        self.point_count: int = None

    def to_dict(self) -> dict:
        return {
            "param_type": (
                self.param_type.value if self.param_type is not None else None
            ),
            "start_value": self.start_value,
            "end_value": self.end_value,
            "point_count": self.point_count,
        }

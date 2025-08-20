from typing import List

from src.core.models.result_data.model_result_data import ModelResultData
from src.core.models.result_data.result_type_enum import ResultTypeEnum


class ResultData:
    def __init__(self):
        self.models: List[ModelResultData] = []
        self.result_type: ResultTypeEnum = ResultTypeEnum.SIMPLE

    def to_dict(self) -> dict:
        return {
            "models": [model.to_dict() for model in self.models],
            "result_type": self.result_type.value,
        }

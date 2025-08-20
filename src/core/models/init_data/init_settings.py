from typing import List
from src.core.models.init_data.calc_settings import CalcSettings
from src.core.models.result_data.calc_model import CalcModel


class InitialSettings:
    def __init__(self):
        self.calc_settings: CalcSettings = None
        self.calc_models: List[CalcModel] = []

    def to_dict(self) -> dict:
        return {
            "calc_settings": (
                self.calc_settings.to_dict() if self.calc_settings is not None else None
            ),
            "calc_models": [model.to_dict() for model in self.calc_models],
        }

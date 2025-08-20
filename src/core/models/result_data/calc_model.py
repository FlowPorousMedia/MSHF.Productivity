from src.core.models.init_data.models_enum import ModelsEnum


class CalcModel:
    def __init__(self):
        self.tp: ModelsEnum = None
        self.name: str = None

    def to_dict(self) -> dict:
        return {"tp": self.tp.value if self.tp is not None else None, "name": self.name}

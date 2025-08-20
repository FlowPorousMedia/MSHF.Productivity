from src.core.models.init_data.initial_data import InitialData
from src.core.models.characteristic_data import CharacteristicData
from src.core.models.input_data.input_data import InputData
from src.core.models.result_data.result_data import ResultData


class MainData:
    def __init__(self):
        self.initial_data: InitialData = None
        self.result: ResultData = None

    def to_dict(self) -> dict:
        """Преобразует объект в словарь, используя to_dict() всех вложенных объектов"""
        return {
            "initial_data": (
                self.initial_data.to_dict() if self.initial_data is not None else None
            ),
            "result": self.result.to_dict() if self.result is not None else None,
        }

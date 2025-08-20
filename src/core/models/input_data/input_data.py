from typing import List

from src.core.models.input_data.fract_input_data import FractInputData
from src.core.models.input_data.res_input_data import ReservoirInputData
from src.core.models.input_data.well_input_data import WellInputData


class InputData:
    def __init__(self):
        self.fractures: List[FractInputData] = []
        self.well: WellInputData = None
        self.reservoir: ReservoirInputData = None

    def to_dict(self) -> dict:
        return {
            "fractures": [fracture.to_dict() for fracture in self.fractures],
            "well": self.well.to_dict() if self.well is not None else None,
            "reservoir": (
                self.reservoir.to_dict() if self.reservoir is not None else None
            ),
        }

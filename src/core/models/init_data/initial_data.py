from typing import List

from src.core.models.init_data.fract_initial_data import FractInitialData
from src.core.models.init_data.init_settings import InitialSettings
from src.core.models.init_data.reservoir_initial_data import ReservoirInitialData
from src.core.models.init_data.well_initial_data import WellInitialData
from src.core.models.init_data.fluid_initial_data import FluidInitialData


class InitialData:
    def __init__(self):
        self.fractures: List[FractInitialData] = []
        self.reservoir: ReservoirInitialData = None
        self.well: WellInitialData = None
        self.fluid: FluidInitialData = None
        self.settings: InitialSettings = None

    def get_dp(self) -> float:
        return self.reservoir.pr - self.well.pw

    def calc_fcd(self, fract_index: int) -> float:
        fr = self.fractures[fract_index]
        return (fr.perm * fr.width) / (self.reservoir.perm * fr.len_p)

    def get_M(self, fract_index: int) -> float:
        fr = self.fractures[fract_index]
        rc = self.reservoir.rc
        delta = fr.width / 2.0
        return (fr.perm * delta) / (self.reservoir.perm * rc)

    def to_dict(self) -> dict:
        """Преобразует объект в словарь с использованием to_dict() вложенных объектов"""
        return {
            "fractures": [fracture.to_dict() for fracture in self.fractures],
            "reservoir": (
                self.reservoir.to_dict() if self.reservoir is not None else None
            ),
            "well": self.well.to_dict() if self.well is not None else None,
            "fluid": self.fluid.to_dict() if self.fluid is not None else None,
            "settings": self.settings.to_dict() if self.settings is not None else None,
        }

from enum import Enum


class FracInitFieldNames(Enum):
    LENGTH_PLUS = "Length Plus (m)"
    LENGTH_MINUS = "Length Minus (m)"
    WIDTH = "Width (mm)"
    PERMEABILITY = "Permeability (D)"
    WELL_CROSS = "Well cross depth (m)"

    @property
    def value_str(self):
        return self.value

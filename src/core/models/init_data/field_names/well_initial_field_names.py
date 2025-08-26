from enum import Enum


class WellInitFieldNames(Enum):
    L = "Length (m)"
    RW = "Radius (cm)"
    PW = "Pressure (atm)"
    IS_PERFORATED = "Perforated"

    @property
    def value_str(self):
        return self.value

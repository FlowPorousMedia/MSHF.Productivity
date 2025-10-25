from enum import Enum


class CalcParamTypeEnum(Enum):
    FRACT_COUNT = 0
    FRACT_LEN = 1
    FRACT_PERM = 2
    FRACT_WIDTH = 3
    WELL_LEN = 4
    RES_RAD = 5
    RES_HEIGTH = 6

    @property
    def display_name(self):
        name_map = {
            self.FRACT_COUNT: "Fract count",
            self.RES_RAD: "Reservoir radius, m",
            self.RES_HEIGTH: "Reservoir height, m",
            self.WELL_LEN: "Well length, m",
            self.FRACT_LEN: "Fract length, m",
            self.FRACT_PERM: "Fract perm, D",
            self.FRACT_WIDTH: "Fract width, mm",
        }
        return name_map.get(self, self.value)

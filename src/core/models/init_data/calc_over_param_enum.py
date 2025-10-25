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
            self.FRACT_COUNT: "N",
            self.RES_RAD: "R",
            self.RES_HEIGTH: "H",
            self.WELL_LEN: "L",
            self.FRACT_LEN: "Xf",
            self.FRACT_PERM: "Kf",
            self.FRACT_WIDTH: "Wf",
        }
        return name_map.get(self, self.value)

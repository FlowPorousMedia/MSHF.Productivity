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
            self.FRACT_COUNT: "Fracture Count",
            self.RES_RAD: "Drainage Radius",
            self.RES_HEIGTH: "Reservior height",
            self.WELL_LEN: "Well Length",
            self.FRACT_LEN: "Fracture Half Length",
            self.FRACT_PERM: "Fracture Permeability",
            self.FRACT_WIDTH: "Fracture Width",
        }
        return name_map.get(self, self.value)

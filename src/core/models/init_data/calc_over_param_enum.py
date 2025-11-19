from enum import Enum

from src.app.i18n import _


class CalcParamTypeEnum(Enum):
    FRACT_COUNT = 0
    FRACT_LEN = 1
    FRACT_PERM = 2
    FRACT_WIDTH = 3
    WELL_LEN = 4
    RES_RAD = 5
    RES_HEIGTH = 6

    @property
    def label(self):
        name_map = {
            self.FRACT_COUNT: _("Fract count"),
            self.FRACT_LEN: _("Fract length, (m)"),
            self.FRACT_PERM: _("Fract perm, (D)"),
            self.FRACT_WIDTH: _("Fract width, (mm)"),
            self.RES_RAD: _("Reservoir radius, (m)"),
            self.RES_HEIGTH: _("Reservoir height, (m)"),
            self.WELL_LEN: _("Well length, (m)"),
        }
        return name_map.get(self, self.value)

    def to_si(self, value: float) -> float:
        """Convert from user units to SI."""
        if self == self.FRACT_WIDTH:
            return value / 1000.0  # mm → m
        elif self == self.FRACT_PERM:
            return value * 9.869233e-13  # D → m² (1 D ≈ 9.869233e-13 m²)
        else:
            return value  # уже в СИ (m, безразмерные и т.д.)

    def from_si(self, value: float) -> float:
        """Convert from SI to user units (опционально, для обратной конвертации)."""
        if self == self.FRACT_WIDTH:
            return value * 1000.0  # m → mm
        elif self == self.FRACT_PERM:
            return value / 9.869233e-13  # m² → D
        else:
            return value

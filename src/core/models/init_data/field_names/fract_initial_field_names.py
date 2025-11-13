from enum import Enum

from src.app.i18n import _


class FracInitFieldNames(Enum):
    LENGTH_PLUS = "LENGTH_PLUS"
    LENGTH_MINUS = "LENGTH_MINUS"
    WIDTH = "WIDTH"
    PERMEABILITY = "PERMEABILITY"
    WELL_CROSS = "WELL_CROSS"

    @property
    def label(self):
        labels = {
            FracInitFieldNames.LENGTH_PLUS: _("Length Plus, (m)"),
            FracInitFieldNames.LENGTH_MINUS: _("Length Minus, (m)"),
            FracInitFieldNames.WIDTH: _("Width, (mm)"),
            FracInitFieldNames.PERMEABILITY: _("Permeability, (D)"),
            FracInitFieldNames.WELL_CROSS: _("Well cross depth, (m)"),
        }
        return labels[self]

from enum import Enum

from src.app.i18n import _


class WellInitFieldNames(Enum):
    L = "L"
    RW = "RW"
    PW = "PW"
    IS_PERFORATED = "IS_PERFORATED"

    @property
    def label(self):
        labels = {
            WellInitFieldNames.L: _("Length, (m)"),
            WellInitFieldNames.RW: _("Radius, (cm)"),
            WellInitFieldNames.PW: _("Pressure, (atm)"),
            WellInitFieldNames.IS_PERFORATED: _("Perforated"),
        }
        return labels[self]

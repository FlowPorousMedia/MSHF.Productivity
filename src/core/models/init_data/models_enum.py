from enum import Enum

from src.app.i18n import _


class ModelsEnum(Enum):
    LI_1996 = "LI_1996"
    GUO_1997 = "GUO_1997"
    GUO_2009 = "GUO_2009"
    ELKIN_2016_12 = "ELKIN_2016_12"
    POTASHEV_2024 = "POTASHEV_2024"

    @property
    def label(self):
        name_map = {
            ModelsEnum.LI_1996: _("Li (1996)"),
            ModelsEnum.GUO_1997: _("Guo (1997)"),
            ModelsEnum.GUO_2009: _("Guo (2009)"),
            ModelsEnum.ELKIN_2016_12: _("Elkin (2016)"),
            ModelsEnum.POTASHEV_2024: _("Potashev (2024)"),
        }
        return name_map.get(self, self.value)

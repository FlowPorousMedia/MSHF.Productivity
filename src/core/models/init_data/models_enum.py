from enum import Enum


class ModelsEnum(Enum):
    LI_1996 = "LI_1996"
    GUO_1997 = "GUO_1997"
    GUO_2009 = "GUO_2009"
    ELKIN_2016_12 = "ELKIN_2016_12"
    POTASHEV_2024 = "POTASHEV_2024"

    @property
    def display_name(self):
        name_map = {
            ModelsEnum.LI_1996: "Li (1996)",
            ModelsEnum.GUO_1997: "Guo (1997)",
            ModelsEnum.GUO_2009: "Guo (2009)",
            ModelsEnum.ELKIN_2016_12: "Elkin (2016, v12)",
            ModelsEnum.POTASHEV_2024: "Potashev (2024)",
        }
        return name_map.get(self, self.value)

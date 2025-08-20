class FractInitialData:
    def __init__(self):
        self.len_p: float = None
        self.len_m: float = None
        self.width: float = None
        self.perm: float = None
        self.well_cross_coord: float = None

    def to_dict(self) -> dict:
        """Возвращает словарь с простыми типами данных (не требуется рекурсия)"""
        return {
            "len_p": self.len_p,
            "len_m": self.len_m,
            "width": self.width,
            "perm": self.perm,
            "well_cross_coord": self.well_cross_coord,
        }

class FractInputData:
    def __init__(self):
        self.len_p: float = None
        self.len_m: float = None
        self.width: float = None
        self.perm: float = None
        self.yf: float = None

    def to_dict(self) -> dict:
        return {
            "len_p": self.len_p,
            "len_m": self.len_m,
            "width": self.width,
            "perm": self.perm,
            "yf": self.yf,
        }

class WellInitialData:
    def __init__(self):
        self.L: float = None
        self.rw: float = None
        self.pw: float = None
        self.is_perforated: float = False

    def to_dict(self) -> dict:
        return {
            "L": self.L,
            "rw": self.rw,
            "pw": self.pw,
            "is_perforated": self.is_perforated,
        }

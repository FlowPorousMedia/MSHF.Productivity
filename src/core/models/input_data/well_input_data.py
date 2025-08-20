class WellInputData:
    def __init__(self):
        self.L: float = None
        self.rw: float = None
        self.is_perforated: float = False

    def to_dict(self) -> dict:
        return {"L": self.L, "rw": self.rw, "is_perforated": self.is_perforated}

class ReservoirInputData:
    def __init__(self):
        self.H: float = None
        self.rc: float = None

    def to_dict(self) -> dict:
        return {"H": self.H}

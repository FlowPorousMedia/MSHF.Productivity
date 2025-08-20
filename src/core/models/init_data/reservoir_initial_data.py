class ReservoirInitialData:
    def __init__(self):
        self.rc: float = None
        self.H: float = None
        self.perm: float = None
        self.pr: float = None

    def to_dict(self) -> dict:
        return {"rc": self.rc, "H": self.H, "perm": self.perm, "pr": self.pr}

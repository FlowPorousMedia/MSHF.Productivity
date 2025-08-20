class FluidInitialData:
    def __init__(self):
        self.mu: float = None

    def to_dict(self) -> dict:
        return {"mu": self.mu}

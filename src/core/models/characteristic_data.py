import math


class CharacteristicData:
    def __init__(self):
        self.perm: float = None
        self.mu: float = None
        self.x0: float = None
        self.pw: float = None
        self.pr: float = None

    def to_dict(self) -> dict:
        return {
            "perm": self.perm,
            "mu": self.mu,
            "x0": self.x0,
            "pw": self.pw,
            "pr": self.pr,
        }

    def get_sigma0(self) -> float:
        return self.perm / self.mu

    def get_dp(self) -> float:
        return self.pr - self.pw

    def get_u0(self) -> float:
        sigma0 = self.get_sigma0()
        dp = self.get_dp()

        return sigma0 * dp / self.x0

    def get_q0(self) -> float:
        u0 = self.get_u0()
        return u0 * self.x0**2

    def __eq__(self, other) -> bool:
        if not isinstance(other, CharacteristicData):
            return False

        return (
            math.isclose(self.perm, other.perm, rel_tol=1e-9, abs_tol=1e-12)
            and math.isclose(self.mu, other.mu, rel_tol=1e-9, abs_tol=1e-12)
            and math.isclose(self.x0, other.x0, rel_tol=1e-9, abs_tol=1e-12)
            and math.isclose(self.pw, other.pw, rel_tol=1e-9, abs_tol=1e-12)
            and math.isclose(self.pr, other.pr, rel_tol=1e-9, abs_tol=1e-12)
        )

    def __hash__(self) -> int:
        # Округляем значения до 10 знаков для стабильного хеша
        def safe_round(x):
            return round(x, 10) if x is not None else None

        return hash(
            (
                safe_round(self.perm),
                safe_round(self.mu),
                safe_round(self.x0),
                safe_round(self.pw),
                safe_round(self.pr),
            )
        )

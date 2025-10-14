from typing import List, Tuple


class WellInitialData:
    def __init__(self):
        self.L: float = None
        self.rw: float = None
        self.pw: float = None
        self.is_perforated: float = False
        self.Ld: float = None    # well pefr ratio [0, 1]

    def to_dict(self) -> dict:
        return {
            "L": self.L,
            "rw": self.rw,
            "pw": self.pw,
            "is_perforated": self.is_perforated,
            "Ld": self.Ld
        }

    def validate_and_raise(self, reservoir_press: float) -> List[str]:
        """
        Validate and raise exception for errors, return warnings
        """
        errors, warnings = self.__validate_data(reservoir_press)

        if errors:
            numbered_errors = [f"{i+1}. {error}" for i, error in enumerate(errors)]
            raise ValueError("\n".join(numbered_errors))

        if warnings:
            warnings = [f"{i+1}. {warning}" for i, warning in enumerate(warnings)]

        return warnings

    def __validate_data(self, reservoir_press: float) -> Tuple[List[str], List[str]]:
        """Validate all fields and raise ValueError if any validation fails"""
        errors = []
        warnings = []

        self.L: float = None
        self.rw: float = None
        self.pw: float = None

        if self.L is None:
            errors.append(f"Well Length (m) is required")
        elif self.L <= 0:
            errors.append("Well Length (m) should be positive number")
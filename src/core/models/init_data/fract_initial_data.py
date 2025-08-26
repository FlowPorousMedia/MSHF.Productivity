from typing import List, Tuple


class FractInitialData:
    def __init__(self):
        self.len_p: float = None
        self.len_m: float = None
        self.width: float = None
        self.perm: float = None
        self.well_cross_coord: float = None

    def validate_and_raise(
        self, well_len: float = None, reservoir_perm: float = None
    ) -> List[str]:
        """
        Validate and raise exception for errors, return warnings
        """
        errors, warnings = self.__validate_data(well_len, reservoir_perm)

        if errors:
            numbered_errors = [f"{i+1}. {error}" for i, error in enumerate(errors)]
            raise ValueError("\n".join(numbered_errors))

        if warnings:
            warnings = [f"{i+1}. {warning}" for i, warning in enumerate(warnings)]

        return warnings

    def to_dict(self) -> dict:
        """Возвращает словарь с простыми типами данных (не требуется рекурсия)"""
        return {
            "len_p": self.len_p,
            "len_m": self.len_m,
            "width": self.width,
            "perm": self.perm,
            "well_cross_coord": self.well_cross_coord,
        }

    def __validate_data(
        self, well_len: float = None, reservoir_perm: float = None
    ) -> Tuple[List[str], List[str]]:
        """Validate all fields and raise ValueError if any validation fails"""
        errors = []
        warnings = []

        if self.len_p is None:
            errors.append(f"Length Plus (m) is required")
        elif self.len_p <= 0:
            errors.append("Length Plus (m) should be positive number")

        if self.len_m is None:
            errors.append("Length Minus (m) is required")
        elif self.len_m <= 0:
            errors.append("Length Minus (m) should be positive number")

        if self.width is None:
            errors.append("Width (mm) is required")
        elif self.width <= 0:
            errors.append("Width (mm) should be positive number")

        if self.perm is None:
            errors.append("Permeability (D) is required")
        elif self.perm <= 0:
            errors.append("Permeability (D) should be positive number")

        if self.well_cross_coord is None:
            errors.append("Well cross depth (m) is required")
        elif self.well_cross_coord < 0:
            errors.append("Well cross depth (m) should be non-negative number")
        elif well_len is not None and self.well_cross_coord > well_len:
            errors.append(f"Well cross depth (m) should be inside well [0, {well_len}]")

        # New warning: fracture perm < reservoir perm
        if (
            reservoir_perm is not None
            and self.perm is not None
            and self.perm > 0
            and self.perm < reservoir_perm
        ):
            warnings.append(
                f"Fracture permeability ({self.perm} D) is less than reservoir permeability ({reservoir_perm} D)"
            )

        return errors, warnings

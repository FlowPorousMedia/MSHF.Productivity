from typing import List, Tuple

from src.app.i18n import _
from src.core.models.init_data.field_names.fract_initial_field_names import (
    FracInitFieldNames,
)
from src.core.models.init_data.field_names.well_initial_field_names import (
    WellInitFieldNames,
)
from src.core.services.data_validation_helper import DataValidationHelper


class FractInitialData:
    def __init__(self):
        self.len_p: float = None
        self.len_m: float = None
        self.width: float = None
        self.perm: float = None
        self.well_cross_coord: float = None

    def validate_and_raise(
        self,
        well_len: float = None,
        reservoir_perm: float = None,
        reservoir_rad: float = None,
    ) -> List[str]:
        """
        Validate and raise exception for errors, return warnings
        """
        errors, warnings = self.__validate_data(well_len, reservoir_perm, reservoir_rad)

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
        self,
        well_len: float,
        reservoir_perm: float,
        reservoir_rad: float,
    ) -> Tuple[List[str], List[str]]:
        """Validate all fields and raise ValueError if any validation fails"""
        errors = []
        warnings = []

        DataValidationHelper.validate_field(
            self.len_p,
            FracInitFieldNames.LENGTH_PLUS.value,
            0.0,
            reservoir_rad,
            errors,
            False,
            False,
        )
        DataValidationHelper.validate_field(
            self.len_m,
            FracInitFieldNames.LENGTH_MINUS.value,
            0.0,
            reservoir_rad,
            errors,
            False,
            False,
        )
        DataValidationHelper.validate_field(
            self.width, FracInitFieldNames.WIDTH, 0.0, 200, errors, False, True
        )
        DataValidationHelper.validate_field(
            self.perm,
            FracInitFieldNames.PERMEABILITY.value,
            0.0,
            None,
            errors,
            False,
            True,
        )
        DataValidationHelper.validate_field(
            self.well_cross_coord,
            FracInitFieldNames.WELL_CROSS.value,
            0.0,
            well_len,
            errors,
            True,
            True,
            f" Well {WellInitFieldNames.L.value}",
        )

        # warnings
        __, max_warn = DataValidationHelper.warn_field(
            self.perm, None, reservoir_perm, min_inclusive=True, max_inclusive=True
        )

        if max_warn:
            warnings.append(
                _(
                    "Fracture permeability ({fract_perm} D) is less than reservoir permeability ({reservoir_perm} D)"
                ).format(fract_perm=self.perm, reservoir_perm=reservoir_perm)
            )

        return errors, warnings

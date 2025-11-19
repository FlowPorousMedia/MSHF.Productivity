from typing import List, Optional, Tuple

from src.app.i18n import _


class DataValidationHelper:
    @staticmethod
    def validate_field(
        value: Optional[float],
        field_name: str,
        min_val: Optional[float],
        max_val: Optional[float],
        messages: List[str],
        min_inclusive: bool = True,
        max_inclusive: bool = True,
        description: str = None,
        required: bool = True,
    ) -> None:
        """
        Validate that a value is within specified range with configurable inclusivity.

        Args:
            value: Value to validate
            field_name: Name of the field for error messages
            min_val: Minimum value (None for no lower bound)
            max_val: Maximum value (None for no upper bound)
            errors: List to append errors to
            min_inclusive: Whether lower bound is inclusive [ or exclusive (
            max_inclusive: Whether upper bound is inclusive ] or exclusive )
        """
        if value is None:
            if required:
                messages.append(f"{field_name} is required")
            return

        str_descrp = f" ({description})" if description else ""

        # Validate lower bound if provided
        if min_val is not None:
            if min_inclusive:
                if value < min_val:
                    messages.append(
                        _(
                            "{field_name} should be at least {min_val}{str_descrp}"
                        ).format(field_name, min_val, str_descrp)
                    )
            else:
                if value <= min_val:
                    messages.append(
                        _(
                            "{field_name} should be greater than {min_val}{str_descrp}"
                        ).format(field_name, min_val, str_descrp)
                    )

        # Validate upper bound if provided
        if max_val is not None:
            if max_inclusive:
                if value > max_val:
                    messages.append(
                        _(
                            "{field_name} should be at most {max_val}{str_descrp}"
                        ).format(field_name, max_val, str_descrp)
                    )
            else:
                if value >= max_val:
                    messages.append(
                        _(
                            "{field_name} should be less than {max_val}{str_descrp}"
                        ).format(field_name, max_val, str_descrp)
                    )

    @staticmethod
    def warn_field(
        value: Optional[float],
        min_val: Optional[float],
        max_val: Optional[float],
        min_inclusive: bool = True,
        max_inclusive: bool = True,
    ) -> Tuple[bool, bool]:
        """
        Check if value is outside recommended bounds and return warning flags.

        Returns:
            Tuple[bool, bool]: (is_below_min, is_above_max) warning flags
        """
        if value is None:
            return (False, False)

        min_warning = False
        max_warning = False

        # Check lower bound warning
        if min_val is not None:
            if min_inclusive:
                min_warning = value < min_val
            else:
                min_warning = value <= min_val

        # Check upper bound warning
        if max_val is not None:
            if max_inclusive:
                max_warning = value > max_val
            else:
                max_warning = value >= max_val

        return (min_warning, max_warning)

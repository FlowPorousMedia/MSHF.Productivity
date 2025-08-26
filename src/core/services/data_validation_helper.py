from typing import List, Optional


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
            messages.append(f"{field_name} is required")
            return

        # Validate lower bound if provided
        if min_val is not None:
            if min_inclusive:
                if value < min_val:
                    messages.append(f"{field_name} should be at least {min_val}")
            else:
                if value <= min_val:
                    messages.append(f"{field_name} should be greater than {min_val}")

        # Validate upper bound if provided
        if max_val is not None:
            if max_inclusive:
                if value > max_val:
                    messages.append(f"{field_name} should be at most {max_val}")
            else:
                if value >= max_val:
                    messages.append(f"{field_name} should be less than {max_val}")

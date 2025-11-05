from enum import Enum


class LogCategory(str, Enum):
    CALCULATION = "calculation"
    SYSTEM = "system"
    UI = "ui"
    CHECK_DATA = "check_data"

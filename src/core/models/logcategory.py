from enum import Enum


class LogCategory(str, Enum):
    CALCULATION = "CALCULATION"
    SYSTEM = "SYSTEM"
    UI = "UI"
    CHECK_DATA = "CHECK_DATA"

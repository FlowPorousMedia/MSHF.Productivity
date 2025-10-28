from enum import Enum


class LogCategory(str, Enum):
    CALCULATION = "calculation"
    SYSTEM = "system"
    UI = "ui"
    NETWORK = "network"

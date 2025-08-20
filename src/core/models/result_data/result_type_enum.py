from enum import Enum


class ResultTypeEnum(Enum):
    SIMPLE = 0  # simple calc for given values
    PARAMETRIC = 1  # loop over one param
    MAP = 2  # loop over two params

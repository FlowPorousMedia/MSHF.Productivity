from typing import Tuple
from src.core.models.init_data.initial_data import InitialData


def calc_lm_lp(
    init_data: InitialData, fract_index: int, account_rc: bool
) -> Tuple[float, float]:
    """
    Calculate half distance to left and right fractures.
    If current fracture is edge then half distance is equal to reservoir radius
    """
    n = len(init_data.fractures)
    if fract_index < 0 or fract_index >= n:
        raise IndexError(f"Fract Index '{fract_index+1}' is out of bounds [1, {n}]")

    rc = init_data.reservoir.rc if account_rc else 0.0
    yf_current = init_data.fractures[fract_index].well_cross_coord
    if fract_index == 0:
        dl = yf_current - 0.0 # distance from well begin till fracture
        lm = rc + dl
    else:
        yf_left = init_data.fractures[fract_index - 1].well_cross_coord
        lm = (yf_current - yf_left) / 2.0
    if fract_index == n - 1:
        dl = init_data.well.L - yf_current
        lp = rc + dl
    else:
        yf_right = init_data.fractures[fract_index + 1].well_cross_coord
        lp = (yf_right - yf_current) / 2.0
    return [lm, lp]

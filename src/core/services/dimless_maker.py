from typing import Tuple
from src.core.models.characteristic_data import CharacteristicData
from src.core.models.init_data.initial_data import InitialData
from src.core.models.input_data.fract_input_data import FractInputData
from src.core.models.input_data.input_data import InputData
from src.core.models.input_data.res_input_data import ReservoirInputData
from src.core.models.input_data.well_input_data import WellInputData
from src.core.services.dimless_converter import DimlessConverter


# def make_dimless(init_data: InitialData) -> Tuple[CharacteristicData, InputData]:
#     char_data = CharacteristicData()
#     char_data.x0 = init_data.reservoir.rc
#     char_data.pw = init_data.well.pw
#     char_data.pr = init_data.reservoir.pr
#     char_data.mu = init_data.fluid.mu
#     char_data.perm = init_data.reservoir.perm
#     input_data = __get_dimless_data(init_data, char_data)

#     return [char_data, input_data]


# def __get_dimless_data(
#     init_data: InitialData, char_data: CharacteristicData
# ) -> InputData:
#     result = InputData()

#     dim_conv = DimlessConverter(char_data)

#     for fract in init_data.fractures:
#         dimless_frac = FractInputData()
#         dimless_frac.len_m = dim_conv.make_dimless_geom(fract.len_m)
#         dimless_frac.len_p = dim_conv.make_dimless_geom(fract.len_p)
#         dimless_frac.width = dim_conv.make_dimless_geom(fract.width)
#         dimless_frac.yf = dim_conv.make_dimless_geom(fract.well_cross_coord)
#         dimless_frac.perm = dim_conv.make_dimless_perm(fract.perm)

#         result.fractures.append(dimless_frac)

#     well = WellInputData()
#     well.L = dim_conv.make_dimless_geom(init_data.well.L)
#     well.rw = dim_conv.make_dimless_geom(init_data.well.rw)
#     well.is_perforated = init_data.well.is_perforated
#     result.well = well

#     reservoir = ReservoirInputData()
#     reservoir.H = dim_conv.make_dimless_geom(init_data.reservoir.H)
#     result.reservoir = reservoir

#     return result

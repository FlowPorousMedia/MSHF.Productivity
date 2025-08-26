from typing import Any, Dict, List

from pydantic import ValidationError

from src.app.models.message_type import MessageType
from src.app.models.parametric_settings import ParametricSettings
from src.app.models.result import Result
from src.app.models.result_details import ResultDetails
from src.core.models.init_data.calc_over_param import CalcOverParam
from src.core.models.init_data.calc_settings import CalcSettings
from src.core.models.init_data.init_settings import InitialSettings
from src.core.models.init_data.initial_data import InitialData
from src.core.models.init_data.fract_initial_data import FractInitialData
from src.core.models.init_data.models_enum import ModelsEnum
from src.core.models.init_data.reservoir_initial_data import ReservoirInitialData
from src.core.models.init_data.well_initial_data import WellInitialData
from src.core.models.init_data.fluid_initial_data import FluidInitialData

from src.core.models.result_data.calc_model import CalcModel
from src.core.models.result_data.result_type_enum import ResultTypeEnum
from src.core.services.measurement_converter import MeasurementConverter


def make_init_data(
    fracture_data: List[Dict[str, Any]],
    well_data: Dict[str, Any],
    reservoir_data: Dict[str, Any],
    fluid_data: Dict[str, Any],
    calc_models,
    setts: ParametricSettings,
) -> Result:
    result = Result()

    data = InitialData()

    if fracture_data:
        for i, frac in enumerate(fracture_data):
            # Handle potential missing values
            try:
                fracture = FractInitialData()
                fracture.len_p = frac.get("length_plus")
                fracture.len_m = frac.get("length_minus")
                fracture.width = MeasurementConverter.convert_mm_to_m(frac.get("width"))
                fracture.perm = MeasurementConverter.convert_D_to_m2(
                    frac.get("permeability")
                )
                fracture.well_cross_coord = frac.get("well_cross")
                # Validate the fracture data
                fracture.validate_and_raise()
                data.fractures.append(fracture)
            except ValueError as e:
                result.success = False
                result.data = None
                result.details = ResultDetails()
                result.details.tp = MessageType.ERROR
                result.details.title = "Invalid fracture data"
                result.details.message = (
                    f"Please, set correct value for fracture {i+1}:\n {str(e)}"
                )
                return result

    # well data
    well = WellInitialData()
    well.L = well_data.get("length", 0)
    well.rw = MeasurementConverter.convert_cm_to_m(well_data.get("radius", 0))
    well.pw = MeasurementConverter.convert_atm_to_Pa(well_data.get("pressure", 0))
    well.is_perforated = bool(well_data.get("perforated", False))
    data.well = well

    # reservoir data
    reservoir = ReservoirInitialData()
    reservoir.H = reservoir_data.get("height", 0)
    reservoir.perm = MeasurementConverter.convert_D_to_m2(
        reservoir_data.get("permeability", 0)
    )
    reservoir.pr = MeasurementConverter.convert_atm_to_Pa(
        reservoir_data.get("pressure", 0)
    )
    reservoir.rc = reservoir_data.get("radius", 0)
    data.reservoir = reservoir

    # fluid data
    fluid = FluidInitialData()
    fluid.mu = MeasurementConverter.convert_from_cP_to_PaSec(
        fluid_data.get("viscosity", 0)
    )
    data.fluid = fluid

    # settings
    data.settings = __make_settings(calc_models, setts)

    result.success = True
    result.data = data

    return result


def __make_settings(calc_models, setts: ParametricSettings):
    calc_settings = CalcSettings()
    calc_settings.calc_type = setts.calc_type

    if setts.calc_type == ResultTypeEnum.PARAMETRIC:
        calc_settings.calc_over_param1 = CalcOverParam()
        calc_settings.calc_over_param1.param_type = setts.tp
        calc_settings.calc_over_param1.start_value = setts.start
        calc_settings.calc_over_param1.end_value = setts.end
        calc_settings.calc_over_param1.point_count = setts.point_count

    result = InitialSettings()
    result.calc_settings = calc_settings
    for an_model in calc_models:
        model = CalcModel()
        model.tp = ModelsEnum(an_model["id"])
        model.name = an_model["name"]
        result.calc_models.append(model)

    return result

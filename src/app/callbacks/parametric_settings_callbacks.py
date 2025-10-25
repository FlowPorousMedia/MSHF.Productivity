from dash import Input, Output, State
from dash.exceptions import PreventUpdate

from src.core.models.init_data.calc_over_param_enum import CalcParamTypeEnum


def register(app):
    """Register all callbacks related to settings panel"""

    @app.callback(
        [
            Output("parameter-dropdown", "disabled"),
            Output("start-input", "disabled"),
            Output("end-input", "disabled"),
            Output("point-count-input", "disabled"),
        ],
        Input("parametric-plot-checkbox", "value"),
    )
    def toggle_parametric_inputs(checked):
        # Enable inputs when checkbox is checked, disable otherwise
        state = not checked if checked is not None else True
        return [state] * 4  # Return disabled state for all four components

    @app.callback(
        [
            Output("start-input", "value"),
            Output("start-input", "min"),
            Output("start-input", "max"),
            Output("start-input", "step"),
            Output("end-input", "value"),
            Output("end-input", "min"),
            Output("end-input", "max"),
            Output("end-input", "step"),
        ],
        Input("parameter-dropdown", "value"),
    )
    def update_start_end(param_value):
        if param_value == CalcParamTypeEnum.FRACT_COUNT.value:
            return 2, 2, 20, 1, False, 10, 2, 100, 1, False
        elif param_value == CalcParamTypeEnum.RES_RAD.value:
            return 100, 10, 1000, 10, False, 500, 10, 5000, 10, False
        elif param_value == CalcParamTypeEnum.WELL_LEN.value:
            return 50, 10, 200, 1, False, 100, 20, 500, 5, False
        elif param_value == CalcParamTypeEnum.FRACT_PERM.value:
            return 1, 0.1, 100, 0.1, False, 10, 0.1, 1000, 0.1, False
        elif param_value == CalcParamTypeEnum.FRACT_LEN.value:
            return 10, 5, 200, 1, False, 50, 5, 500, 1, False
        elif param_value == CalcParamTypeEnum.FRACT_WIDTH.value:
            return 0.001, 0.0001, 0.01, 0.0001, False, 0.005, 0.0001, 0.1, 0.0001, False
        elif param_value == CalcParamTypeEnum.RES_HEIGTH.value:
            return 10, 1, 100, 1, False, 50, 1, 500, 1, False

        # fallback: выключить инпуты
        return 0, 0, 0, 1, True, 0, 0, 0, 1, True

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
            return 2, 2, 20, 1, 10, 2, 100, 1
        elif param_value == CalcParamTypeEnum.RES_RAD.value:
            return 100, 10, 1000, 10, 500, 10, 5000, 10
        elif param_value == CalcParamTypeEnum.WELL_LEN.value:
            return 1000, 200, 10000, 50, 2000, 200, 10000, 50
        elif param_value == CalcParamTypeEnum.FRACT_PERM.value:
            return 1, 0.01, 1e6, 10, 1e4, 1, 1e6, 10
        elif param_value == CalcParamTypeEnum.FRACT_LEN.value:
            return 10, 5, 190, 1, 150, 10, 190, 1
        elif param_value == CalcParamTypeEnum.FRACT_WIDTH.value:
            return 1, 0.1, 20, 1, 5, 0.1, 20, 1
        elif param_value == CalcParamTypeEnum.RES_HEIGTH.value:
            return 10, 1, 100, 10, 50, 1, 1000, 10

        # fallback: выключить инпуты
        return 0, 0, 0, 1, True, 0, 0, 0, 1, True

# src/app/callbacks/calculate_button_callbacks.py
from dash import Input, Output, State, no_update, exceptions
from src.app.models.parametric_settings import ParametricSettings
from src.app.models.result import Result
from src.app.models.result_details import ResultDetails
from src.app.services import init_data_reader
from src.app.services.calc_preprocessor import CalcPreprocessor
from src.core.models.init_data.calc_over_param_enum import CalcParamTypeEnum
from src.core.models.init_data.initial_data import InitialData
from src.core.models.loglevel import LogLevel
from src.core.models.main_data import MainData
from src.core.models.result_data.result_type_enum import ResultTypeEnum
from src.core.services.main_solver import MainSolver


def register(app):
    @app.callback(
        Output("calculate-button", "disabled"),
        Output("show-logs-button", "disabled"),
        Input("app-state", "data"),
    )
    def update_buttons(state):
        if state == "init":
            return False, True
        if state == "running":
            return True, True
        if state == "idle":
            return False, False
        return no_update, no_update

    # 1️⃣ click "Рассчитать"
    @app.callback(
        Output("message-request", "data"),
        Output("app-state", "data", allow_duplicate=True),
        Input("calculate-button", "n_clicks"),
        State("app-state", "data"),
        State("well-params-store", "data"),
        State("reservoir-params-store", "data"),
        State("fluid-params-store", "data"),
        State("fracture-table", "data"),
        prevent_initial_call=True,
    )
    def handle_calc_request(n_clicks, state, well, reservoir, fluid, fracture):
        if not n_clicks or state not in ("init", "idle"):
            raise exceptions.PreventUpdate

        if CalcPreprocessor.is_default_params(well, reservoir, fluid, fracture):
            data = {
                "context": "confirm_calc_start",
                "title": "Default Parameters Notification",
                "message": "You are about to run the calculation with default parameters. Continue?",
                "type": LogLevel.INFO.name,
                "buttons": ["Yes", "No"],
            }
            return data, "confirming"

        print("✅ No confirmation needed, starting calculation")
        return no_update, "running"

    # 2️⃣ handle Yes/No
    @app.callback(
        Output("app-state", "data", allow_duplicate=True),  # ← добавлено
        Input("message-response", "data"),
        State("app-state", "data"),
        prevent_initial_call=True,
    )
    def handle_dialog_response(msg_response, state):
        if not msg_response or msg_response.get("context") != "confirm_calc_start":
            raise exceptions.PreventUpdate
        return "running" if msg_response.get("response") == "Yes" else "idle"

    # 3️⃣ run calculation
    @app.callback(
        Output("log-store", "data"),
        Output("solver-result-store", "data"),
        Input("app-state", "data"),
        State("analytical-models-gridtable", "selectedRows"),
        State("semianalytical-models-gridtable", "selectedRows"),
        State("fracture-table", "data"),
        State("well-params-store", "data"),
        State("reservoir-params-store", "data"),
        State("fluid-params-store", "data"),
        State("parametric-plot-checkbox", "value"),
        State("parameter-dropdown", "value"),
        State("start-input", "value"),
        State("end-input", "value"),
        State("point-count-input", "value"),
        State("log-store", "data"),
        prevent_initial_call=True,
    )
    def calculate_results(
        app_state,
        analytical_selected_models,
        semianalytical_selected_models,
        fracture_data,
        well_data,
        reservoir_data,
        fluid_data,
        parametric_checked,
        parameter,
        start_val,
        end_val,
        point_count,
        logs,
    ):
        if app_state != "running":
            raise exceptions.PreventUpdate

        logs = logs or []
        if not analytical_selected_models and not semianalytical_selected_models:
            return logs, {
                "message": "No selected models",
                "type": LogLevel.WARNING.name,
            }

        setts = ParametricSettings()
        if parametric_checked:
            try:
                setts.start = float(start_val)
                setts.end = float(end_val)
                setts.point_count = int(point_count)
                setts.tp = CalcParamTypeEnum(parameter)
                setts.calc_type = ResultTypeEnum.PARAMETRIC
            except (TypeError, ValueError):
                return logs, {
                    "message": "Invalid parametric settings",
                    "type": LogLevel.ERROR.name,
                }
            if setts.point_count < 2 or setts.start >= setts.end:
                return logs, {
                    "message": "Invalid parametric settings",
                    "type": LogLevel.ERROR.name,
                }

        calc_models = (analytical_selected_models or []) + (
            semianalytical_selected_models or []
        )
        result_init_data: Result = init_data_reader.make_init_data(
            fracture_data, well_data, reservoir_data, fluid_data, calc_models, setts
        )

        if not result_init_data.success:
            details: ResultDetails = result_init_data.details
            return logs, {"message": details.message, "type": LogLevel.ERROR.name}

        init_data: InitialData = result_init_data.data
        solver = MainSolver()
        result: MainData = solver.calc(init_data, logs)
        return logs, result.to_dict()

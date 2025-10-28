from dash import Input, Output, State, no_update

from src.app.models.parametric_settings import ParametricSettings
from src.app.models.result import Result
from src.app.models.result_details import ResultDetails
from src.app.services import init_data_reader
from src.core.models.init_data.calc_over_param_enum import CalcParamTypeEnum
from src.core.models.init_data.initial_data import InitialData
from src.core.models.logcategory import LogCategory
from src.core.models.loglevel import LogLevel
from src.core.models.main_data import MainData
from src.core.models.result_data.result_type_enum import ResultTypeEnum
from src.core.services.log_worker import make_log
from src.core.services.main_solver import MainSolver


def register(app):
    # Callback for calculation - returns only solver result
    @app.callback(
        Output("log-store", "data"),
        Output("solver-result-store", "data"),
        Output("open-msg-dialog", "data", allow_duplicate=True),
        Output("calc-state", "data"),
        Input("calculate-button", "n_clicks"),
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
        n_clicks,
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
        yield no_update, no_update, no_update, "running"

        logs = logs or []

        if analytical_selected_models is None and (
            semianalytical_selected_models is None
        ):
            logs.append(
                make_log(
                    "No selected models",
                    LogLevel.WARNING,
                    LogCategory.CALCULATION,
                    True,
                )
            )

        if n_clicks is None:
            yield no_update, no_update, no_update, "idle"
            return

        setts = ParametricSettings()
        if parametric_checked:
            try:
                start_val = float(start_val)
                end_val = float(end_val)
                point_count = int(point_count)

                setts.start = start_val
                setts.end = end_val
                setts.point_count = point_count
                setts.tp = CalcParamTypeEnum(parameter)
                setts.calc_type = ResultTypeEnum.PARAMETRIC
            except ValueError:
                print("Invalid parametric settings: non-numeric value")
                yield no_update, no_update, no_update, "idle"
                return

            if point_count < 2:
                print("Point count must be at least 2")
                yield no_update, no_update, no_update, "idle"
                return

            if start_val >= end_val:
                print("Start must be less than end")
                yield no_update, no_update, no_update, "idle"
                return

        calc_models = analytical_selected_models + semianalytical_selected_models

        result_init_data: Result = init_data_reader.make_init_data(
            fracture_data, well_data, reservoir_data, fluid_data, calc_models, setts
        )

        if not result_init_data.success:
            details: ResultDetails = result_init_data.details
            yield (
                no_update,
                no_update,
                {
                    "title": details.title,
                    "message": details.message,
                    "type": (
                        details.tp.name
                        if hasattr(details.tp, "name")
                        else str(details.tp)
                    ),
                    "buttons": ["OK"],
                },
                "idle",
            )
            return

        init_data: InitialData = result_init_data.data

        M0 = init_data.get_M(0)
        print(f"M = {M0}")

        solver = MainSolver()
        result: MainData = solver.calc(init_data)

        yield logs, result.to_dict(), no_update, "idle"

    @app.callback(
        Output("calculate-button", "disabled"),
        Output("show-logs-button", "disabled"),
        Input("calc-state", "data"),
    )
    def update_buttons(state):
        if state == "init":  # старт
            return False, True  # calc включена, logs выключена
        elif state == "running":
            return True, True  # обе выключены
        elif state == "idle":
            return False, False  # обе включены
        return no_update, no_update

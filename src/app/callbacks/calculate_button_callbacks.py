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
    # --- Кнопки управляются только состоянием calc-state ---
    @app.callback(
        Output("calculate-button", "disabled"),
        Output("show-logs-button", "disabled"),
        Input("calc-state", "data"),
    )
    def update_buttons(state):
        if state == "init":  # старт
            return False, True  # calc включена, logs выключена
        if state == "running":  # расчёт идёт
            return True, True  # обе выключены
        if state == "idle":  # расчёт был завершён хотя бы раз
            return False, False  # обе включены
        return no_update, no_update

    # --- Колбэк A: клик -> сразу переводим в running ---
    @app.callback(
        Output("calc-state", "data"),
        Input("calculate-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def start_calculation(n_clicks):
        # моментально блокируем обе кнопки через состояние
        return "running"

    # --- Колбэк B: если running -> выполняем расчёт, отдаём результат и ставим idle ---
    @app.callback(
        Output("log-store", "data"),
        Output("solver-result-store", "data"),
        Output("open-msg-dialog", "data", allow_duplicate=True),
        Input("calc-state", "data"),
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
        calc_state,
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
        # Запускаем расчёт ТОЛЬКО когда состояние "running"
        if calc_state != "running":
            return no_update, no_update, no_update

        logs = logs or []

        if not analytical_selected_models and not semianalytical_selected_models:
            return (
                logs,
                no_update,
                {
                    "title": "Calculation Warning",
                    "message": "No selected models",
                    "type": LogLevel.WARNING.name,
                    "buttons": ["OK"],
                },
            )

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
            except (TypeError, ValueError):
                # ошибка ввода — показать диалог и разблокировать кнопки
                return (
                    logs,
                    no_update,
                    {
                        "title": "Invalid parametric settings",
                        "message": "Start/End must be numbers, Point count must be integer.",
                        "type": "ERROR",
                        "buttons": ["OK"],
                    },
                )

            if point_count < 2 or start_val >= end_val:
                return (
                    logs,
                    no_update,
                    {
                        "title": "Invalid parametric settings",
                        "message": "Point count ≥ 2 and Start < End are required.",
                        "type": "ERROR",
                        "buttons": ["OK"],
                    },
                )

        calc_models = (analytical_selected_models or []) + (
            semianalytical_selected_models or []
        )

        result_init_data: Result = init_data_reader.make_init_data(
            fracture_data, well_data, reservoir_data, fluid_data, calc_models, setts
        )

        if not result_init_data.success:
            details: ResultDetails = result_init_data.details
            return (
                logs,
                no_update,
                {
                    "title": details.title,
                    "message": details.message,
                    "type": getattr(details.tp, "name", str(details.tp)),
                    "buttons": ["OK"],
                },
            )

        init_data: InitialData = result_init_data.data
        solver = MainSolver()
        result: MainData = solver.calc(init_data)

        # УСПЕХ: вернём логи, результат и разблокируем кнопки
        return logs, result.to_dict(), no_update

    @app.callback(
        Output("calc-state", "data", allow_duplicate=True),
        Input("solver-result-store", "data"),
        Input("open-msg-dialog", "data"),
        prevent_initial_call=True,
    )
    def finish_calculation(result_data, dialog_data):
        # если появились результаты ИЛИ всплыло сообщение об ошибке — отпускаем кнопки
        if result_data is not None or dialog_data is not None:
            return "idle"
        return no_update

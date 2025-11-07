from dash import Input, Output, State, no_update, exceptions, html
from src.app.models.parametric_settings import ParametricSettings
from src.app.models.result import Result
from src.app.models.result_details import ResultDetails
from src.app.services import init_data_reader
from src.app.services.calc_preprocessor import CalcPreprocessor
from src.core.models.init_data.calc_over_param_enum import CalcParamTypeEnum
from src.core.models.init_data.initial_data import InitialData
from src.core.models.logcategory import LogCategory
from src.core.models.loglevel import LogLevel
from src.core.models.main_data import MainData
from src.core.models.result_data.result_type_enum import ResultTypeEnum
from src.core.services.log_worker import make_log
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

    # click "Calculate" - упрощенная версия
    @app.callback(
        Output("message-request", "data", allow_duplicate=True),
        Output("app-state", "data", allow_duplicate=True),
        Output("log-store", "data", allow_duplicate=True),
        Output("status-text", "children", allow_duplicate=True),
        Output("progress-wrapper", "style", allow_duplicate=True),
        Input("calculate-button", "n_clicks"),
        State("app-state", "data"),
        State("well-params-store", "data"),
        State("reservoir-params-store", "data"),
        State("fluid-params-store", "data"),
        State("fracture-table", "data"),
        State("log-store", "data"),
        prevent_initial_call=True,
    )
    def handle_calc_request(n_clicks, state, well, reservoir, fluid, fracture, logs):
        logs = logs or []

        if not n_clicks or state not in ("init", "idle"):
            raise exceptions.PreventUpdate

        # Сразу показываем прогресс бар
        progress_style = {
            "display": "flex",
            "flex": "1",
            "alignItems": "center",
            "marginLeft": "10px",
        }
        status_text = "Preparing for calculation..."

        if CalcPreprocessor.is_default_params(well, reservoir, fluid, fracture, logs):
            data = {
                "context": "confirm_calc_start",
                "title": "Default Parameters Notification",
                "message": "You are about to run the calculation with default parameters. Continue?",
                "type": LogLevel.INFO.name,
                "buttons": ["Yes", "No"],
            }
            return data, "confirming", logs, status_text, progress_style

        logs.append(
            make_log(
                "No confirmation needed, starting calculation",
                LogLevel.DEBUG,
                LogCategory.CALCULATION,
                False,
            )
        )
        return no_update, "running", logs, status_text, progress_style

    # handle Yes/No
    @app.callback(
        Output("app-state", "data", allow_duplicate=True),
        Output("status-text", "children", allow_duplicate=True),
        Output("progress-wrapper", "style", allow_duplicate=True),
        Input("message-response", "data"),
        State("app-state", "data"),
        prevent_initial_call=True,
    )
    def handle_dialog_response(msg_response, state):
        if not msg_response or msg_response.get("context") != "confirm_calc_start":
            raise exceptions.PreventUpdate

        if msg_response.get("response") == "Yes":
            progress_style = {
                "display": "flex",
                "flex": "1",
                "alignItems": "center",
                "marginLeft": "10px",
            }
            return "running", "Starting calculation...", progress_style
        else:
            return "idle", "Calculation cancelled", {"display": "none"}

    # run calculation - основной background callback
    @app.callback(
        output=[
            Output("log-store", "data", allow_duplicate=True),
            Output("solver-result-store", "data", allow_duplicate=True),
            Output("status-text", "children", allow_duplicate=True),
            Output("calculation-progress", "value", allow_duplicate=True),
            Output("progress-percent", "children", allow_duplicate=True),
            Output("progress-wrapper", "style", allow_duplicate=True),
            Output("app-state", "data", allow_duplicate=True),
        ],
        inputs=[Input("app-state", "data")],  # ← меняем триггер на app-state
        state=[
            State("calculate-button", "n_clicks"),
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
        ],
        background=True,
        running=[
            (Output("calculate-button", "disabled"), True, False),
            (Output("show-logs-button", "disabled"), True, False),
        ],
        progress=[
            Output("calculation-progress", "value"),
            Output("progress-percent", "children"),
            Output("status-text", "children"),
        ],
        prevent_initial_call=True,
    )
    def calculate_results(
        set_progress,
        app_state,  # ← теперь это основной input
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
        # Запускаем расчет только когда состояние "running"
        if app_state != "running":
            return (
                logs or [],
                no_update,
                "Готов",
                0,
                "0%",
                {"display": "none"},
                app_state,
            )

        logs = logs or []

        # Этап 1: Проверка моделей
        set_progress((10, "10%", "Checking selected models..."))
        if not analytical_selected_models and not semianalytical_selected_models:
            logs.append(
                make_log(
                    "No models selected",
                    LogLevel.WARNING,
                    LogCategory.CALCULATION,
                    False,
                )
            )
            return (
                logs,
                {"message": "No selected models", "type": LogLevel.WARNING.name},
                "Warning: no models selected",
                0,
                "0%",
                {"display": "none"},
                "idle",
            )

        # Этап 2: Настройка параметров
        set_progress((20, "20%", "Configuring calculation parameters..."))
        setts = ParametricSettings()
        if parametric_checked:
            try:
                setts.start = float(start_val)
                setts.end = float(end_val)
                setts.point_count = int(point_count)
                setts.tp = CalcParamTypeEnum(parameter)
                setts.calc_type = ResultTypeEnum.PARAMETRIC
            except (TypeError, ValueError):
                logs.append(
                    make_log(
                        "Invalid parametric settings",
                        LogLevel.ERROR,
                        LogCategory.CALCULATION,
                        False,
                    )
                )
                return (
                    logs,
                    {
                        "message": "Invalid parametric settings",
                        "type": LogLevel.ERROR.name,
                    },
                    "Error: invalid calculation parameters",
                    0,
                    "0%",
                    {"display": "none"},
                    "idle",
                )

            if setts.point_count < 2 or setts.start >= setts.end:
                logs.append(
                    make_log(
                        "Invalid parametric range",
                        LogLevel.ERROR,
                        LogCategory.CALCULATION,
                        False,
                    )
                )
                return (
                    logs,
                    {
                        "message": "Invalid parametric settings",
                        "type": LogLevel.ERROR.name,
                    },
                    "Error: invalid parameter range",
                    0,
                    "0%",
                    {"display": "none"},
                    "idle",
                )

        # Этап 3: Подготовка данных
        set_progress((40, "40%", "Preparing data for calculation..."))
        calc_models = (analytical_selected_models or []) + (
            semianalytical_selected_models or []
        )

        # Этап 4: Чтение исходных данных
        set_progress((60, "60%", "Reading initial data..."))
        result_init_data: Result = init_data_reader.make_init_data(
            fracture_data, well_data, reservoir_data, fluid_data, calc_models, setts
        )

        if not result_init_data.success:
            details: ResultDetails = result_init_data.details
            logs.append(
                make_log(
                    f"Init data error: {details.message}",
                    LogLevel.ERROR,
                    LogCategory.CALCULATION,
                    False,
                )
            )
            return (
                logs,
                {"message": details.message, "type": LogLevel.ERROR.name},
                f"Data preparation error: {details.message}",
                0,
                "0%",
                {"display": "none"},
                "idle",
            )

        # Этап 5: Выполнение расчета
        set_progress((80, "80%", "Performing calculation..."))
        init_data: InitialData = result_init_data.data

        def update_solver_progress(progress, message):
            # set_progress((progress, f"{progress}%", message))
            overall_progress = 80 + (progress * 0.15)
            set_progress((overall_progress, f"{int(overall_progress)}%", message))

        solver = MainSolver()
        result: MainData = solver.calc(
            init_data, logs, progress_callback=update_solver_progress
        )

        # Завершение
        set_progress((100, "100%", "Finalizing calculation..."))

        return (
            logs,
            result.to_dict(),
            "Calculation completed successfully",
            100,
            "100%",
            {"display": "flex", "flex": "0 0 auto", "alignItems": "center"},
            "idle",
        )

    @app.callback(
        Output("graph-container", "children", allow_duplicate=True),
        Output("table-container", "children", allow_duplicate=True),
        Input("message-response", "data"),  # ← меняем триггер на ответ от диалога
        State("calculate-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def clear_containers(msg_response, n_clicks):
        if not n_clicks or not msg_response:
            raise exceptions.PreventUpdate

        # Очищаем только если пользователь нажал "Yes"
        if (
            msg_response.get("context") == "confirm_calc_start"
            and msg_response.get("response") == "Yes"
        ):
            empty_content = html.Div(
                [
                    html.Div(
                        [
                            html.I(className="bi bi-hourglass-split me-2"),
                            "Calculation in progress...",
                        ],
                        className="alert alert-info d-flex align-items-center",
                    ),
                ]
            )
            return empty_content, empty_content

        raise exceptions.PreventUpdate

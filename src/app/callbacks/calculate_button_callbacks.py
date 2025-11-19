from dash import Input, Output, State, no_update, exceptions, html
from src.app.i18n import _
from src.app.models.parametric_settings import ParametricSettings
from src.app.models.result import Result
from src.app.models.result_details import ResultDetails
from src.app.services import init_data_reader
from src.app.services.calc_preprocessor import CalcPreprocessor
from src.app.services.response_utils import make_response
from src.app.services.result_table_graph_helper import (
    get_calc_content,
    get_default_containers,
)
from src.core.models.init_data.calc_over_param_enum import CalcParamTypeEnum
from src.core.models.init_data.initial_data import InitialData
from src.core.models.logcategory import LogCategory
from src.core.models.message_level import MessageLevel
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
        status_text = _("Preparing for calculation...")

        if CalcPreprocessor.is_default_params(well, reservoir, fluid, fracture, logs):
            data = {
                "context": "confirm_calc_start",
                "title": _("Default Parameters Notification"),
                "message": _(
                    "You are about to run the calculation with default parameters. Continue?"
                ),
                "type": MessageLevel.INFO,
                "buttons": [
                    {"label": _("Yes"), "value": True},
                    {"label": _("No"), "value": False},
                ],
            }
            return data, "confirming", logs, status_text, progress_style

        logs.append(
            make_log(
                _("No confirmation needed, starting calculation"),
                MessageLevel.DEBUG,
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

        if msg_response.get("response") == "True":
            progress_style = {
                "display": "flex",
                "flex": "1",
                "alignItems": "center",
                "marginLeft": "10px",
            }
            return "running", _("Starting calculation..."), progress_style
        else:
            return "idle", _("Calculation cancelled"), {"display": "none"}

    # run calculation - основной background callback
    @app.callback(
        output=[
            Output("log-store", "data", allow_duplicate=True),
            Output("message-request", "data", allow_duplicate=True),
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
            return make_response(logs, state=app_state)

        logs = logs or []

        # Этап 1: Проверка моделей
        set_progress((10, "10%", _("Checking selected models...")))
        if not analytical_selected_models and not semianalytical_selected_models:
            message_body = _("No models selected")
            logs.append(
                make_log(
                    message_body,
                    MessageLevel.WARNING,
                    LogCategory.CALCULATION,
                    False,
                )
            )

            message = {
                "context": "calc_error_no_models",
                "title": message_body,
                "message": _(
                    "Please select at least one model before starting the calculation."
                ),
                "type": MessageLevel.WARNING.name,
                "buttons": [_("OK")],
            }

            return make_response(
                logs=logs,
                message=message,
                status_text=_("Warning: no models selected"),
                state="error",
            )

        # Этап 2: Настройка параметров
        set_progress((20, "20%", _("Configuring calculation parameters...")))
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
                        _("Invalid parametric settings"),
                        MessageLevel.ERROR,
                        LogCategory.CALCULATION,
                        False,
                    )
                )
                return (
                    logs,
                    {
                        "message": _("Invalid parametric settings"),
                        "type": MessageLevel.ERROR.label,
                    },
                    _("Error: invalid calculation parameters"),
                    0,
                    "0%",
                    {"display": "none"},
                    "error",
                )

            if setts.point_count < 2 or setts.start >= setts.end:
                logs.append(
                    make_log(
                        _("Invalid parametric range"),
                        MessageLevel.ERROR,
                        LogCategory.CALCULATION,
                        False,
                    )
                )
                return (
                    logs,
                    {
                        "message": _("Invalid parametric settings"),
                        "type": MessageLevel.ERROR.label,
                    },
                    _("Error: invalid parameter range"),
                    0,
                    "0%",
                    {"display": "none"},
                    "error",
                )

        # Этап 3: Подготовка данных
        set_progress((40, "40%", _("Preparing data for calculation...")))
        calc_models = (analytical_selected_models or []) + (
            semianalytical_selected_models or []
        )

        # Этап 4: Чтение исходных данных
        set_progress((60, "60%", _("Reading initial data...")))
        result_init_data: Result = init_data_reader.make_init_data(
            fracture_data, well_data, reservoir_data, fluid_data, calc_models, setts
        )

        if not result_init_data.success:
            details: ResultDetails = result_init_data.details
            logs.append(
                make_log(
                    _("Init data error: {message}").format(message=details.message),
                    MessageLevel.ERROR,
                    LogCategory.CALCULATION,
                    False,
                )
            )
            return (
                logs,
                {"message": details.message, "type": MessageLevel.ERROR},
                _("Data preparation error: {message}").format(message=details.message),
                0,
                "0%",
                {"display": "none"},
                "error",
            )

        # Этап 5: Выполнение расчета
        set_progress((80, "80%", _("Performing calculation...")))
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
        set_progress((100, "100%", _("Finalizing calculation...")))

        return (
            logs,
            no_update,
            result.to_dict(),
            _("Calculation completed successfully"),
            0,
            "",
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
            and msg_response.get("response") == "True"
        ):
            calc_content = get_calc_content()

            return calc_content, calc_content

        raise exceptions.PreventUpdate

    @app.callback(
        Output("graph-container", "children", allow_duplicate=True),
        Output("table-container", "children", allow_duplicate=True),
        Input("app-state", "data"),
        prevent_initial_call=True,
    )
    def update_main_display(state):
        if state == "init":
            return get_default_containers()

        elif state == "running":
            calc_content = get_calc_content()
            return calc_content, calc_content

        elif state == "error":
            # Ошибка → вернуть дефолт
            return get_default_containers()

        else:
            # idle — расчет завершён → оставить результат как есть
            raise exceptions.PreventUpdate

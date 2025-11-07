from dash import Input, Output, State, html, ctx
import dash_bootstrap_components as dbc

from src.core.models.logcategory import LogCategory
from src.core.models.loglevel import LogLevel


def register(app):
    @app.callback(
        Output("modal-logs", "is_open"),
        Input("show-logs-button", "n_clicks"),
        Input("close-logs-button", "n_clicks"),
        State("modal-logs", "is_open"),
    )
    def toggle_logs_modal(show_clicks, close_clicks, is_open):
        if show_clicks or close_clicks:
            return not is_open
        return is_open

    # Очистка логов
    @app.callback(
        Output("log-store", "data", allow_duplicate=True),
        Input("clear-logs-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def clear_logs(_):
        return []

    # Основной рендер логов
    @app.callback(
        Output("logs-body", "children"),
        Input("log-store", "data"),
        Input("filter-error", "outline"),
        Input("filter-warning", "outline"),
        Input("filter-info", "outline"),
        Input("logs-checklist", "value"),
        Input("logs-search", "value"),
    )
    def render_logs(
        logs, err_outline, warn_outline, info_outline, checklist, search_text
    ):
        if not logs:
            return html.Div("No logs yet.", className="text-muted fst-italic")

        # === Активные уровни ===
        active_levels = []
        if not err_outline:
            active_levels.append(LogLevel.ERROR.value)
        if not warn_outline:
            active_levels.append(LogLevel.WARNING.value)
        if not info_outline:
            active_levels.append(LogLevel.INFO.value)

        print(checklist)

        # Если отмечен "Show system logs" — добавляем DEBUG
        if "system" in checklist:
            active_levels.append(LogLevel.DEBUG.value)

        # === Категории ===
        if "calc" in checklist:
            allowed_categories = [LogCategory.CALCULATION.value]
        else:
            allowed_categories = [
                LogCategory.CALCULATION.value,
                LogCategory.UI.value,
                LogCategory.CHECK_DATA.value,
                LogCategory.SYSTEM.value,
            ]

        # === Фильтрация логов ===
        filtered = []
        search_text = (search_text or "").lower().strip()

        for log in logs:
            level = (
                log["level"].value
                if hasattr(log["level"], "value")
                else str(log["level"])
            )
            category = (
                log["category"].value
                if hasattr(log["category"], "value")
                else str(log["category"])
            )

            if level not in active_levels:
                print (f"{log} is not active")
                continue
            if category not in allowed_categories:
                print (f"{log} is not allowed category")
                continue
            if search_text and search_text not in log["message"].lower():
                continue

            filtered.append(log)

        if not filtered:
            return html.Div(
                "No logs match the filters.", className="text-muted fst-italic"
            )

        # === Визуализация ===
        def render_log_item(log):
            level = (
                log["level"].value
                if hasattr(log["level"], "value")
                else str(log["level"])
            )
            color_map = {
                "DEBUG": "secondary",
                "INFO": "info",
                "WARNING": "warning",
                "ERROR": "danger",
                "CRITICAL": "dark",
            }
            badge_color = color_map.get(level, "secondary")

            category = (
                log["category"].value
                if hasattr(log["category"], "value")
                else str(log["category"])
            )

            return dbc.Card(
                dbc.CardBody(
                    [
                        html.Small(
                            f"[{log['timestamp']}]", className="text-muted me-2"
                        ),
                        dbc.Badge(level, color=badge_color, className="me-2"),
                        html.Span(f"{category.upper()}: ", className="fw-semibold"),
                        html.Span(log["message"]),
                    ],
                    className="py-2",
                ),
                className="mb-1 shadow-sm border-0 bg-light",
            )

        return html.Div([render_log_item(log) for log in filtered])

    @app.callback(
        Output("filter-error", "outline"),
        Output("filter-warning", "outline"),
        Output("filter-info", "outline"),
        State("filter-error", "outline"),
        State("filter-warning", "outline"),
        State("filter-info", "outline"),
        Input("filter-error", "n_clicks"),
        Input("filter-warning", "n_clicks"),
        Input("filter-info", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_filter_buttons(err_outline, warn_outline, info_outline, *btn_clicks):
        trigger = ctx.triggered_id
        outlines = [err_outline, warn_outline, info_outline]

        mapping = {"filter-error": 0, "filter-warning": 1, "filter-info": 2}
        if trigger in mapping:
            idx = mapping[trigger]
            outlines[idx] = not outlines[idx]  # переключаем

        return outlines

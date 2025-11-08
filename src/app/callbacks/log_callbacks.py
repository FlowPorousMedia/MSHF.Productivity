import time
import dash
from dash import ALL, Input, Output, State, html, ctx, no_update

from src.app.services.log_item_worker import render_log_item
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
                continue
            if category not in allowed_categories:
                continue
            if search_text and search_text not in log["message"].lower():
                continue

            filtered.append(log)

        if not filtered:
            return html.Div(
                "No logs match the filters.", className="text-muted fst-italic"
            )

        return html.Div([render_log_item(log, search_text) for log in filtered])

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

    @app.callback(
        Output({"type": "copy-log", "index": ALL}, "children"),
        Output({"type": "copy-tooltip", "index": ALL}, "is_open"),
        Output("copy-tooltip-interval", "disabled"),
        Output("copy-tooltip-interval", "n_intervals"),
        Input({"type": "copy-log", "index": ALL}, "n_clicks"),
        Input("copy-tooltip-interval", "n_intervals"),
        State({"type": "copy-tooltip", "index": ALL}, "is_open"),
        prevent_initial_call=True,
    )
    def copy_icon_and_tooltip(n_clicks_list, tick, current_tooltips):
        n = len(n_clicks_list)
        default_icons = [html.I(className="fas fa-copy text-muted")] * n
        all_closed = [False] * n
        disable_interval = True
        reset_ticks = 0

        # если ничего не кликнули и не тикает
        if not n or (not any(n_clicks_list) and (tick is None or tick == 0)):
            return default_icons, all_closed, disable_interval, reset_ticks

        triggered = ctx.triggered_id

        # ⏱ тикнул интервал — закрываем все тултипы
        if triggered == "copy-tooltip-interval":
            return default_icons, all_closed, True, 0

        # 🖱 клик по кнопке копирования
        if isinstance(triggered, dict) and triggered.get("type") == "copy-log":
            clicked_ts = triggered["index"]

            icons = []
            tooltips = []
            # проходим по всем id, реально сравнивая значение index
            for i, btn in enumerate(ctx.inputs_list[0]):
                idx = btn["id"]["index"]
                if idx == str(clicked_ts):
                    icons.append(html.I(className="fas fa-copy text-primary"))
                    tooltips.append(True)  # показать тултип только у нужного
                else:
                    icons.append(html.I(className="fas fa-copy text-muted"))
                    tooltips.append(False)

            # включаем интервал на 1 секунду для автозакрытия
            return icons, tooltips, False, 0

        return default_icons, all_closed, True, 0

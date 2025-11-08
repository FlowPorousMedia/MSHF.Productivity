from datetime import datetime
import time
import dash
from dash import ALL, Input, Output, State, html, ctx, no_update, dcc

from src.app._version import SOFTWARE_TITLE, USER_VERSION
from src.app.services.log_item_worker import filter_logs, render_log_item
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

        filtered = filter_logs(
            logs, err_outline, warn_outline, info_outline, checklist, search_text
        )

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

    @app.callback(
        Output("download-logs", "data"),
        Input("save-logs-button", "n_clicks"),
        State("log-store", "data"),
        State("filter-error", "outline"),
        State("filter-warning", "outline"),
        State("filter-info", "outline"),
        State("logs-checklist", "value"),
        State("logs-search", "value"),
        prevent_initial_call=True,
    )
    def save_filtered_logs(
        n_clicks, logs, err_outline, warn_outline, info_outline, checklist, search_text
    ):
        if not n_clicks or not logs:
            return dash.no_update

        filtered = filter_logs(
            logs, err_outline, warn_outline, info_outline, checklist, search_text
        )

        if not filtered:
            return dash.no_update

        # === Формируем текст ===
        lines = []
        for log in filtered:
            lines.append(
                f"[{log['timestamp']}] {getattr(log['level'], 'value', log['level'])} "
                f"{getattr(log['category'], 'value', log['category']).upper()}: {log['message']}"
            )
        content = "\n".join(lines)

        # === Формируем имя файла ===
        filename = (
            f"{SOFTWARE_TITLE}_v{USER_VERSION}_logs_"
            f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        )

        # === Отправляем файл ===
        return dcc.send_string(content, filename)

    @app.callback(
        Output("save-logs-button", "disabled"),
        Output("save-logs-button", "style"),
        Input("log-store", "data"),
    )
    def toggle_save_button(logs):
        if not logs or len(logs) == 0:
            return True, {
                "opacity": "0.5",
                "pointerEvents": "none",
                "cursor": "not-allowed",
            }
        return False, {"opacity": "1.0", "cursor": "pointer"}

    @app.callback(
        Output("logs-count", "children"),
        Input("log-store", "data"),
        Input("filter-error", "outline"),
        Input("filter-warning", "outline"),
        Input("filter-info", "outline"),
        Input("logs-checklist", "value"),
        Input("logs-search", "value"),
    )
    def update_logs_count(
        logs, err_outline, warn_outline, info_outline, checklist, search_text
    ):
        if not logs:
            return "Showing 0 messages"

        filtered = filter_logs(
            logs, err_outline, warn_outline, info_outline, checklist, search_text
        )

        return f"Showing {len(filtered)} of {len(logs)} messages"

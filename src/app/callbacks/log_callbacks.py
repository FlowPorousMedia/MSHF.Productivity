from dash import Input, Output, State, html

import dash_bootstrap_components as dbc


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

    # подгрузка логов в тело модалки
    @app.callback(
        Output("logs-body", "children"),
        Input("log-store", "data"),
    )
    def render_logs(logs):
        if not logs:
            return html.Div("No logs yet.", className="text-muted")

        items = []
        for log in logs:
            color = {
                "INFO": "primary",
                "WARNING": "warning",
                "ERROR": "danger",
            }.get(
                (
                    log["level"].name
                    if hasattr(log["level"], "name")
                    else str(log["level"])
                ),
                "secondary",
            )

            items.append(
                dbc.Alert(
                    [
                        html.Strong(f"[{log['timestamp']}] "),
                        html.Span(
                            f"{log['category'].name if hasattr(log['category'], 'name') else log['category']}: "
                        ),
                        html.Span(log["message"]),
                    ],
                    color=color,
                    className="mb-2",
                )
            )

        return html.Div(items)

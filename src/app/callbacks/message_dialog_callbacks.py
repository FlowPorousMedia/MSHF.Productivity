import dash
from dash import Input, Output, ctx, ALL, no_update, State
from src.app.components.message_dialog import get_message_dialog
from src.app.models.message_type import MessageType


def register(app):
    @app.callback(
        Output("msg-dialog", "is_open"),
        Output("msg-dialog", "children"),
        Output("open-msg-dialog", "clear_data"),
        Output("msg-dialog-response-store", "data"),
        Input("open-msg-dialog", "data"),
        Input({"type": "msg-btn", "index": ALL}, "n_clicks"),
        State("msg-dialog", "is_open"),
        prevent_initial_call=True,
    )
    def control_dialog(open_data, btn_clicks, is_open):
        # Determine what triggered the callback
        trigger = ctx.triggered_id

        # Case 1: open dialog
        if open_data is not None:
            dialog = get_message_dialog(
                "msg-dialog",
                open_data.get("title", "Message"),
                open_data.get("message", ""),
                MessageType[open_data.get("type", "INFO").upper()],
                open_data.get("buttons", ["OK"]),
            )
            return True, dialog.children, True, None  # reset store to None immediately

        # Case 2: user clicked a button
        if isinstance(trigger, dict) and trigger.get("type") == "msg-btn":
            btn_id = trigger["index"]
            context = None
            if isinstance(open_data, dict):
                context = open_data.get("context")
            return (
                False,
                no_update,
                True,
                {"context": context, "response": btn_id},
            )

        raise dash.exceptions.PreventUpdate

    @app.callback(
        Output("calc-state", "data", allow_duplicate=True),
        Input("msg-dialog-response-store", "data"),
        prevent_initial_call=True,
    )
    def handle_dialog_response(data):
        if not data:
            raise dash.exceptions.PreventUpdate

        context = data.get("context")
        response = data.get("response")

        # 👇 Универсальная логика
        if context == "confirm_calc_start":
            if response == "Yes":
                return "running"  # начать расчёт
            else:
                return "idle"  # отменить

        # можно расширять для других случаев
        # if context == "delete_model": ...
        # if context == "reset_params": ...
        return no_update

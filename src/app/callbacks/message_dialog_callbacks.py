import dash
from dash import Input, Output, ctx, ALL, no_update, State
from src.app.components.message_dialog import get_message_dialog
from src.app.models.message_type import MessageType


def register(app):
    @app.callback(
        Output("msg-dialog", "is_open"),
        Output("msg-dialog", "children"),
        Output("open-msg-dialog", "clear_data"),
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
            return True, dialog.children, True  # reset store to None immediately

        # Case 2: user clicked a button
        if isinstance(trigger, dict) and trigger.get("type") == "msg-btn":
            btn_id = trigger["index"]
            return False, no_update, True  # close dialog + clear store

        raise dash.exceptions.PreventUpdate

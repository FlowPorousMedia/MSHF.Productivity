# src/app/callbacks/message_bus_callbacks.py
from dash import Input, Output, State, ALL, ctx, no_update
from src.app.components.message_dialog import get_message_dialog
from src.app.models.message_type import MessageType


def register(app):
    # 1️⃣ Открываем диалог (пришёл запрос)
    @app.callback(
        Output("msg-dialog", "is_open", allow_duplicate=True),
        Output("msg-dialog", "children", allow_duplicate=True),
        Output("message-context", "data", allow_duplicate=True),
        Input("message-request", "data"),
        prevent_initial_call=True,
    )
    def open_dialog(request_data):
        if not request_data:
            raise no_update

        context = request_data.get("context")

        dialog = get_message_dialog(
            "msg-dialog",
            request_data.get("title", "Message"),
            request_data.get("message", ""),
            MessageType[request_data.get("type", "INFO").upper()],
            request_data.get("buttons", ["OK"]),
            context=context,  # 👈 добавляем контекст сюда!
        )

        return True, dialog.children, context

    # 2️⃣ Пользователь нажал кнопку (Yes / No / OK)
    @app.callback(
        Output("msg-dialog", "is_open", allow_duplicate=True),
        Output("message-response", "data", allow_duplicate=True),
        Input({"type": "msg-btn", "index": ALL}, "n_clicks"),
        State("message-context", "data"),
        prevent_initial_call=True,
    )
    def handle_modal_buttons(btn_clicks, context):
        # Фильтр: если ни одна кнопка не нажата — не делаем ничего
        if not btn_clicks or all(click is None for click in btn_clicks):
            return no_update, no_update

        trigger = ctx.triggered_id
        if not isinstance(trigger, dict) or trigger.get("type") != "msg-btn":
            return no_update, no_update

        btn_id = trigger["index"]

        # Закрываем модалку и возвращаем ответ
        return False, {"context": context, "response": btn_id}

from dash import html, dcc
import dash_bootstrap_components as dbc


from src.app.models.message_type import MessageType


# Message dialog component
def get_message_dialog(
    dialog_id, title, message, type: MessageType.INFO, buttons=["OK"]
):
    icons = {MessageType.INFO: "ℹ️", MessageType.WARNING: "⚠️", MessageType.ERROR: "❌"}
    return dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle(f"{icons.get(type, '')} {title}"),
                close_button=False,  # disable the "X"
            ),
            dbc.ModalBody(message),
            dbc.ModalFooter(
                [
                    dbc.Button(b, id={"type": "msg-btn", "index": b}, className="me-2")
                    for b in buttons
                ]
            ),
        ],
        id=dialog_id,
        is_open=False,
        backdrop="static",  # user must click a button
        keyboard=False,      # cannot close with ESC
        centered=True,
    )

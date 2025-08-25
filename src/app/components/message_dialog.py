from dash import html, dcc
import dash_bootstrap_components as dbc


from src.app.models.message_type import MessageType


# Message dialog component
def get_message_dialog(
    dialog_id, title, message, type: MessageType.INFO, buttons=["OK"]
):
    icons = {
        MessageType.INFO: html.I(className="fa-solid fa-circle-info"),
        MessageType.WARNING: html.I(className="fa-solid fa-triangle-exclamation"),
        MessageType.ERROR: html.I(
            className="fas fa-circle-xmark", style={"color": "red", "margin-right": "8px"}
        ),
    }
    return dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle([icons.get(type, ""), title]),
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
        keyboard=False,  # cannot close with ESC
        centered=True,
    )

from dash import html, dcc
import dash_bootstrap_components as dbc


from src.app.models.message_type import MessageType


# Message dialog component
def get_message_dialog(
    dialog_id, title, message, type: MessageType.INFO, buttons=["OK"]
):
    title_colors = {
        MessageType.INFO: "blue",
        MessageType.WARNING: "orange",
        MessageType.ERROR: "red",
    }

    icons = {
        MessageType.INFO: html.I(
            className="fa-solid fa-circle-info",
            style={"color": title_colors[MessageType.INFO], "margin-right": "8px"},
        ),
        MessageType.WARNING: html.I(
            className="fa-solid fa-triangle-exclamation",
            style={"color": title_colors[MessageType.WARNING], "margin-right": "8px"},
        ),
        MessageType.ERROR: html.I(
            className="fas fa-circle-xmark",
            style={"color": title_colors[MessageType.ERROR], "margin-right": "8px"},
        ),
    }

    return dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle(
                    [
                        icons.get(type, ""),
                        html.Span(
                            title, style={"color": title_colors.get(type, "black")}
                        ),
                    ]
                ),
                close_button=False,  # disable the "X"
            ),
            __create_modal_body_with_newlines(message),
            # dbc.ModalBody(message),
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



def __create_modal_body_with_newlines(message: str, style: dict = None) -> dbc.ModalBody:
    """
    Create a ModalBody that properly handles newline characters
    """
    default_style = {"whiteSpace": "pre-line", "padding": "10px"}
    if style:
        default_style.update(style)
    
    return dbc.ModalBody(
        html.Div(message, style=default_style)
    )
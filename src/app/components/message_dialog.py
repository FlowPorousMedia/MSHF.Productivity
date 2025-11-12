from dash import html
import dash_bootstrap_components as dbc
from src.app.models.message_type import MessageType


def get_message_dialog(
    dialog_id,
    title,
    message,
    type: MessageType = MessageType.INFO,
    buttons=["OK"],
    context=None,  # 👈 добавлен
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

    normalized_buttons = []
    for b in buttons:
        if isinstance(b, dict):
            normalized_buttons.append(b)
        else:
            normalized_buttons.append({"label": str(b), "value": str(b)})

    # Весь контент оборачиваем в контейнер с data-context
    content = html.Div(
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
                close_button=False,
            ),
            __create_modal_body_with_newlines(message),
            dbc.ModalFooter(
                [
                    dbc.Button(
                        b["label"],
                        id={"type": "msg-btn", "index": str(b["value"])},
                        className="me-2",
                    )
                    for b in normalized_buttons
                ]
            ),
        ],
        **({"data-context": context} if context else {}),
    )

    return dbc.Modal(
        content,
        id=dialog_id,
        is_open=False,
        backdrop="static",
        keyboard=False,
        centered=True,
    )


def __create_modal_body_with_newlines(
    message: str, style: dict = None
) -> dbc.ModalBody:
    """
    Create a ModalBody that properly handles newline characters
    """
    default_style = {"whiteSpace": "pre-line", "padding": "10px"}
    if style:
        default_style.update(style)

    return dbc.ModalBody(html.Div(message, style=default_style))

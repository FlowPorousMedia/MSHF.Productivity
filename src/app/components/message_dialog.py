from dash import html
import dash_bootstrap_components as dbc

from src.core.models.message_level import MessageLevel


def get_message_dialog(
    dialog_id,
    title,
    message,
    type: MessageLevel = MessageLevel.INFO,
    buttons=["OK"],
    context=None,
):
    """
    Универсальное диалоговое окно сообщений.
    Поддерживает MessageLevel с автоматическими цветами и иконками.
    """

    normalized_buttons = []
    for b in buttons:
        if isinstance(b, dict):
            normalized_buttons.append(b)
        else:
            normalized_buttons.append({"label": str(b), "value": str(b)})

    header_icon = html.I(
        className=type.icon,
        style={"color": type.color, "marginRight": "8px"},
    )

    title_span = html.Span(title, style={"color": type.color})

    # Весь контент оборачиваем в контейнер с data-context
    content = html.Div(
        [
            dbc.ModalHeader(
                dbc.ModalTitle([header_icon, title_span]),
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

import re
from dash import html
import dash_bootstrap_components as dbc


def render_log_item(log, search_text=None):
    level = log["level"].value if hasattr(log["level"], "value") else str(log["level"])
    color_map = {
        "DEBUG": "secondary",
        "INFO": "info",
        "WARNING": "warning",
        "ERROR": "danger",
        "CRITICAL": "dark",
    }
    badge_color = color_map.get(level, "secondary")

    category = (
        log["category"].value
        if hasattr(log["category"], "value")
        else str(log["category"])
    )

    message = log["message"]

    # === Подсветка текста ===
    if search_text:
        pattern = re.escape(search_text)
        parts = re.split(f"({pattern})", message, flags=re.IGNORECASE)
        message_content = []
        for part in parts:
            if re.fullmatch(f"({pattern})", part, flags=re.IGNORECASE):
                message_content.append(
                    html.Span(
                        part, style={"backgroundColor": "yellow", "fontWeight": "600"}
                    )
                )
            else:
                message_content.append(part)
    else:
        message_content = [message]

    return dbc.Card(
        dbc.CardBody(
            [
                html.Small(f"[{log['timestamp']}]", className="text-muted me-2"),
                dbc.Badge(level, color=badge_color, className="me-2"),
                html.Span(f"{category.upper()}: ", className="fw-semibold"),
                html.Span(message_content),
            ],
            className="py-2",
        ),
        className="mb-1 shadow-sm border-0 bg-light",
    )

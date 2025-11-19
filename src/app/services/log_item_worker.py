import re
from typing import Any, Dict, List
import uuid
from dash import html, dcc
import dash_bootstrap_components as dbc

from src.app.i18n import _


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

    unique_id = f"{log['timestamp']}-{uuid.uuid4().hex[:6]}"

    copy_id = {"type": "copy-log", "index": unique_id}
    copied_tooltip_id = {"type": "copied-tooltip", "index": unique_id}
    copy_tooltip_id = {"type": "copy-tooltip", "index": unique_id}

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Small(
                            f"[{log['timestamp']}]", className="text-muted me-2"
                        ),
                        dbc.Badge(level, color=badge_color, className="me-2"),
                        html.Span(f"{category.upper()}: ", className="fw-semibold"),
                        html.Span(message_content),
                    ],
                    className="d-inline",
                    id=f"log-text-{log['timestamp']}",
                ),
                html.Span(
                    html.I(
                        className="fas fa-copy text-muted", title=_("Copy to clipboard")
                    ),
                    id=copy_id,
                    className="float-end copy-icon",
                    style={"cursor": "pointer"},
                    n_clicks=0,
                ),
                dcc.Clipboard(
                    target_id=f"log-text-{log['timestamp']}",
                    title=_("Copy to clipboard"),
                    style={"visibility": "hidden", "position": "absolute"},
                ),
                # 1. Тултип-подсказка (hover)
                dbc.Tooltip(
                    _("Copy to clipboard"),
                    target=copy_id,
                    id=copy_tooltip_id,
                    placement="top",
                    trigger="hover",  # стандартный режим
                ),
                # 2. Тултип-уведомление (manual)
                dbc.Tooltip(
                    _("Copied!"),
                    target=copy_id,
                    id=copied_tooltip_id,
                    placement="top",
                    trigger="manual",  # срабатывает мануально
                    is_open=False,
                ),
            ],
            className="py-2 position-relative",
        ),
        className="mb-1 shadow-sm border-0 bg-light",
    )


def filter_logs(
    logs: List[Dict[str, Any]],
    err_outline: bool,
    warn_outline: bool,
    info_outline: bool,
    checklist: list,
    search_text: str,
) -> list:
    """Возвращает список логов, отфильтрованных по уровням, категориям и поиску."""

    if not logs:
        return []

    # === Активные уровни ===
    active_levels = []
    if not err_outline:
        active_levels.append("ERROR")
    if not warn_outline:
        active_levels.append("WARNING")
    if not info_outline:
        active_levels.append("INFO")
    if "system" in checklist:
        active_levels.append("DEBUG")

    # === Категории ===
    if "calc" in checklist:
        allowed_categories = ["calculation"]
    else:
        allowed_categories = ["calculation", "ui", "check_data", "system"]

    # === Поиск ===
    search_text = (search_text or "").lower().strip()

    # === Фильтрация ===
    filtered = []
    for log in logs:
        level = str(getattr(log["level"], "value", log["level"]))
        category = str(getattr(log["category"], "value", log["category"]))
        if level not in active_levels:
            continue
        if category not in allowed_categories:
            continue
        if search_text and search_text not in log["message"].lower():
            continue
        filtered.append(log)

    return filtered

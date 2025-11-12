import dash_bootstrap_components as dbc
from dash import html, dcc

from src.app.i18n import _
from src.core.models.message_level import MessageLevel


def create_log_viewer():
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle(_("Log Viewer")), close_button=False),
            dbc.ModalBody(
                [
                    # 1. Первая строка — фильтры по уровням
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(_("Show logs for:"), className="fw-semibold"),
                                width="auto",
                            ),
                            dbc.Col(
                                dbc.ButtonGroup(
                                    [
                                        dbc.Button(
                                            _(MessageLevel.ERROR.label),
                                            id="filter-error",
                                            color=MessageLevel.ERROR.color,
                                            outline=False,
                                            n_clicks=0,
                                        ),
                                        dbc.Button(
                                            _(MessageLevel.WARNING.label),
                                            id="filter-warning",
                                            color=MessageLevel.WARNING.color,
                                            outline=False,
                                            n_clicks=0,
                                        ),
                                        dbc.Button(
                                            _(MessageLevel.INFO.label),
                                            id="filter-info",
                                            color=MessageLevel.INFO.color,
                                            outline=False,
                                            n_clicks=0,
                                        ),
                                    ],
                                    size="sm",
                                ),
                                width="auto",
                            ),
                        ],
                        className="g-2 mb-2 align-items-center",
                    ),
                    # 2. Чекбоксы
                    dbc.Row(
                        dbc.Col(
                            dbc.Checklist(
                                options=[
                                    {
                                        "label": _("Show only calculation logs"),
                                        "value": "calc",
                                    },
                                    {"label": _("Show system logs"), "value": "system"},
                                ],
                                value=["calc"],
                                id="logs-checklist",
                                inline=True,
                                switch=True,
                            )
                        ),
                        className="mb-2",
                    ),
                    # 3. Поиск
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    _("Search:"), className="fw-semibold text-end"
                                ),
                                width="auto",
                                className="align-self-center pe-0",  # убираем лишний отступ справа
                            ),
                            dbc.Col(
                                dbc.Input(
                                    id="logs-search",
                                    type="text",
                                    placeholder=_("Search in logs..."),
                                    size="sm",
                                ),
                                width=6,
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        id="logs-count",
                        className="text-muted small mb-2 fst-italic",
                    ),
                    # 4. Тело логов
                    html.Div(id="logs-body", className="logs-container"),
                    dcc.Interval(
                        id="copy-tooltip-interval",
                        interval=1000,  # 1 секунда
                        disabled=True,
                        n_intervals=0,
                    ),
                ]
            ),
            dbc.ModalFooter(
                [
                    dbc.Button(
                        _("Save"),
                        id="save-logs-button",
                        color="success",
                        className="me-2",
                        n_clicks=0,
                    ),
                    dbc.Button(
                        _("Clear"),
                        id="clear-logs-button",
                        color="danger",
                        outline=True,
                        className="me-2",
                        n_clicks=0,
                    ),
                    dbc.Button(
                        _("Close"),
                        id="close-logs-button",
                        className="ms-auto",
                        n_clicks=0,
                    ),
                    dcc.Download(id="download-logs"),  # 👈 компонент для скачивания
                ]
            ),
        ],
        id="modal-logs",
        is_open=False,
        size="xl",
        scrollable=True,
        backdrop="static",
        keyboard=False,
    )

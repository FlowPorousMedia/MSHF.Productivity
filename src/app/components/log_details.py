import dash_bootstrap_components as dbc
from dash import html


def create_logs_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Log Viewer"), close_button=False),
            dbc.ModalBody(
                [
                    # 1. Первая строка — фильтры по уровням
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div("Show logs for:", className="fw-semibold"),
                                width="auto",
                            ),
                            dbc.Col(
                                dbc.ButtonGroup(
                                    [
                                        dbc.Button(
                                            "ERROR",
                                            id="filter-error",
                                            color="danger",
                                            outline=False,
                                            n_clicks=0,
                                        ),
                                        dbc.Button(
                                            "WARNING",
                                            id="filter-warning",
                                            color="warning",
                                            outline=False,
                                            n_clicks=0,
                                        ),
                                        dbc.Button(
                                            "INFO",
                                            id="filter-info",
                                            color="info",
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
                                        "label": "Show only calculation logs",
                                        "value": "calc",
                                    },
                                    {"label": "Show system logs", "value": "system"},
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
                                html.Div("Search:", className="fw-semibold text-end"),
                                width="auto",
                                className="align-self-center pe-0",  # убираем лишний отступ справа
                            ),
                            dbc.Col(
                                dbc.Input(
                                    id="logs-search",
                                    type="text",
                                    placeholder="Search in logs...",
                                    size="sm",
                                ),
                                width=6,
                            ),
                        ],
                        className="mb-3",
                    ),
                    # 4. Тело логов
                    html.Div(id="logs-body", className="logs-container"),
                ]
            ),
            dbc.ModalFooter(
                [
                    dbc.Button(
                        "Clear",
                        id="clear-logs-button",
                        color="danger",
                        outline=True,
                        className="me-2",
                        n_clicks=0,
                    ),
                    dbc.Button(
                        "Close", id="close-logs-button", className="ms-auto", n_clicks=0
                    ),
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

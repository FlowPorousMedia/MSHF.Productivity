import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, no_update


def create_logs_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Calculation Logs")),
            dbc.ModalBody(id="logs-body"),  # сюда будем рендерить логи
            dbc.ModalFooter(
                dbc.Button(
                    "Close", id="close-logs-button", className="ms-auto", n_clicks=0
                )
            ),
        ],
        id="modal-logs",
        is_open=False,
        size="lg",  # можно md / lg / xl
        scrollable=True,  # если логов много
    )

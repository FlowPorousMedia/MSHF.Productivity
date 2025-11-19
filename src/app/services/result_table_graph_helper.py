from dash import html
import dash_bootstrap_components as dbc
from src.app.i18n import _


def get_default_containers():
    """Возвращает исходные пустые контейнеры графика и таблицы"""
    graph_container = [
        html.H4(_("Results Plot"), className="mb-3"),
        html.Div(
            [
                html.I(className="bi bi-graph-up me-2"),
                _('Press "Calculate" to see visual results here'),
            ],
            className="alert alert-light d-flex align-items-center",
        ),
    ]

    table_container = [
        html.H4(_("Results Table"), className="mb-3"),
        html.Div(
            [
                html.I(className="bi bi-table me-2"),
                _('Press "Calculate" to see table results here'),
            ],
            className="alert alert-light d-flex align-items-center",
        ),
    ]

    return graph_container, table_container


def get_calc_content():
    return html.Div(
        [
            html.Div(
                [
                    html.I(className="bi bi-hourglass-split me-2"),
                    _("Calculation in progress..."),
                ],
                className="alert alert-info d-flex align-items-center",
            ),
        ]
    )

from dash import html, dcc
import dash_bootstrap_components as dbc

from src.app.i18n import _
from src.app.models.default_values import DEFAULT_VALUES


def create_reservoir_params():
    """Create reservoir parameters component"""

    defaults = DEFAULT_VALUES["reservoir"]

    return html.Div(
        [
            # Radius input
            dbc.Row(
                [
                    dbc.Col(html.Label(_("Radius, (m):"), className="fw-bold"), width=6),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "reservoir-params", "name": "radius"},
                            type="number",
                            value=defaults["radius"],
                            min=10,
                            step=10,
                            className="form-control",
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
            # Height input
            dbc.Row(
                [
                    dbc.Col(html.Label(_("Height, (m):"), className="fw-bold"), width=6),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "reservoir-params", "name": "height"},
                            type="number",
                            value=defaults["height"],
                            min=1,
                            step=1,
                            className="form-control",
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
            # Permeability input
            dbc.Row(
                [
                    dbc.Col(
                        html.Label(_("Permeability, (D):"), className="fw-bold"), width=6
                    ),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "reservoir-params", "name": "permeability"},
                            type="number",
                            value=defaults["permeability"],
                            min=0.1,
                            step=0.1,
                            className="form-control",
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
            # Pressure input
            dbc.Row(
                [
                    dbc.Col(
                        html.Label(_("Pressure, (atm):"), className="fw-bold"), width=6
                    ),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "reservoir-params", "name": "pressure"},
                            type="number",
                            value=defaults["pressure"],
                            min=0,
                            step=1,
                            className="form-control",
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
        ]
    )

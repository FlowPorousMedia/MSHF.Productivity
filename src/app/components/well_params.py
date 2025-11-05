from dash import html, dcc
import dash_bootstrap_components as dbc

from src.app.models.default_values import DEFAULT_VALUES
from src.core.models.init_data.field_names.well_initial_field_names import (
    WellInitFieldNames,
)


def create_well_params():
    """Create well parameters component"""

    defaults = DEFAULT_VALUES["well"]

    return html.Div(
        [
            # Length input
            dbc.Row(
                [
                    dbc.Col(
                        html.Label(WellInitFieldNames.L.value, className="fw-bold"),
                        width=6,
                    ),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "well-params", "name": "length"},
                            type="number",
                            value=defaults["length"],
                            min=100,
                            step=10,
                            className="form-control",
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
            # Radius input
            dbc.Row(
                [
                    dbc.Col(
                        html.Label(WellInitFieldNames.RW.value, className="fw-bold"),
                        width=6,
                    ),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "well-params", "name": "radius"},
                            type="number",
                            value=defaults["radius"],
                            min=1,
                            step=1,
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
                        html.Label(WellInitFieldNames.PW.value, className="fw-bold"),
                        width=6,
                    ),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "well-params", "name": "pressure"},
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
            # Perforation status
            dbc.Row(
                [
                    dbc.Col(
                        html.Label(
                            WellInitFieldNames.IS_PERFORATED.value, className="fw-bold"
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        dcc.Checklist(
                            id={"type": "well-params", "name": "perforated"},
                            options=[{"label": " Yes", "value": True}],
                            value=[True] if defaults["perforated"] else [],
                            className="pt-2",
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
        ]
    )

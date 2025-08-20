from dash import html, dcc
import dash_bootstrap_components as dbc


def create_reservoir_params():
    """Create reservoir parameters component"""
    return html.Div(
        [
            # Radius input
            dbc.Row(
                [
                    dbc.Col(html.Label("Radius (m):", className="fw-bold"), width=6),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "reservoir-params", "name": "radius"},
                            type="number",
                            value=200,
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
                    dbc.Col(html.Label("Height (m):", className="fw-bold"), width=6),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "reservoir-params", "name": "height"},
                            type="number",
                            value=10,
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
                        html.Label("Permeability (D):", className="fw-bold"), width=6
                    ),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "reservoir-params", "name": "permeability"},
                            type="number",
                            value=0.1,
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
                        html.Label("Pressure (atm):", className="fw-bold"), width=6
                    ),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "reservoir-params", "name": "pressure"},
                            type="number",
                            value=100,
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

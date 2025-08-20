from dash import html, dcc
import dash_bootstrap_components as dbc


def create_well_params():
    """Create well parameters component"""
    return html.Div(
        [
            # Length input
            dbc.Row(
                [
                    dbc.Col(html.Label("Length (m):", className="fw-bold"), width=6),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "well-params", "name": "length"},
                            type="number",
                            value=400,
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
                    dbc.Col(html.Label("Radius (cm):", className="fw-bold"), width=6),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "well-params", "name": "radius"},
                            type="number",
                            value=8,
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
                        html.Label("Pressure (atm):", className="fw-bold"), width=6
                    ),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "well-params", "name": "pressure"},
                            type="number",
                            value=80,
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
                    dbc.Col(html.Label("Perforated:", className="fw-bold"), width=6),
                    dbc.Col(
                        dcc.Checklist(
                            id={"type": "well-params", "name": "perforated"},
                            options=[{"label": " Yes", "value": True}],
                            value=[True],
                            className="pt-2",
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
        ]
    )

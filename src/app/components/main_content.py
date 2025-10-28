from dash import html
import dash_bootstrap_components as dbc

from src.app.components.parametric_settings_panel import (
    create_parametric_settings_panel,
)


def create_main_content():
    """Create the main content area with visualization and table"""
    return html.Div(
        id="main-content",
        style={"flex": "1", "overflow": "auto", "padding": "20px", "minWidth": 0},
        children=[
            # Toggle button for sidebar (mobile view)
            # html.Button(
            #     "☰", id="sidebar-toggle_mobile", className="btn btn-secondary d-md-none mb-3"
            # ),
            # Main content title
            html.H2("Fracture Analysis Dashboard", className="mb-4"),
            # Action bar with Calculate button
            create_action_panel(),
            # Graph and table container
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            id="graph-container",
                            className="bg-white p-3 border rounded",
                            children=[
                                html.H4("Results Plot", className="mb-3"),
                                html.Div(
                                    [
                                        html.I(className="bi bi-graph-up me-2"),
                                        'Press "Calculate" to see visual results here',
                                    ],
                                    className="alert alert-light d-flex align-items-center",
                                ),
                            ],
                        ),
                        width=12,
                        className="mb-4",
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            id="table-container",
                            className="bg-white p-3 border rounded",
                            children=[
                                html.H4("Results Table", className="mb-3"),
                                html.Div(
                                    [
                                        html.I(className="bi bi-table me-2"),
                                        'Press "Calculate" to see table results here',
                                    ],
                                    className="alert alert-light d-flex align-items-center",
                                ),
                            ],
                        ),
                        width=12,
                    )
                ]
            ),
        ],
    )


def create_action_panel():
    return dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            html.I(className="fas fa-play"),
                            id="calculate-button",
                            color="primary",
                            title="Run calculation",
                            n_clicks=0,
                            className="d-flex align-items-center justify-content-center",
                            style={"width": "32px", "height": "32px", "padding": 0},
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        dbc.Button(
                            html.I(className="fas fa-list-alt"),
                            id="show-logs-button",
                            color="primary",
                            title="Show logs",
                            disabled=True,
                            n_clicks=0,
                            className="d-flex align-items-center justify-content-center",
                            style={"width": "32px", "height": "32px", "padding": 0},
                        ),
                        width="auto",
                    ),
                ],
                className="g-2",
                justify="start",
            )
        ),
        className="mb-4 shadow-sm",
    )

from dash import html
import dash_bootstrap_components as dbc

from src.app.components.parametric_settings_panel import create_parametric_settings_panel


def create_main_content():
    """Create the main content area with visualization and table"""
    return html.Div(
        id="main-content",
        style={"flex": "1", "overflow": "auto", "padding": "20px"},
        children=[
            # Toggle button for sidebar (mobile view)
            html.Button(
                "☰", id="sidebar-toggle", className="btn btn-secondary d-md-none mb-3"
            ),
            # Main content title
            html.H2("Fracture Analysis Dashboard", className="mb-4"),  
            # Action bar with Calculate button
            dbc.Row(
                dbc.Col(
                    dbc.Button(
                        "Calculate",
                        id="calculate-button",
                        color="primary",
                        size="lg",
                        className="w-100 mb-4",
                    ),
                )
            ),
            # Graph and table container
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            id="graph-container",
                            className="bg-white p-3 border rounded",
                            children=[
                                html.H4("Results Visualization", className="mb-3"),
                                html.Div(
                                    [
                                        html.I(className="bi bi-graph-up me-2"),
                                        "Press \"Calculate\" to see visual results here",
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
                                        "Press \"Calculate\" to see table results here",
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

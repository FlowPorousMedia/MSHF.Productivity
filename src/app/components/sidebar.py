from dash import html, dcc
import dash_bootstrap_components as dbc

from src.app.components.fracture_params import create_fracture_params
from src.app.components.parametric_settings_panel import (
    create_parametric_settings_panel,
)
from src.app.components.well_params import create_well_params
from src.app.components.reservoir_params import create_reservoir_params
from src.app.components.fluid_params import create_fluid_params
from src.app.models.analyt_models import get_analytic_models
from src.app.models.semianalyt_models import get_semianalytic_models
from src.app.services import models_grid_creator


def create_sidebar():
    analytical_models = get_analytic_models()
    semianalytical_models = get_semianalytic_models()
    """Create sidebar with foldable panels"""
    return html.Div(
        id="sidebar-container",
        style={
            "display": "flex",
            "height": "100vh",
        },
        children=[
            # Sidebar
            html.Div(
                id="sidebar",
                className="sidebar bg-light",
                style={
                    "width": "400px",
                    "minWidth": "260px",
                    "maxWidth": "75vw",
                    "height": "100%",
                    "position": "relative",
                    "overflow": "hidden",
                },
                children=[
                    html.Div(
                        style={
                            "display": "flex",
                            "justifyContent": "space-between",
                            "alignItems": "center",
                            "padding": "10px 15px",
                            "borderBottom": "1px solid #dee2e6",
                            "backgroundColor": "#f8f9fa",
                        },
                        children=[
                            html.H5("Parameters", style={"margin": "0"}),
                            html.Button(
                                id="sidebar-toggle",
                                children="☰",  # Hamburger icon
                                style={
                                    "background": "none",
                                    "border": "none",
                                    "fontSize": "20px",
                                    "cursor": "pointer",
                                    "padding": "5px 10px",
                                    "borderRadius": "3px",
                                },
                                title="Collapse/Expand sidebar",
                            ),
                        ],
                    ),
                    # Content wrapper
                    html.Div(
                        className="sidebar-content",
                        style={
                            "width": "100%",
                            "height": "100%",
                            "overflowY": "auto",
                            "overflowX": "hidden",
                            "paddingRight": "8px",
                        },
                        children=[
                            # Accordion with foldable panels
                            dbc.Accordion(
                                [
                                    dbc.AccordionItem(
                                        [
                                            # Nested accordion for parameters
                                            dbc.Accordion(
                                                [
                                                    # Fracture Parameters Subpanel
                                                    dbc.AccordionItem(
                                                        create_fracture_params(),
                                                        title="Fracture Parameters",
                                                        item_id="fracture-panel",
                                                    ),
                                                    # Well Parameters Subpanel
                                                    dbc.AccordionItem(
                                                        create_well_params(),
                                                        title="Well Parameters",
                                                        item_id="well-panel",
                                                    ),
                                                    # Reservoir Parameters Subpanel
                                                    dbc.AccordionItem(
                                                        create_reservoir_params(),
                                                        title="Reservoir Parameters",
                                                        item_id="reservoir-panel",
                                                    ),
                                                    # Fluid Properties Subpanel
                                                    dbc.AccordionItem(
                                                        create_fluid_params(),
                                                        title="Fluid Properties",
                                                        item_id="fluid-panel",
                                                    ),
                                                ],
                                                flush=True,
                                                start_collapsed=True,
                                            )
                                        ],
                                        title="Input Data",
                                        item_id="input-data-panel",
                                        className="mt-3",
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            dbc.Accordion(
                                                [
                                                    dbc.AccordionItem(
                                                        models_grid_creator.create(
                                                            analytical_models,
                                                            ag_grid_id="analytical-models-gridtable",
                                                        ),
                                                        title="Analytical",
                                                        item_id="analytical-model-panel",
                                                    ),
                                                    dbc.AccordionItem(
                                                        models_grid_creator.create(
                                                            semianalytical_models,
                                                            ag_grid_id="semianalytical-models-gridtable",
                                                        ),
                                                        title="Semi-analytical",
                                                        item_id="semianalytical-model-panel",
                                                    ),
                                                ],
                                                flush=True,
                                                start_collapsed=True,
                                            )
                                        ],
                                        title="Models",
                                        item_id="models-panel",
                                        className="mt-3",
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            dbc.Accordion(
                                                [
                                                    dbc.AccordionItem(
                                                        [
                                                            create_parametric_settings_panel()
                                                        ],
                                                        title="Parametric Calc Settings",
                                                        item_id="parametric-settings-panel",
                                                        className="mt-3",
                                                    ),
                                                ],
                                                flush=True,
                                                start_collapsed=True,
                                            )
                                        ],
                                        title="Settings",
                                        item_id="settings-panel",
                                        className="mt-3",
                                    ),
                                ],
                                active_item=[],
                                flush=True,
                                className="mt-3",
                            ),
                            # Hidden store for fracture data
                            dcc.Store(id="fracture-data-store"),
                        ],
                    ),
                ],
            ),
            # Resize handle as separate component
            html.Div(
                id="sidebar-resize-handle",
                style={
                    "width": "8px",
                    "height": "100%",
                    "backgroundColor": "rgba(0,0,0,0.1)",
                    "cursor": "col-resize",
                    "zIndex": 1001,
                    "transition": "background-color 0.2s",
                },
            ),
        ],
    )

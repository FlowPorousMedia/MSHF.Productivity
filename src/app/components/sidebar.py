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
        id="sidebar",
        className="sidebar bg-light",
        style={
            "width": "400px",
            "height": "100vh",
            "overflowY": "auto",
            "position": "relative",
        },
        children=[
            # Resize handle (optional)
            html.Div(
                id="sidebar-resize-handle",
                style={
                    "position": "absolute",
                    "top": 0,
                    "right": 0,
                    "width": "6px",
                    "height": "100%",
                    "background": "#ddd",
                    "cursor": "col-resize",
                    "zIndex": 1000,
                },
            ),
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
                                start_collapsed=True,  # Start with all subpanels collapsed
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
                                        ),  # Use our new component
                                        title="Semi-analytical",
                                        item_id="semianalytical-model-panel",
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            html.Div(
                                                "Additional models will go here",
                                                className="p-2",
                                            )
                                        ],
                                        title="Numerical",
                                        item_id="numerical-model-panel",
                                    ),
                                ],
                                flush=True,
                                start_collapsed=True,  # Start with all subpanels collapsed
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
                                    # Other Settings Panel
                                    dbc.AccordionItem(
                                        [create_parametric_settings_panel()],
                                        title="Parametric Calc Settings",
                                        item_id="parametric-settings-panel",
                                        className="mt-3",
                                    ),
                                ],
                                flush=True,
                                start_collapsed=True,  # Start with all subpanels collapsed
                            )
                        ],
                        title="Settings",
                        item_id="settings-panel",
                        className="mt-3",
                    ),
                ],
                # Start with all panels closed
                active_item=[],
                flush=True,
                className="mt-3",
            ),
            # Hidden store for fracture data
            dcc.Store(id="fracture-data-store"),
        ],
    )

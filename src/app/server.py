from dash import (
    Dash,
    Input,
    Output,
    html,
    dcc,
)
import dash_bootstrap_components as dbc


from src.app.callbacks.main_callbacks import register_all_callbacks
from src.app.components.about_modal import create_about_modal
from src.app.components.model_details import create_model_details_modal
from src.app.components.navbar import create_navbar
from src.app.components.sidebar import create_sidebar
from src.app.components.main_content import create_main_content

from src.app.models.analyt_models import get_analytic_models
from src.app.models.numerical_models import get_numerical_models
from src.app.models.semianalyt_models import get_semianalytic_models
from src.app._version import USER_VERSION

# Initialize the app
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
    ],
    assets_folder="assets",
)

# Define the app layout
app.layout = html.Div(
    style={"height": "100vh", "display": "flex"},
    children=[
        dcc.Store(id="analytical-models-store", data=get_analytic_models()),
        dcc.Store(id="semianalytical-models-store", data=get_semianalytic_models()),
        # dcc.Store(id="numerical-models-store", data=get_numerical_models()),
        dcc.Store(id="solver-result-store", data=None),
        create_navbar(),
        create_about_modal(),
        create_sidebar(),
        create_main_content(),
        create_model_details_modal(),
        # Hidden elements for future functionality
        dcc.Store(id="sidebar-width-store", data=400),
        dcc.Store(id="resize-state-store", data={"resizing": False}),
        html.Div(id="resize-mousemove", style={"display": "none"}),
        html.Div(id="resize-mouseup", style={"display": "none"}),
        # Add stores for parameter groups
        dcc.Store(id="well-params-store", data={}),
        dcc.Store(id="reservoir-params-store", data={}),
        dcc.Store(id="fluid-params-store", data={}),
    ],
)

register_all_callbacks(app)

#  Это важно для развертывания
server = app.server

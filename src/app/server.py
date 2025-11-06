from dash import Dash, html, dcc, DiskcacheManager
import dash_bootstrap_components as dbc
import diskcache


from src.app.components.about_modal import create_about_modal
from src.app.components.log_details import create_logs_modal
from src.app.components.model_details import create_model_details_modal
from src.app.components.navbar import create_navbar
from src.app.components.sidebar import create_sidebar
from src.app.components.main_content import create_main_content
from src.app.components.message_dialog import get_message_dialog
from src.app.models.analyt_models import get_analytic_models
from src.app.models.message_type import MessageType
from src.app.models.numerical_models import get_numerical_models
from src.app.models.semianalyt_models import get_semianalytic_models
from src.app._version import SOFTWARE_TITLE


def create_app() -> Dash:
    """
    Initialize the app
    """

    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache)

    app = Dash(
        __name__,
        title=SOFTWARE_TITLE,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
        ],
        assets_folder="assets",
        background_callback_manager=background_callback_manager,
    )

    # Define the app layout
    app.layout = html.Div(
        style={"height": "100vh", "display": "flex", "flexDirection": "column"},
        # style={"height": "100vh", "display": "flex"},
        children=[
            dcc.Location(id="url", refresh=False),  # Add this to handle URL routing
            # Navbar at the top
            create_navbar(),
            # Content area with sidebar and main content
            html.Div(
                style={"display": "flex", "flex": 1, "overflow": "hidden"},
                children=[
                    create_sidebar(),
                    create_main_content(),
                ],
            ),
            create_about_modal(),
            create_model_details_modal(),
            get_message_dialog(
                "msg-dialog", "Message", "Default", MessageType.INFO, ["OK"]
            ),
            create_logs_modal(),
            # ===============
            # Add stores for parameter groups
            # ===============
            dcc.Store(id="well-params-store", data={}),
            dcc.Store(id="reservoir-params-store", data={}),
            dcc.Store(id="fluid-params-store", data={}),
            # ===============
            # Hidden elements for future functionality
            # ===============
            dcc.Store(id="analytical-models-store", data=get_analytic_models()),
            dcc.Store(id="semianalytical-models-store", data=get_semianalytic_models()),
            # dcc.Store(id="numerical-models-store", data=get_numerical_models()),
            dcc.Store(id="language-store", data="en"),
            dcc.Store(id="log-store", data=[]),
            dcc.Store(id="solver-result-store", data=None),
            # ===============
            # Central state & message channels
            # ===============
            dcc.Store(id="app-state", data="init"),
            dcc.Store(id="message-request"),
            dcc.Store(id="message-response"),
            dcc.Store(id="message-context", data=None),
            # ===============
            # Helpers
            # ===============
            dcc.Store(id="sidebar-width-store", data=400),
            dcc.Store(id="resize-state-store", data={"resizing": False}),
            html.Div(id="resize-mousemove", style={"display": "none"}),
            html.Div(id="resize-mouseup", style={"display": "none"}),
        ],
    )

    return app

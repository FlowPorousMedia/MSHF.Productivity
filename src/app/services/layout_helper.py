from dash import html, dcc
from src.app.i18n import _, set_language
from src.app.components.about_modal import create_about_modal
from src.app.components.log_viewer import create_log_viewer
from src.app.components.model_details import create_model_details_modal
from src.app.components.navbar import create_navbar
from src.app.components.sidebar import create_sidebar
from src.app.components.main_content import create_main_content
from src.app.components.message_dialog import get_message_dialog
from src.app.models.analyt_models import get_analytic_models
from src.app.models.semianalyt_models import get_semianalytic_models
from src.core.models.message_level import MessageLevel


# -------------------------------------------------------------
# 1. Полный UI (layout, созданный на нужном языке)
# -------------------------------------------------------------
def create_main_layout():
    """
    Полный UI приложения на уже выбранном языке.
    """

    return html.Div(
        style={"height": "100vh", "display": "flex", "flexDirection": "column"},
        children=[
            dcc.Location(id="url", refresh=False),
            html.Div(
                id="app-content-container",
                children=[
                    create_navbar(),
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
                        "msg-dialog",
                        _("Message"),
                        _("Default"),
                        MessageLevel.INFO,
                        [_("OK")],
                    ),
                    create_log_viewer(),
                ],
            ),
            # Stores
            dcc.Store(id="well-params-store", data={}),
            dcc.Store(id="reservoir-params-store", data={}),
            dcc.Store(id="fluid-params-store", data={}),
            dcc.Store(id="analytical-models-store", data=get_analytic_models()),
            dcc.Store(id="semianalytical-models-store", data=get_semianalytic_models()),
            # dcc.Store(id="language-store", storage_type="local"),
            dcc.Store(id="log-store", data=[]),
            dcc.Store(id="solver-result-store", data=None),
            dcc.Store(id="app-state", data="init"),
            dcc.Store(id="message-request"),
            dcc.Store(id="message-response"),
            dcc.Store(id="message-context", data=None),
            dcc.Store(id="sidebar-width-store", data=400),
            dcc.Store(id="resize-state-store", data={"resizing": False}),
            html.Div(id="resize-mousemove", style={"display": "none"}),
            html.Div(id="resize-mouseup", style={"display": "none"}),
        ],
    )


# -------------------------------------------------------------
# 2. Минимальный layout (загружается первым)
# -------------------------------------------------------------
def serve_layout():
    """
    Минимальный layout, который Dash загружает при первой загрузке.
    Содержит:
    - language-store (загружается из localStorage)
    - loader
    - пустой контейнер main-ui, куда мы вставим настоящий UI
    """

    return html.Div(
        [
            dcc.Store(id="language-store", data=None, storage_type="local"),
            html.Div(
                id="loader",
                children=html.H2(
                    "Loading...", style={"textAlign": "center", "marginTop": "40vh"}
                ),
            ),
            html.Div(id="main-ui"),
        ]
    )


# -------------------------------------------------------------
# 3. Строим полный UI после того, как язык известен
# -------------------------------------------------------------
def build_ui_for_language(lang: str):
    set_language(lang)
    return create_main_layout()

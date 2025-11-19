import diskcache
from dash import Dash, DiskcacheManager
import dash_bootstrap_components as dbc


from src.app._version import SOFTWARE_TITLE


def create_app():
    """
    Создаёт Dash приложение БЕЗ layout.
    Layout мы зададим позже через app.layout = serve_layout.
    """
    cache = diskcache.Cache("./cache")
    manager = DiskcacheManager(cache)

    app = Dash(
        __name__,
        title=SOFTWARE_TITLE,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,
        background_callback_manager=manager,
    )
    return app

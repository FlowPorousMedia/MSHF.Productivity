from dash import Input, Output
from src.app.i18n import set_language


def register(app):
    # Инициализация языка при загрузке
    @app.callback(
        Output("app-state", "data"),
        Input("language-store", "data"),
    )
    def init_language(lang):
        set_language(lang)
        return "init"

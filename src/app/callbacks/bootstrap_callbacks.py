from dash import Output, Input, no_update

from src.app.services.layout_helper import build_ui_for_language


def register(app):

    @app.callback(
        Output("loader", "style"),
        Output("main-ui", "children"),
        Input("language-store", "data"),
        prevent_initial_call=True,
    )
    def load_main_ui(lang):

        # localStorage ещё не загрузился
        if not lang:
            return no_update, no_update

        # Полный UI на нужном языке
        ui = build_ui_for_language(lang)

        # Спрятать loader, показать UI
        return {"display": "none"}, ui

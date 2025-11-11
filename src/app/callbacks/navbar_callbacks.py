import dash
from dash import Input, Output, State, ctx

from src.app.i18n import set_language, _
from src.app.services.translator_helpers import with_language


def register(app):
    # Callback for language selection (you would expand this based on your i18n implementation)
    @app.callback(
        Output("language-store", "data"),
        Input("lang-ru", "n_clicks"),
        Input("lang-en", "n_clicks"),
        prevent_initial_call=True,
    )
    def update_language(ru_clicks, en_clicks):
        trigger = ctx.triggered_id
        if trigger == "lang-ru":
            return "ru"
        elif trigger == "lang-en":
            return "en"
        raise dash.exceptions.PreventUpdate

    # Callback for navbar collapse on small screens
    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    # Callback for the About modal
    @app.callback(
        Output("about-modal", "is_open"),
        [Input("about-link", "n_clicks"), Input("close-about", "n_clicks")],
        [State("about-modal", "is_open")],
    )
    def toggle_about(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @app.callback(Output("guide-navlink", "href"), Input("language-store", "data"))
    def update_guide_link(language):
        if language == "ru":
            return "https://github.com/FlowPorousMedia/MSHF.Productivity/wiki/Home-RU"
        else:
            return "https://github.com/FlowPorousMedia/MSHF.Productivity/wiki/Home-EN"

    @app.callback(
        Output("github-tooltip", "children"),
        Output("language-tooltip", "children"),
        Output("guide-tooltip", "children"),
        Output("about-tooltip", "children"),
        Input("language-store", "data"),
    )
    @with_language
    def update_tooltips(language):
        return (
            _("Github"),
            _("Language"),
            _("Guide"),
            _("About"),
        )

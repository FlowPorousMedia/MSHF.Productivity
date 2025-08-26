from dash import Input, Output, State, no_update, callback_context, html


def register(app):
    # Callback for language selection (you would expand this based on your i18n implementation)
    @app.callback(
        Output("language-dropdown", "label"),
        Output("language-store", "data"),
        # Input("lang-ru", "n_clicks"),
        Input("lang-en", "n_clicks"),
        State("language-store", "data"),
        prevent_initial_call=True,
    )
    # def update_language(ru_clicks, en_clicks, current_lang):
    def update_language(en_clicks, current_lang):
        ctx = callback_context
        if not ctx.triggered:
            return html.I(className="fas fa-language", id="language-icon"), current_lang

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "lang-ru":
            return html.I(className="fas fa-language", id="language-icon"), "ru"
        elif button_id == "lang-en":
            return html.I(className="fas fa-language", id="language-icon"), "en"

        return html.I(className="fas fa-flag"), current_lang

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

    @app.callback(
        Output("github-tooltip", "children"),
        Output("language-tooltip", "children"),
        Output("guide-tooltip", "children"),
        Output("about-tooltip", "children"),
        Input("language-store", "data"),
    )
    def update_tooltips(language):
        if language == "ru":
            return "GitHub", "Язык", "Руководство пользователя", "О программе"
        else:
            return "GitHub", "Language", "User Guide", "About"

    @app.callback(Output("guide-navlink", "href"), Input("language-store", "data"))
    def update_guide_link(language):
        if language == "ru":
            return "https://github.com/FlowPorousMedia/MSHF.Productivity/wiki/Home-RU"
        else:
            return "https://github.com/FlowPorousMedia/MSHF.Productivity/wiki/Home-EN"

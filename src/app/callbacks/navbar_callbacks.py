from dash import Input, Output, State, no_update, callback_context


def register(app):
    # Callback for language selection (you would expand this based on your i18n implementation)
    @app.callback(
        Output("url", "pathname"),  # This would update based on your app structure
        [
            Input("lang-ru", "n_clicks"),
            Input("lang-en", "n_clicks"),
        ],
    )
    def change_language(ru, en):
        ctx = callback_context
        if not ctx.triggered:
            return no_update
        else:
            lang_id = ctx.triggered[0]["prop_id"].split(".")[0]
            # Here you would implement your language change logic
            print(f"Language changed to: {lang_id}")
            return no_update

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

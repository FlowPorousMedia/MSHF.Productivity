from dash import Input, Output, State, no_update, callback_context


def register(app):
    # Add this callback to your app
    @app.callback(
        Output("sidebar", "className"),
        Input("sidebar-toggle", "n_clicks"),
        State("sidebar", "className"),
        prevent_initial_call=True,
    )
    def toggle_sidebar(n_clicks, current_class):
        if n_clicks:
            if "show" in current_class:
                return current_class.replace("show", "").strip()
            else:
                return current_class + " show"
        return current_class

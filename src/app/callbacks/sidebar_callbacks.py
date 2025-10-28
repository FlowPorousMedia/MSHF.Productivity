from dash import Input, Output, State


def register(app):
    # Toggle sidebar visibility
    @app.callback(
        Output("sidebar", "className"),
        Input("sidebar-toggle", "n_clicks"),
        State("sidebar", "className"),
        prevent_initial_call=True,
    )
    def toggle_sidebar(n, current_class):
        if "collapsed" in current_class:
            return current_class.replace(" collapsed", "")
        else:
            return current_class + " collapsed"

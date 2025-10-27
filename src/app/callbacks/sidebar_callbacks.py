from dash import Input, Output, State


def register(app):
    # Toggle sidebar visibility
    @app.callback(
        Output("sidebar", "className"),
        Input("sidebar-toggle", "n_clicks"),
        State("sidebar", "className"),
        prevent_initial_call=True,
    )
    def toggle_sidebar(n_clicks, current_class):
        print(
            f"Callback triggered! n_clicks: {n_clicks}, current_class: '{current_class}'"
        )

        if n_clicks is None:
            return current_class

        if "collapsed" in current_class:
            new_class = current_class.replace("collapsed", "").strip()
            print(f"Removing collapsed. New class: '{new_class}'")
            return new_class
        else:
            new_class = current_class + " collapsed" if current_class else "collapsed"
            print(f"Adding collapsed. New class: '{new_class}'")
            return new_class

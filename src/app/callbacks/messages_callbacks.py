from dash import Input, Output, State, no_update


def register(app):
    @app.callback(
        Output("error-alert", "children"),
        Output("error-alert", "is_open"),
        Input("error-store", "data"),
    )
    def show_error(data):
        if data and data.get("show"):
            return data["message"], True
        return "", False

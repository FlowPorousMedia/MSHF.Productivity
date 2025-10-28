from dash import Input, Output, State, html


def register(app):
    # Toggle sidebar visibility
    @app.callback(
        [Output("sidebar", "className"), Output("sidebar-toggle", "children")],
        Input("sidebar-toggle", "n_clicks"),
        State("sidebar", "className"),
        prevent_initial_call=True,
    )
    def toggle_sidebar(n, current_class):
        if "collapsed" in current_class:
            # раскрыто -> стрелка влево
            return current_class.replace(" collapsed", ""), html.I(
                className="fas fa-chevron-left"
            )
        else:
            # свернуто -> стрелка вправо
            return current_class + " collapsed", html.I(
                className="fas fa-chevron-right"
            )

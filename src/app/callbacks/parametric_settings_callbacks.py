from dash import Input, Output, State
from dash.exceptions import PreventUpdate


def register(app):
    """Register all callbacks related to settings panel"""

    @app.callback(
        [
            Output("parameter-dropdown", "disabled"),
            Output("start-input", "disabled"),
            Output("end-input", "disabled"),
            Output("point-count-input", "disabled"),
        ],
        Input("parametric-plot-checkbox", "value"),
    )
    def toggle_parametric_inputs(checked):
        # Enable inputs when checkbox is checked, disable otherwise
        state = not checked if checked is not None else True
        return [state] * 4  # Return disabled state for all four components

import dash
from dash import Output
from dash import Input
from dash import ALL


def register(app):
    # Aggregation callback for well parameters
    @app.callback(
        Output("well-params-store", "data"),
        Input({"type": "well-params", "name": ALL}, "value"),
    )
    def aggregate_well_params(values):
        # Get callback context
        ctx = dash.callback_context

        # Create dictionary of name:value pairs
        return {
            inp["id"]["name"]: value for inp, value in zip(ctx.inputs_list[0], values)
        }

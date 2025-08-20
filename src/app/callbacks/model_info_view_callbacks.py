from dash import Input, Output, State, callback_context, no_update

from src.app.services.model_info_worker import model_info_to_html


def register(app):
    @app.callback(
        [
            Output("model-info-modal", "is_open"),
            Output("model-info-modal-body", "children"),
        ],
        [
            Input("analytical-models-gridtable", "cellRendererData"),
            Input("semianalytical-models-gridtable", "cellRendererData"),
            # Input("numerical-models-gridtable", "cellRendererData"),
            Input("close-model-info-modal", "n_clicks"),
        ],
        [
            State("model-info-modal", "is_open"),
            State("analytical-models-store", "data"),
            State("semianalytical-models-store", "data"),
            # State("numerical-models-store", "data"),
        ],
    )
    def toggle_modal(
        analytical_click,
        semi_click,
        close_clicks,
        is_open,
        analytical_models,
        semi_models,
        # numerical_models,
    ):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update

        trigger_id: str = ctx.triggered[0]["prop_id"].split(".")[0]

        # Handle Details button clicks
        if trigger_id.endswith("-gridtable"):
            # Get clicked data from the triggered table
            click_data = ctx.triggered[0]["value"]

            if not click_data:
                return no_update, no_update

            model_id = click_data["rowId"]

            # Determine which store to use based on triggered table
            if trigger_id == "analytical-models-gridtable":
                model_store = analytical_models
            elif trigger_id == "semianalytical-models-gridtable":
                model_store = semi_models
            elif trigger_id == "numerical-models-gridtable":
                # model_store = numerical_models
                return no_update, no_update
            else:
                return no_update, no_update

            # Find the matching model
            model = next((m for m in model_store if m["id"] == model_id), None)
            if model:
                content = model_info_to_html(model)
                return True, content

        # Handle modal close button
        elif trigger_id == "close-model-info-modal":
            return False, no_update

        return no_update, no_update

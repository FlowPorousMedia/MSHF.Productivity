from dash import Input, Output, State, html

from src.app.components.task_scheme import create_task_scheme_component


def register(app):
    # Toggle sidebar visibility
    @app.callback(
        Output("scheme-container", "children"),
        [
            Input("well-params-store", "data"),
            Input("reservoir-params-store", "data"),
            Input("fracture-table", "data"),
        ],
    )
    def update_scheme(well_data, res_data, fracts_data):
        L = 1000
        R = 300
        fracts = []

        if well_data:
            L = well_data.get("length", 1000)

        if res_data:
            R = res_data.get("radius", 300)

        if fracts_data:
            fracts = []
            for i, frac in enumerate(fracts_data):
                lp = frac.get("length_plus")
                lm = frac.get("length_minus")
                pos = frac.get("well_cross")
                fracts.append({"pos": pos, "len_plus": lp, "len_minus": lm})
        return create_task_scheme_component(L, R, fracts)

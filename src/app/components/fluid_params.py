from dash import html, dcc
import dash_bootstrap_components as dbc


def create_fluid_params():
    """Create fluid properties component"""
    return html.Div(
        [
            # Viscosity input
            dbc.Row(
                [
                    dbc.Col(
                        html.Label("Viscosity (cP):", className="fw-bold"), width=6
                    ),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "fluid-params", "name": "viscosity"},
                            type="number",
                            value=1.0,
                            min=0.01,
                            step=0.01,
                            className="form-control",
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
            # Density input
            # dbc.Row(
            #     [
            #         dbc.Col(
            #             html.Label("Density (kg/m³):", className="fw-bold"), width=6
            #         ),
            #         dbc.Col(
            #             dcc.Input(
            #                 id="fluid-density",  id={"type": "fluid-params", "name": "viscosity"},
            #                 type="number",
            #                 value=800,
            #                 min=1,
            #                 step=1,
            #                 className="form-control",
            #             ),
            #             width=6,
            #         ),
            #     ],
            #     className="mb-3",
            # ),
            # # Compressibility input
            # dbc.Row(
            #     [
            #         dbc.Col(
            #             html.Label("Compressibility (1/atm):", className="fw-bold"),
            #             width=6,
            #         ),
            #         dbc.Col(
            #             dcc.Input(
            #                 id="fluid-compressibility", id={"type": "fluid-params", "name": "viscosity"},
            #                 type="number",
            #                 value=1e-5,
            #                 min=0,
            #                 step=1e-6,
            #                 className="form-control",
            #             ),
            #             width=6,
            #         ),
            #     ],
            #     className="mb-3",
            # ),
            # # Formation volume factor
            # dbc.Row(
            #     [
            #         dbc.Col(
            #             html.Label("FVF (dimensionless):", className="fw-bold"), width=6
            #         ),
            #         dbc.Col(
            #             dcc.Input(
            #                 id="fluid-fvf", id={"type": "fluid-params", "name": "viscosity"},
            #                 type="number",
            #                 value=1.2,
            #                 min=1.0,
            #                 step=0.01,
            #                 className="form-control",
            #             ),
            #             width=6,
            #         ),
            #     ],
            #     className="mb-3",
            # ),
        ]
    )

from dash import html, dcc
import dash_bootstrap_components as dbc

from src.app.i18n import _
from src.app.models.default_values import DEFAULT_VALUES


def create_fluid_params():
    """Create fluid properties component"""

    defaults = DEFAULT_VALUES["fluid"]

    return html.Div(
        [
            # Viscosity input
            dbc.Row(
                [
                    dbc.Col(
                        html.Label(_("Viscosity (cP):"), className="fw-bold"), width=6
                    ),
                    dbc.Col(
                        dcc.Input(
                            id={"type": "fluid-params", "name": "viscosity"},
                            type="number",
                            value=defaults["viscosity"],
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
            #                 value=defaults["density"],
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
            #                 value=defaults["compressibility"],
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
            #                 value=defaults["fvf"],
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

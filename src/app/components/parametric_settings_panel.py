from dash import html, dcc
import dash_bootstrap_components as dbc

from src.core.models.init_data.calc_over_param_enum import CalcParamTypeEnum


def create_parametric_settings_panel():
    return html.Div(
        [
            # Parametric Plot Checkbox (already has inline label)
            dbc.Checkbox(
                id="parametric-plot-checkbox",
                label="Parametric Plot",
                value=True,
                className="mb-3",
            ),
            # Parameter Selection Combobox with inline label
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Label("Parameter", width="auto"),
                        className="pe-0 d-flex align-items-center",
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="parameter-dropdown",
                            options=[
                                {
                                    "label": CalcParamTypeEnum.FRACT_COUNT.display_name,
                                    "value": CalcParamTypeEnum.FRACT_COUNT.value,
                                },
                            ],
                            value=CalcParamTypeEnum.FRACT_COUNT.value,
                            disabled=True,
                        ),
                        className="ps-0",
                    ),
                ],
                className="mb-3 g-0 align-items-center",
            ),
            # Start/End Inputs with inline labels
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Label("Start", width="auto"),
                        className="pe-0 d-flex align-items-center",
                    ),
                    dbc.Col(
                        dbc.Input(
                            id="start-input",
                            type="number",
                            placeholder="Start",
                            value=2,
                            min=2,
                            step=1,
                            disabled=True,
                        ),
                        className="g-0",
                    ),
                ],
                className="g-0 align-items-center",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Label("End", width="auto"),
                        className="pe-0 d-flex align-items-center",
                    ),
                    dbc.Col(
                        dbc.Input(
                            id="end-input",
                            type="number",
                            placeholder="End",
                            value=10,
                            min=2,
                            step=1,
                            disabled=True,
                        ),
                        className="ps-0",
                    ),
                ],
                className="g-0 align-items-center",
            ),
            # Point Count Input with inline label
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Label("Point Count", width="auto"),
                        className="pe-0 d-flex align-items-center",
                    ),
                    dbc.Col(
                        dbc.Input(
                            id="point-count-input",
                            type="number",
                            placeholder="Point Count",
                            value=9,
                            min=2,
                            step=1,
                            disabled=True,
                        ),
                        className="ps-0",
                    ),
                ],
                className="g-0 align-items-center",
            ),
        ],
        className="p-3",
    )

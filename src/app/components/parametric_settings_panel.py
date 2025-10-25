from dash import html, dcc
import dash_bootstrap_components as dbc

from src.core.models.init_data.calc_over_param_enum import CalcParamTypeEnum


def create_parametric_settings_panel():
    # Общие классы для выравнивания
    label_col_class = "pe-0 d-flex align-items-center"
    input_col_class = "ps-0"
    row_class = "mb-3 g-0 align-items-center"

    # Ширина правой колонки (в Bootstrap-сетке: 1–12)
    INPUT_COL_WIDTH = 8

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
                        className=label_col_class,
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="parameter-dropdown",
                            options=[
                                {
                                    "label": CalcParamTypeEnum.FRACT_COUNT.display_name,
                                    "value": CalcParamTypeEnum.FRACT_COUNT.value,
                                },
                                {
                                    "label": CalcParamTypeEnum.FRACT_LEN.display_name,
                                    "value": CalcParamTypeEnum.FRACT_LEN.value,
                                },
                                {
                                    "label": CalcParamTypeEnum.FRACT_PERM.display_name,
                                    "value": CalcParamTypeEnum.FRACT_PERM.value,
                                },
                                {
                                    "label": CalcParamTypeEnum.FRACT_WIDTH.display_name,
                                    "value": CalcParamTypeEnum.FRACT_WIDTH.value,
                                },
                                {
                                    "label": CalcParamTypeEnum.WELL_LEN.display_name,
                                    "value": CalcParamTypeEnum.WELL_LEN.value,
                                },
                                {
                                    "label": CalcParamTypeEnum.RES_RAD.display_name,
                                    "value": CalcParamTypeEnum.RES_RAD.value,
                                },
                                {
                                    "label": CalcParamTypeEnum.RES_HEIGTH.display_name,
                                    "value": CalcParamTypeEnum.RES_HEIGTH.value,
                                },
                            ],
                            value=CalcParamTypeEnum.FRACT_COUNT.value,
                            disabled=True,
                            className="w-100",
                        ),
                        className=input_col_class,
                        width=INPUT_COL_WIDTH,
                    ),
                ],
                className=row_class,
            ),
            # Start/End Inputs with inline labels
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Label("Start", width="auto"),
                        className=label_col_class,
                    ),
                    dbc.Col(
                        dbc.Input(
                            id="start-input",
                            type="number",
                            placeholder="Start",
                            value=2,
                            min=2,
                            step=1,
                            max=20,
                            disabled=True,
                            className="w-100",
                        ),
                        className=input_col_class,
                        width=INPUT_COL_WIDTH,
                    ),
                ],
                className=row_class,
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Label("End", width="auto"),
                        className=label_col_class,
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
                            className="w-100",
                        ),
                        className=input_col_class,
                        width=INPUT_COL_WIDTH,
                    ),
                ],
                className=row_class,
            ),
            # Point Count Input with inline label
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Label("Point Count", width="auto"),
                        className=label_col_class,
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
                            className="w-100",
                        ),
                        className=input_col_class,
                        width=INPUT_COL_WIDTH,
                    ),
                ],
                className=row_class,
            ),
        ],
        className="p-3",
    )

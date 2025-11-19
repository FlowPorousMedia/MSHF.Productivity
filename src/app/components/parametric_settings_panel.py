from dash import html, dcc
import dash_bootstrap_components as dbc

from src.app.i18n import _
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
                label=_("Parametric Plot"),
                value=True,
                className="mb-3",
            ),
            # Parameter Selection Combobox with inline label
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Label(_("Parameter"), width="auto"),
                        className=label_col_class,
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="parameter-dropdown",
                            options=[
                                {
                                    "label": CalcParamTypeEnum.FRACT_COUNT.label,
                                    "value": CalcParamTypeEnum.FRACT_COUNT.value,
                                },
                                {
                                    "label": CalcParamTypeEnum.FRACT_LEN.label,
                                    "value": CalcParamTypeEnum.FRACT_LEN.value,
                                },
                                {
                                    "label": CalcParamTypeEnum.FRACT_PERM.label,
                                    "value": CalcParamTypeEnum.FRACT_PERM.value,
                                },
                                {
                                    "label": CalcParamTypeEnum.FRACT_WIDTH.label,
                                    "value": CalcParamTypeEnum.FRACT_WIDTH.value,
                                },
                                {
                                    "label": CalcParamTypeEnum.WELL_LEN.label,
                                    "value": CalcParamTypeEnum.WELL_LEN.value,
                                },
                                {
                                    "label": CalcParamTypeEnum.RES_RAD.label,
                                    "value": CalcParamTypeEnum.RES_RAD.value,
                                },
                                {
                                    "label": CalcParamTypeEnum.RES_HEIGTH.label,
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
                        dbc.Label(_("Start"), width="auto"),
                        className=label_col_class,
                    ),
                    dbc.Col(
                        dbc.Input(
                            id="start-input",
                            type="number",
                            placeholder=_("Start"),
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
                        dbc.Label(_("End"), width="auto"),
                        className=label_col_class,
                    ),
                    dbc.Col(
                        dbc.Input(
                            id="end-input",
                            type="number",
                            placeholder=_("End"),
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
                        dbc.Label(_("Point Count"), width="auto"),
                        className=label_col_class,
                    ),
                    dbc.Col(
                        dbc.Input(
                            id="point-count-input",
                            type="number",
                            placeholder=_("Point Count"),
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

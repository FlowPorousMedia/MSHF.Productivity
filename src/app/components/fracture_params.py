from dash import html, dash_table, dcc

from src.core.models.init_data.field_names.fract_initial_field_names import (
    FracInitFieldNames,
)


def create_fracture_params():
    """Create fracture parameters component with dynamic table"""
    return html.Div(
        [
            html.Div(
                [
                    html.Label(
                        "Fractures count:",
                        className="fw-bold mb-0 align-self-center",
                    ),
                    dcc.Input(
                        id="fracture-count",
                        type="number",
                        value=3,
                        min=1,
                        step=1,
                        className="form-control ms-3",
                        style={"width": "100px"},
                    ),
                    html.Button(
                        "×",  # или можно использовать "Delete All"
                        id="delete-all-fractures",
                        className="btn btn-danger ms-2 p-1",
                        title="Delete all fractures",
                        style={"width": "32px", "height": "32px"},
                    ),
                ],
                className="d-flex align-items-center mb-3",
            ),
            # Fracture parameters table
            dash_table.DataTable(
                id="fracture-table",
                columns=[
                    {
                        "name": "Fract",
                        "id": "fracture_id",
                        "editable": False,
                    },
                    {
                        "name": FracInitFieldNames.LENGTH_PLUS.value,
                        "id": "length_plus",
                        "editable": True,
                        "type": "numeric",
                    },
                    {
                        "name": FracInitFieldNames.LENGTH_MINUS.value,
                        "id": "length_minus",
                        "editable": True,
                        "type": "numeric",
                    },
                    {
                        "name": FracInitFieldNames.WIDTH.value,
                        "id": "width",
                        "editable": True,
                        "type": "numeric",
                    },
                    {
                        "name": FracInitFieldNames.PERMEABILITY.value,
                        "id": "permeability",
                        "editable": True,
                        "type": "numeric",
                    },
                    {
                        "name": FracInitFieldNames.WELL_CROSS.value,
                        "id": "well_cross",
                        "editable": True,
                        "type": "numeric",
                    },
                ],
                data=[
                    {
                        "fracture_id": i + 1,
                        "length_plus": 100,
                        "length_minus": 100,
                        "width": 40,
                        "permeability": 10000,
                        "well_cross": i * 400,
                    }
                    for i in range(3)
                ],
                editable=True,
                row_deletable=False,
                style_table={
                    "overflowX": "auto",
                    "maxHeight": "200px",
                    "overflowY": "scroll",
                    "minWidth": "100%",
                },
                style_cell={
                    "minWidth": "80px",  # Минимальная ширина
                    "maxWidth": "150px",  # Увеличим максимальную ширину
                    "padding": "5px",
                    "textOverflow": "ellipsis",  # Оставляем, но с переносом строк
                    "whiteSpace": "normal",  # Разрешаем перенос слов
                    "height": "auto",  # Автоматическая высота
                },
                style_header={
                    "backgroundColor": "rgb(230, 230, 230)",
                    "fontWeight": "bold",
                    "textAlign": "center",  # Выравнивание по центру
                    "whiteSpace": "normal",  # Перенос слов в заголовках
                    "height": "auto",  # Автоматическая высота
                    "lineHeight": "15px",  # Межстрочный интервал
                    "position": "sticky",
                    "top": 0,
                },
                style_data_conditional=[
                    {
                        "if": {"row_index": "odd"},
                        "backgroundColor": "rgb(248, 248, 248)",
                    }
                ],
            ),
            html.Button(
                "Show Fcd",
                id="show-fcd-button",
                className="btn btn-secondary ms-2",
                title="Show Fcd values",
            ),
        ]
    )

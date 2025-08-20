from dash import html, dash_table, dcc


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
                    {"name": "Fracture", "id": "fracture_id", "editable": False},
                    {
                        "name": "Length Plus (m)",
                        "id": "length_plus",
                        "editable": True,
                        "type": "numeric",
                    },
                    {
                        "name": "Length Minus (m)",
                        "id": "length_minus",
                        "editable": True,
                        "type": "numeric",
                    },
                    {
                        "name": "Width (mm)",
                        "id": "width",
                        "editable": True,
                        "type": "numeric",
                    },
                    {
                        "name": "Permeability (D)",
                        "id": "permeability",
                        "editable": True,
                        "type": "numeric",
                    },
                    {
                        "name": "Well cross depth (m)",
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
                        "well_cross": i * 200,
                    }
                    for i in range(3)
                ],
                editable=True,
                row_deletable=False,
                style_table={
                    "overflowX": "auto",
                    "minWidth": "100%",  # Гарантирует, что таблица займет всю ширину контейнера
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
                },
                style_data_conditional=[
                    {
                        "if": {"row_index": "odd"},
                        "backgroundColor": "rgb(248, 248, 248)",
                    }
                ],
            ),
        ]
    )

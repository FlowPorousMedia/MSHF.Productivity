from typing import List

import dash_ag_grid as dag

from src.core.models.init_data.models_enum import ModelsEnum


def create(models: List, ag_grid_id: str):
    columns_definition = [
        # Добавляем скрытое поле с ID
        {"field": "id", "hide": True},  # Скрываем, но оно будет доступно в данных
        {
            "field": "name",
            "headerName": "Model",
            "checkboxSelection": True,
            "flex": 8,  # 90% of available space (9 parts out of 10)
        },
        {
            "field": "info",
            "headerName": "Info",
            "flex": 2,  # 10% of available space (1 part out of 10)
            "cellRenderer": "Button",
            "cellRendererParams": {
                "className": "btn btn-info",
            },
        },
    ]

    selected_ids = models

    return dag.AgGrid(
        id=ag_grid_id,
        columnDefs=columns_definition,
        rowData=models,
        selectedRows=selected_ids,
        dashGridOptions={
            "headerHeight": 0,  # This hides the header row
            "getRowId": "params.data.id",  # Используем ID модели как идентификатор строк
            "rowSelection": "multiple",
            "suppressRowClickSelection": True,
            "animateRows": False,
            "domLayout": "autoHeight",
        },
    )

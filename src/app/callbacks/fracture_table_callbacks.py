import dash
from dash import (
    Output,
    Input,
    State,
)

from src.app.models.message_type import MessageType


def register(app):
    @app.callback(
        Output("fracture-count", "value"),
        Output("fracture-table", "data"),
        Input("fracture-count", "value"),
        Input("delete-all-fractures", "n_clicks"),
        State("fracture-table", "data"),
        prevent_initial_call=True,
    )
    def update_fracture_system(fracture_count, delete_clicks, current_data):
        ctx = dash.callback_context
        trigger_id = (
            ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None
        )

        # Handle delete button click
        if trigger_id == "delete-all-fractures" and delete_clicks:
            # Reset count to 1 and create one empty fracture row
            return 1, [{"fracture_id": 1}]

        # Handle fracture count change
        elif trigger_id == "fracture-count" and fracture_count is not None:
            if fracture_count < 1:
                return 1, [{"fracture_id": 1}]

            current_data = current_data or []
            current_rows = len(current_data)

            # Сохраняем существующие данные
            new_data = []

            # Копируем существующие строки (если они есть)
            for i in range(min(current_rows, fracture_count)):
                # Если в текущих данных есть строка - используем ее
                row = current_data[i].copy()
                # Обновляем fracture_id на случай изменения порядка
                row["fracture_id"] = i + 1
                new_data.append(row)

            # Добавляем новые строки при увеличении количества
            if fracture_count > current_rows:
                for i in range(current_rows, fracture_count):
                    new_data.append({"fracture_id": i + 1})

            return dash.no_update, new_data

        return dash.no_update, dash.no_update

    @app.callback(
        Output("open-msg-dialog", "data", allow_duplicate=True),
        Input("show-fcd-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def show_fcd_modal(n_clicks):
        if n_clicks is None:
            return dash.no_update
    
        # Здесь подставьте реальные значения Fcd (пока заглушка)
        fcd_message = (
            "Fcd = 1.23\n"
            "Fcd (min) = 0.90\n"
            "Fcd (max) = 1.80\n"
            "Calculated based on current fracture parameters."
        )
    
        return {
            "title": "Fcd Values",
            "message": fcd_message,
            "type": MessageType.INFO.name,  # → "INFO"
            "buttons": ["Close"],
        }
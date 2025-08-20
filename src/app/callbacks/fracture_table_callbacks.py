from dash import (
    Output,
    Input,
    State,
)


def register(app):

    # Callback to update fracture table when count changes
    @app.callback(
        Output("fracture-table", "data"),
        Input("fracture-count", "value"),
        State("fracture-table", "data"),
    )
    def update_fracture_table(fracture_count, current_data):
        if fracture_count is None or fracture_count < 1:
            return []

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
                new_data.append(
                    {
                        "fracture_id": i + 1,
                    }
                )

        return new_data

import dash
from dash import (
    Output,
    Input,
    State,
)

from src.core.models.message_level import MessageLevel


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
        Output("message-request", "data", allow_duplicate=True),
        Input("show-fcd-button", "n_clicks"),
        State("fracture-table", "data"),
        State("reservoir-params-store", "data"),
        prevent_initial_call=True,
    )
    def show_fcd_modal(n_clicks, fracture_data, reservoir_data):
        if n_clicks is None:
            return dash.no_update

        if not fracture_data or not reservoir_data:
            return {
                "title": "Missing Data",
                "message": "Fracture or reservoir data not available.",
                "type": "WARNING",
                "buttons": ["OK"],
            }

        try:
            res_perm = float(reservoir_data.get("permeability", 0.1))
            if res_perm <= 0:
                raise ValueError("Reservoir permeability must be > 0")
        except (TypeError, ValueError):
            return {
                "title": "Invalid Reservoir Data",
                "message": "Reservoir permeability is missing or invalid.",
                "type": MessageLevel.ERROR.label,
                "buttons": ["OK"],
            }

        fcd_lines = []
        for row in fracture_data:
            try:
                frac_id = row["fracture_id"]
                k_f = float(row["permeability"])  # проницаемость трещины
                w_f = float(row["width"])  # ширина трещины
                l_plus = float(row["length_plus"])
                l_minus = float(row["length_minus"])
                l_f = l_plus + l_minus  # общая длина трещины

                if l_f <= 0:
                    return {
                        "title": "Invalid Fracture Data",
                        "message": f"Fracture {frac_id} length is negative",
                        "type": MessageLevel.ERROR.label,
                        "buttons": ["OK"],
                    }
                if w_f <= 0:
                    return {
                        "title": "Invalid Fracture Data",
                        "message": f"Fracture {frac_id} width is negative",
                        "type": MessageLevel.ERROR.label,
                        "buttons": ["OK"],
                    }
                if k_f <= 0:
                    return {
                        "title": "Invalid Fracture Data",
                        "message": f"Fracture {frac_id} permeability is negative",
                        "type": MessageLevel.ERROR.label,
                        "buttons": ["OK"],
                    }
                fcd_val = (k_f * w_f) / (res_perm * l_f)
                fcd_val = round(fcd_val, 1)
            except (TypeError, ValueError, KeyError) as e:
                return {
                    "title": "Invalid Fracture Data",
                    "message": f"Fracture {frac_id} {str(e)} is incorrect",
                    "type": MessageLevel.ERROR.label,
                    "buttons": ["OK"],
                }

            fcd_lines.append(f"Fracture {frac_id}: Fcd = {fcd_val}")

        message = "\n".join(fcd_lines)
        return {
            "title": "Dimensionless Fracture Conductivity (Fcd)",
            "message": message,
            "type": MessageLevel.INFO.label,
            "buttons": ["Close"],
        }

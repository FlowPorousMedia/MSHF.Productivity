import csv
import datetime
import io
import uuid

from dash import Input, Output, no_update, html, dash_table, dcc, State, MATCH
from dash.dash_table.Format import Format
import dash_bootstrap_components as dbc

from src.app.i18n import _, set_language
from src.app.services.translator_helpers import with_language
from src.core.models.result_data.result_type_enum import ResultTypeEnum


def register(app):
    # Callback to update table
    @app.callback(
        Output("table-container", "children"),
        Input("solver-result-store", "data"),
        prevent_initial_call=True,
    )
    def update_table_content(solver_result):
        if solver_result is None:
            return no_update

        # Получаем и преобразуем тип результата
        try:
            calc_result = solver_result.get("result")
            if calc_result != None:
                result_type_value = calc_result.get("result_type")
                result_type = ResultTypeEnum(result_type_value)
        except (ValueError, TypeError):
            return __render_unknown_result(result_type_value)

        if calc_result != None:
            models = calc_result.get("models", [])

        if not models:
            return html.Div(_("No results available"), className="alert alert-info")

        # Обработка разных типов результатов с помощью match-case
        match result_type:
            case ResultTypeEnum.SIMPLE:
                return __render_simple_result(models)
            case ResultTypeEnum.PARAMETRIC:
                return __render_parametric_result(models)
            case ResultTypeEnum.MAP:
                return __render_map_result(models)
            case _:
                return __render_unknown_result(result_type.value)

    # Добавляем callback для обработки скачивания
    @app.callback(
        Output({"type": "download-parametric-csv", "index": MATCH}, "data"),
        Input({"type": "btn-download-parametric-csv", "index": MATCH}, "n_clicks"),
        State({"type": "parametric-data-store", "index": MATCH}, "data"),
        prevent_initial_call=True,
    )
    def download_csv(n_clicks, stored_data):
        """Генерация и скачивание CSV файла"""
        if not stored_data or not stored_data.get("models"):
            return None

        models = stored_data["models"]
        param_caption = stored_data.get("param_caption", _("Parameter"))

        # Создаем CSV в памяти
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)

        # Заголовки столбцов
        headers = [param_caption] + [
            m.get("name", f"Model {i+1}") for i, m in enumerate(models)
        ]
        writer.writerow(headers)

        # Получаем количество строк (берем из первой модели)
        n_rows = len(models[0]["param1_values"]) if models else 0

        # Записываем данные
        for i in range(n_rows):
            row = [models[0]["param1_values"][i]]  # Значение параметра
            for model in models:
                # Добавляем Q-значение для каждой модели
                row.append(model["q_values"][i] if i < len(model["q_values"]) else "")
            writer.writerow(row)

        # Формируем имя файла с текущей датой
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"parametric_results_{timestamp}.csv"

        # Возвращаем файл для скачивания
        return dict(content=csv_buffer.getvalue(), filename=filename)

    # Вспомогательные функции для рендеринга разных типов результатов
    def __render_simple_result(models: list) -> html.Div:
        """Рендеринг таблицы для SIMPLE результата в транспонированном виде"""
        # Создаем столбцы: первый столбец для заголовков строк
        columns = [{"name": "Models", "id": "row_header", "type": "text"}]

        # Добавляем столбцы для каждой модели
        for i, model in enumerate(models):
            columns.append(
                {
                    "name": model["name"],
                    "id": f"col_{i}",
                    "type": "numeric",
                    "format": Format(precision=1, scheme="f"),
                }
            )

        # Создаем данные для таблицы
        data = [
            {
                "row_header": _("Q, m³/day"),
                **{
                    f"col_{i}": (
                        model["q_values"][0] if model.get("q_values") else None
                    )
                    for i, model in enumerate(models)
                },
            }
        ]

        # Создаем таблицу
        table = dash_table.DataTable(
            id="results-table-simple",
            columns=columns,
            data=data,
            style_table={"overflowX": "auto", "width": "100%"},
            style_cell={"textAlign": "center", "padding": "10px", "minWidth": "150px"},
            style_header={
                "backgroundColor": "rgb(230, 230, 230)",
                "fontWeight": "bold",
                "textAlign": "center",
            },
            style_data_conditional=[
                {
                    "if": {"column_id": "row_header"},
                    "backgroundColor": "rgb(245, 245, 245)",
                    "fontWeight": "bold",
                }
            ],
        )

        return html.Div([html.H4(_("Flow Rate Table"), className="mb-3"), table])

    def __render_parametric_result(models: list) -> html.Div:
        """
        Рендеринг таблицы для PARAMETRIC результата
        """

        # Проверка наличия моделей и данных
        if (
            not models
            or not models[0].get("param1_values")
            or not models[0].get("q_values")
        ):
            return html.Div(
                [
                    html.H4(_("Parametric Results Table"), className="mb-3"),
                    html.Div(
                        _("No parametric data available for display"),
                        className="alert alert-warning",
                    ),
                ]
            )

        # Получаем заголовок параметра из первой модели
        param_caption = models[0].get("param1_capt", "Parameter 1")

        # Создаем заголовки столбцов
        headers = [html.Th(param_caption, className="fw-bold")]
        for model in models:
            model_name = model.get("name", _("Unnamed Model"))
            headers.append(html.Th(model_name, className="fw-bold"))

        # Создаем строки таблицы
        rows = []
        base_length = len(models[0]["param1_values"])
        for i in range(base_length):
            # Ячейка со значением параметра
            param_value = models[0]["param1_values"][i]
            row_cells = [
                html.Td(
                    f"{param_value:.4f}"
                    if isinstance(param_value, float)
                    else str(param_value)
                )
            ]

            # Ячейки со значениями Q для каждой модели
            for model in models:
                q_value = model["q_values"][i]
                if q_value is None:
                    # Создаем пустую ячейку для None
                    row_cells.append(html.Td(""))
                else:
                    row_cells.append(
                        html.Td(
                            f"{q_value:.4f}"
                            if isinstance(q_value, float)
                            else str(q_value)
                        )
                    )

            rows.append(html.Tr(row_cells, className="border-top"))

        # Создаем таблицу
        table = dbc.Table(
            [
                html.Thead(html.Tr(headers, className="table-primary")),
                html.Tbody(rows),
            ],
            bordered=True,
            hover=True,
            responsive=True,
            striped=True,
            className="mt-4",
        )

        component_id = str(uuid.uuid4())

        # Создаем кнопку скачивания
        download_button = dbc.Button(
            _("Download CSV"),
            id={"type": "btn-download-parametric-csv", "index": component_id},
            color="success",
            className="mt-3",
        )

        # Компонент для скачивания
        download_component = dcc.Download(
            id={"type": "download-parametric-csv", "index": component_id}
        )

        # Сохраняем данные в dcc.Store для использования в callback
        data_store = dcc.Store(
            id={"type": "parametric-data-store", "index": component_id},
            data={"models": models, "param_caption": param_caption},
        )

        return [
            html.Div(
                [
                    html.H4(_("Parametric Results Table"), className="mb-3"),
                    html.Div(_("Q, m³/day"), className="mt-2 text-end fw-light"),
                    table,
                    download_button,
                    download_component,
                    data_store,
                ],
                className="border rounded p-3 bg-white",
                id={"type": "parametric-result-container", "index": component_id},
            )
        ]

    def __render_map_result(models: list) -> html.Div:
        """Рендеринг таблицы для MAP результата"""
        # Пока заглушка
        return html.Div(
            [
                html.H4(_("Map Results"), className="mb-3"),
                html.Div(
                    _("Map results display is under development"),
                    className="alert alert-info",
                ),
            ]
        )

    def __render_unknown_result(result_type: int) -> html.Div:
        """Рендеринг для неизвестного типа результата"""
        return html.Div(
            [
                html.H4(_("Results"), className="mb-3"),
                html.Div(
                    _("Result type '{result_type}' is not supported").format(
                        result_type=result_type
                    ),
                    className="alert alert-danger",
                ),
            ]
        )

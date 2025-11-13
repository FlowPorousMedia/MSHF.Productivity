from dash import Input, Output, no_update, dcc, html
import plotly.graph_objects as go
from src.app.i18n import _
from src.core.models.init_data.calc_over_param_enum import CalcParamTypeEnum
from src.core.models.result_data.result_type_enum import ResultTypeEnum


def register(app):
    # Callback to update graph
    @app.callback(
        Output("graph-container", "children"),
        Input("solver-result-store", "data"),
        prevent_initial_call=True,
    )
    def update_graph_content(solver_result):
        if solver_result is None:
            return no_update

        # Проверяем наличие данных
        if not solver_result:
            return no_update

        try:
            # Извлекаем данные результата
            calc_result = solver_result.get("result")
            if calc_result is not None:
                result_type_value = calc_result.get("result_type")
                result_type = ResultTypeEnum(result_type_value)
                models = calc_result.get("models", [])
            else:
                models = []
        except (ValueError, TypeError):
            return __render_unknown_graph(_("Invalid result format"))

        # Обработка разных типов результатов
        match result_type:
            case ResultTypeEnum.SIMPLE:
                if models:
                    return __render_simple_graph(models)
                else:
                    return __render_no_data_graph()
            case ResultTypeEnum.PARAMETRIC:
                return __render_parametric_graph(models)
            case ResultTypeEnum.MAP:
                return __render_map_graph(models)
            case _:
                return __render_unknown_graph(
                    _("Unsupported result type: {result_type_value}").format(
                        result_type_value=result_type_value
                    )
                )

    # Вспомогательные функции для рендеринга графиков
    def __render_simple_graph(models: list) -> html.Div:
        """
        Рендеринг столбчатой диаграммы для SIMPLE результата
        """

        # Подготавливаем данные для графика
        model_names = [
            model.get("name", _("Model {index}").format(index=i + 1))
            for i, model in enumerate(models)
        ]
        q_values = [model.get("q_values", [None])[0] for model in models]

        # Создаем фигуру
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=model_names,
                y=q_values,
                text=q_values,
                texttemplate="%{text:.1f}",
                textposition="outside",
                marker_color="rgb(55, 83, 109)",
                opacity=0.8,
            )
        )

        # Настраиваем оформление
        fig.update_layout(
            title=_("Flow Rate Comparison"),
            title_x=0.5,
            xaxis_title=_("Models"),
            yaxis_title=_("Q, m³/day"),
            plot_bgcolor="white",
            showlegend=False,
            margin=dict(l=40, r=40, t=60, b=40),
        )

        # Настраиваем оси
        # fig.update_xaxes(tickangle=-45)
        fig.update_yaxes(
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="gray",
            rangemode="tozero",  # Гарантирует, что график начинается с 0
            range=[
                0,
                max(q_values) * 1.2 if max(q_values) > 0 else 10,
            ],  # Добавляем 20% сверху
        )

        return html.Div(
            [html.H4(_("Flow Rate Plot"), className="mb-3"), dcc.Graph(figure=fig)]
        )

    def __render_parametric_graph(models: list) -> html.Div:
        """Рендеринг для PARAMETRIC результата"""

        # Если нет моделей для отображения
        if not models:
            return html.Div(
                [
                    html.H4(_("Parametric Results Plot"), className="mb-3"),
                    html.Div(
                        _("No data available for parametric visualization"),
                        className="alert alert-warning",
                    ),
                ]
            )

        # Создаем график
        fig = go.Figure()

        # Счетчик валидных моделей
        valid_models_count = 0

        first_model = models[0]
        param1_type_value = first_model.get("param1_type_value")
        if param1_type_value is not None:
            try:
                param_type = CalcParamTypeEnum(param1_type_value)
                x_title = param_type.label
                is_log_x = param_type == CalcParamTypeEnum.FRACT_PERM
            except ValueError:
                x_title = _("Parameter")
                is_log_x = False
        else:
            x_title = _("Parameter")
            is_log_x = False

        for model in models:
            qs = model.get("q_values")
            ps1 = model.get("param1_values")
            model_name = model.get("name")

            # Проверяем наличие необходимых данных
            if qs is None or ps1 is None or len(qs) == 0 or len(ps1) == 0:
                continue

            fig.add_trace(
                go.Scatter(
                    x=ps1,
                    y=qs,
                    mode="lines+markers",
                    name=model_name or _("Unnamed Model"),
                    hoverinfo="x+y+name",
                    hovertemplate=(
                        f"<b>{model_name or ''}</b><br>"
                        f"{x_title}: %{{x}}<br>"
                        "Q: %{y}<extra></extra>"
                    ),
                )
            )
            valid_models_count += 1

        # Если не найдено ни одной валидной модели
        if valid_models_count == 0:
            return html.Div(
                [
                    html.H4(_("Parametric Results Plot"), className="mb-3"),
                    html.Div(
                        _("No valid data available for parametric visualization"),
                        className="alert alert-warning",
                    ),
                ]
            )

        fig.update_layout(
            title=_("Parametric Analysis"),
            xaxis_title=x_title,
            yaxis_title=_("Q, m³/day"),
            legend_title=_("Models"),
            hovermode="closest",
            template="plotly_white",
            height=600,
            margin={"t": 60, "b": 60, "l": 60, "r": 30},
            showlegend=True,
        )

        if is_log_x:
            fig.update_xaxes(type="log", gridcolor="#f0f0f0", tickformat=".0f")
        else:
            fig.update_xaxes(gridcolor="#f0f0f0", tickformat=".0f")
        fig.update_yaxes(gridcolor="#f0f0f0", tickformat=".0f")

        return html.Div(
            [
                html.H4(_("Parametric Results Plot"), className="mb-3"),
                dcc.Graph(
                    figure=fig,
                    config={"displayModeBar": True},
                    className="border rounded p-2 bg-white",
                ),
            ]
        )

    def __render_map_graph(models: list) -> html.Div:
        """Рендеринг для MAP результата"""
        return html.Div(
            [
                html.H4(_("Map Results"), className="mb-3"),
                html.Div(
                    _(
                        "Map visualization is under development and will be available in a future release"
                    ),
                    className="alert alert-info",
                ),
            ]
        )

    def __render_no_data_graph() -> html.Div:
        """Рендеринг при отсутствии данных"""
        return html.Div(
            [
                html.H4(_("Results Graph"), className="mb-3"),
                html.Div(
                    _("No data available for visualization"),
                    className="alert alert-warning",
                ),
            ]
        )

    def __render_unknown_graph(message: str) -> html.Div:
        """Рендеринг для неизвестных ошибок"""
        return html.Div(
            [
                html.H4(_("Results Graph"), className="mb-3"),
                html.Div(
                    _("Error: {message}").format(message=message),
                    className="alert alert-danger",
                ),
            ]
        )

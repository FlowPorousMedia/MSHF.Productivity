from typing import Dict, List
import dash_svg as svg
from dash import html


def create_task_scheme_component(L: float, R: float, fracts: List[Dict]) -> List:
    """Создает SVG компонент для Dash"""
    elements = __create_elements(L, R, fracts)

    return html.Div(
        [
            html.H5("Scheme", style={"textAlign": "center", "marginBottom": "10px"}),
            html.Div(  # Обертка для responsive поведения
                svg.Svg(
                    id="scheme-svg",
                    width="100%",
                    height="100%",  # 100% от родительского контейнера
                    viewBox="0 0 300 200",  # Добавляем viewBox для сохранения пропорций
                    preserveAspectRatio="xMidYMid meet",  # Сохраняем пропорции
                    children=elements,
                ),
                style={
                    "width": "100%",
                    "height": "200px",  # Фиксируем высоту контейнера
                    "border": "0px solid #ddd",
                    "borderRadius": "4px",
                    "backgroundColor": "white",
                },
            ),
        ],
        style={"width": "100%"},
    )


def __create_elements(L: float, R: float, fracts: List[Dict]) -> List:
    """
    Создает элементы SVG на основе параметров
    fracts: список словарей [{"pos": x, "len_plus": l, "len_minus": lm, "width": w}]
    """
    if fracts is None:
        fracts = []

    # Размеры области для масштабирования
    total_width = L + 2 * R  # Длина скважины + дренирование слева и справа
    total_height = 2 * R  # Дренирование сверху и снизу

    # Размеры SVG контейнера
    svg_width = 300
    svg_height = 200

    padding = 20

    # Масштабирующие коэффициенты (нормируем на большую сторону)
    scale_factor = min(
        (svg_width - 2 * padding) / total_width,  # Учитываем отступы слева и справа
        (svg_height - 2 * padding) / total_height,  # Учитываем отступы сверху и снизу
    )

    # Смещение - начинаем отрисовку с отступов
    offset_x = padding
    offset_y = padding

    # Элементы SVG
    elements = []

    # Область дренирования (прямоугольник)
    drain_x = offset_x
    drain_y = offset_y
    drain_width = total_width * scale_factor
    drain_height = total_height * scale_factor

    elements.append(
        svg.Rect(
            x=drain_x,
            y=drain_y,
            width=drain_width,
            height=drain_height,
            fill="none",
            stroke="black",
            strokeWidth="1",
        )
    )

    # Горизонтальная скважина
    well_start_x = offset_x + R * scale_factor  # Начинается после левого дренирования
    well_end_x = well_start_x + L * scale_factor
    well_y = offset_y + total_height * scale_factor / 2  # Центр по вертикали

    elements.append(
        svg.Line(
            x1=well_start_x,
            y1=well_y,
            x2=well_end_x,
            y2=well_y,
            stroke="blue",
            strokeWidth="3",
        )
    )

    # Трещины
    for i, fracture in enumerate(fracts):
        pos = fracture.get("pos", 0)
        len_plus = fracture.get("len_plus", 50)
        len_minus = fracture.get("len_minus", 50)

        if pos is None or len_plus is None or len_minus is None:
            continue

        # Преобразуем в float на случай если пришли строки
        try:
            pos = float(pos)
            len_plus = float(len_plus)
            len_minus = float(len_minus)
        except (TypeError, ValueError):
            continue

        # Позиция трещины вдоль скважины (относительно начала скважины)
        fracture_x = well_start_x + pos * scale_factor

        # Верхняя и нижняя точки трещины
        fracture_top_y = well_y - len_plus * scale_factor
        fracture_bottom_y = well_y + len_minus * scale_factor

        elements.extend(
            [
                # Линия трещины (двусторонняя)
                svg.Line(
                    x1=fracture_x,
                    y1=fracture_top_y,
                    x2=fracture_x,
                    y2=fracture_bottom_y,
                    stroke="red",
                    strokeWidth="2",
                ),
            ]
        )

        label_y = fracture_bottom_y + 15  # Отступ 15px ниже трещины
        elements.append(
            svg.Text(
                x=str(fracture_x),
                y=str(label_y),
                children=str(i + 1),  # Индекс начинается с 1
                fill="darkred",
                fontSize="12",
                fontWeight="bold",
                textAnchor="middle",  # Выравнивание по центру
            )
        )

    return elements

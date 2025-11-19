from typing import Dict
from dash import html, dcc
import dash_bootstrap_components as dbc

from src.app.i18n import _


def model_info_to_html(model_data: Dict):
    model = model_data["metadata"]
    children = [
        # html.H4(model["name"], className="mb-3"),
        # Библиографическая ссылка
        html.H5(_("Citation")),
        model_citation_to_html(model["citation"]),
        html.Hr(),
        # Описание модели
        html.H5(_("Abstract")),
        html.P(model["abstract"], className="model-abstract"),
        html.Hr(),
        # Параметры модели
        html.H5(_("Model specification")),
        dbc.Row(
            [
                html.P(model["description"], className="model-description"),
                dbc.Col(
                    [
                        html.Dt(_("Application")),
                        html.Dd(__list_to_html(model["parameters"]["applicability"])),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Dt(_("Limitations")),
                        html.Dd(__list_to_html(model["parameters"]["limitations"])),
                    ],
                    width=6,
                ),
            ],
            className="mb-3",
        ),
    ]
    # Кнопка для публикации
    if model.get("citation", {}).get("doi") or model.get("citation", {}).get("url"):
        # Determine the link - prioritize DOI if available
        link = (
            f'https://doi.org/{model["citation"]["doi"]}'
            if model["citation"].get("doi")
            else model["citation"].get("url")
        )
        children.append(
            dbc.Button(
                [html.I(className="fas fa-book me-2"), _("Source")],
                href=link,
                target="_blank",
                color="primary",
                className="mt-3",
            )
        )

    return html.Div(children)


def model_citation_to_html(bibtex):
    entry_type = bibtex["entry_type"]
    html_parts = []

    # Авторы
    authors = bibtex["author"].replace(" and ", ", ")
    html_parts.append(html.Strong(authors))
    html_parts.append(". ")

    # Название
    html_parts.append(html.Em(f'"{bibtex["title"]}"'))
    html_parts.append(". ")

    # В зависимости от типа публикации
    if entry_type == "inproceedings":
        html_parts.append(f"{bibtex['conference']}. ")
        if "city" in bibtex:
            html_parts.append(f"{bibtex['city']}. ")
        if "date" in bibtex:
            html_parts.append(f"{bibtex['date']}. ")

    elif entry_type == "article":
        html_parts.append(html.Strong(bibtex["journal"]))
        html_parts.append(". ")
        if "volume" in bibtex:
            html_parts.append(f"{bibtex['volume']}")
            if "number" in bibtex:
                html_parts.append(f"({bibtex['number']})")
            html_parts.append(": ")
        if "pages" in bibtex:
            html_parts.append(f"{bibtex['pages']}. ")
        html_parts.append(f"{bibtex['year']}. ")

    # DOI (если есть)
    if "doi" in bibtex:
        html_parts.append(f"doi: {bibtex['doi']}")

    return html.Div(html_parts, className="citation")


def __list_to_html(limitations):
    if isinstance(limitations, list):
        return html.Ul([html.Li(item) for item in limitations])
    return limitations

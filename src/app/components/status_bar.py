from dash import html, dcc
import dash_bootstrap_components as dbc


def create_status_bar():
    """Создает статусную панель в стиле WinForms"""
    return html.Div(
        id="status-bar",
        style={
            "position": "fixed",
            "bottom": 0,
            "height": "25px",
            "backgroundColor": "#f8f9fa",
            "borderTop": "1px solid #dee2e6",
            "borderBottom": "1px solid #dee2e6",
            "display": "flex",
            "alignItems": "center",
            "padding": "0 10px",
            "fontSize": "12px",
            "boxSizing": "border-box",
            "width": "100%",
            "gap": "10px",
            "zIndex": 1050,
        },
        children=[
            # Status text
            html.Span(
                id="status-text",
                children="Ready for calculation",
                style={
                    "flex": "0 0 auto",
                    "whiteSpace": "nowrap",
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                    "minWidth": "150px",
                },
            ),
            # Progress bar (hidden by default)
            html.Div(
                id="progress-wrapper",
                style={
                    "display": "none",
                    "flex": "0 0 auto",
                    "alignItems": "center",
                    "marginLeft": "10px",
                },
                children=[
                    dbc.Progress(
                        id="calculation-progress",
                        value=0,
                        max=100,
                        striped=True,
                        animated=True,
                        style={
                            "height": "12px",
                            "width": "400px",
                            "marginRight": "10px",
                        },
                    ),
                    html.Span(
                        id="progress-percent",
                        children="0%",
                        style={"fontSize": "10px", "minWidth": "40px"},
                    ),
                ],
            ),
        ],
    )

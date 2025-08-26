from dash import html
import dash_bootstrap_components as dbc

from src.app._version import SOFTWARE_TITLE, USER_VERSION


def create_about_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(f"About {SOFTWARE_TITLE}"),
            dbc.ModalBody(
                [
                    html.H4(
                        [
                            html.Span(
                                "MSHF.Productivity", style={"font-weight": "bold"}
                            ),
                            " is a powerful Productivity Evaluation Tool for Multistage Fractured Horizontal Wells (MSHF)",
                        ]
                    ),
                    html.P(f"Version {USER_VERSION}"),
                    # html.P(
                    #     "Analytics Pro is a powerful data analysis and visualization tool designed for professionals."
                    # ),
                    # html.P("Features include:"),
                    # html.Ul(
                    #     [
                    #         html.Li("Interactive data exploration"),
                    #         html.Li("Advanced visualization capabilities"),
                    #         html.Li("Real-time collaboration"),
                    #         html.Li("Export to multiple formats"),
                    #     ]
                    # ),
                    # html.P("For support, please contact: support@analyticspro.com"),
                ]
            ),
            dbc.ModalFooter(dbc.Button("Close", id="close-about", className="ms-auto")),
        ],
        id="about-modal",
        size="lg",
    )

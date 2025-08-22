from dash import html
import dash_bootstrap_components as dbc

# About Modal
about_modal = dbc.Modal(
    [
        dbc.ModalHeader("About Analytics Pro"),
        dbc.ModalBody(
            [
                html.H4("Version 1.0"),
                html.P(
                    "Analytics Pro is a powerful data analysis and visualization tool designed for professionals."
                ),
                html.P("Features include:"),
                html.Ul(
                    [
                        html.Li("Interactive data exploration"),
                        html.Li("Advanced visualization capabilities"),
                        html.Li("Real-time collaboration"),
                        html.Li("Export to multiple formats"),
                    ]
                ),
                html.P("For support, please contact: support@analyticspro.com"),
            ]
        ),
        dbc.ModalFooter(dbc.Button("Close", id="close-about", className="ml-auto")),
    ],
    id="about-modal",
    size="lg",
)

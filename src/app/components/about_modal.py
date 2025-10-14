from dash import html
import dash_bootstrap_components as dbc

from src.app._version import SOFTWARE_TITLE, USER_VERSION


def create_about_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(f"About {SOFTWARE_TITLE} (v.{USER_VERSION})"),
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
                    html.P(
                        "This software tool enables petroleum engineers to rapidly forecast production rates for multistage "
                        "fractured horizontal wells. It utilizes analytical modeling to perform steady-state flow analysis, "
                        "providing a quick and efficient solution for well performance evaluation."
                    ),
                    # Authors section
                    html.H5(
                        "Authors", style={"margin-top": "20px", "margin-bottom": "10px"}
                    ),
                    html.Ul(
                        [
                            html.Li(
                                [
                                    html.A(
                                        "Marsel Khamidullin",
                                        href="https://www.researchgate.net/profile/Marsel-Khamidullin",
                                        target="_blank",
                                    )
                                ]
                            ),
                            html.Li(
                                [
                                    html.A(
                                        "Constantin Potashev",
                                        href="https://www.researchgate.net/profile/Konstantin-Potashev",
                                        target="_blank",
                                    )
                                ]
                            ),
                        ]
                    ),
                    # License section
                    html.H5(
                        "License",
                        style={"margin-top": "20px", "margin-bottom": "10px"},
                    ),
                    html.P(
                        [
                            "© ",
                            html.A(
                                "FlowPorousMedia",
                                href="https://github.com/FlowPorousMedia/",
                                target="_blank",
                            ),
                            ", 2025. All rights reserved",
                        ]
                    ),
                    html.P(
                        [
                            "This project is distributed under the ",
                            html.A(
                                "MIT",
                                href="https://github.com/FlowPorousMedia/MSHF.Productivity/blob/main/LICENSE",
                                target="_blank",
                            ),
                        ]
                    ),
                    # Support section with GitHub Issues link
                    html.H5(
                         "Support",
                        style={"margin-top": "20px", "margin-bottom": "10px"},
                    ),
                    html.P(
                        [
                            "For support, please open an issue on ",
                            html.A(
                                "GitHub Issues",
                                href="https://github.com/FlowPorousMedia/MSHF.Productivity/issues",
                                target="_blank",
                            ),
                            ".",
                        ]
                    ),
                ]
            ),
            dbc.ModalFooter(dbc.Button("Close", id="close-about", className="ms-auto")),
        ],
        id="about-modal",
        size="lg",
    )

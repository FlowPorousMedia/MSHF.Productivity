from dash import html
import dash_bootstrap_components as dbc


def create_navbar():
    return dbc.Navbar(
        [
            # Left side: Software name
            html.A(
                dbc.Row(
                    [
                        # dbc.Col(html.Img(src="/assets/logo.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("MSHF.Productivity", className="ml-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            # Right side navigation items
            html.Div(
                [
                    dbc.NavbarToggler(id="navbar-toggler"),
                    dbc.Collapse(
                        dbc.Nav(
                            [
                                # GitHub link
                                dbc.NavItem(
                                    html.Div(
                                        [
                                            dbc.NavLink(
                                                html.I(
                                                    className="fab fa-github mr-1",
                                                    id="github-icon",
                                                ),
                                                href="https://github.com/FlowPorousMedia/MSHF.Productivity",
                                                target="_blank",
                                                style={"fontSize": "1.2rem"},
                                            ),
                                            dbc.Tooltip(
                                                id="github-tooltip",
                                                target="github-icon",
                                                placement="left",
                                            ),
                                        ]
                                    )
                                ),
                                # Language dropdown with flag
                                dbc.NavItem(
                                    html.Div(
                                        [
                                            dbc.DropdownMenu(
                                                [
                                                    dbc.DropdownMenuItem(
                                                        "Русский", id="lang-ru"
                                                    ),
                                                    dbc.DropdownMenuItem(
                                                        "English", id="lang-en"
                                                    ),
                                                ],
                                                label=html.I(
                                                    className="fas fa-language",
                                                    id="language-icon",
                                                ),  # Default flag icon
                                                nav=True,
                                                id="language-dropdown",
                                                align_end=True,
                                            ),
                                            dbc.Tooltip(
                                                id="language-tooltip",
                                                target="language-icon",
                                                placement="left",
                                            ),
                                        ]
                                    )
                                ),
                                # User Guide/Wiki link (icon only)
                                dbc.NavItem(
                                    html.Div(
                                        [
                                            dbc.NavLink(
                                                html.I(
                                                    className="fas fa-book",
                                                    id="guide-icon",
                                                ),
                                                href="https://github.com/FlowPorousMedia/MSHF.Productivity/wiki/Home-EN",
                                                target="_blank",
                                                style={"fontSize": "1.2rem"},
                                                id="guide-navlink",
                                            ),
                                            dbc.Tooltip(
                                                id="guide-tooltip",
                                                target="guide-icon",
                                                placement="left",
                                            ),
                                        ]
                                    )
                                ),
                                # About modal (icon only)
                                dbc.NavItem(
                                    html.Div(
                                        [
                                            dbc.NavLink(
                                                html.I(
                                                    className="fas fa-info-circle",
                                                    id="about-icon",
                                                ),
                                                id="about-link",
                                                style={"fontSize": "1.2rem"},
                                            ),
                                            dbc.Tooltip(
                                                id="about-tooltip",
                                                target="about-icon",
                                                placement="left",
                                            ),
                                        ]
                                    )
                                ),
                            ],
                            className="d-flex align-items-center",
                            navbar=True,
                        ),
                        id="navbar-collapse",
                        navbar=True,
                    ),
                ],
                className="ms-auto d-flex align-items-center",  # This pushes content to the right
            ),
        ],
        color="primary",
        dark=True,
        sticky="top",
    )

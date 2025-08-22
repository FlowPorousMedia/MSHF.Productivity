from dash import html
import dash_bootstrap_components as dbc


def create_nav_bar():
    return dbc.Navbar(
        [
            # Left side: Software name
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/logo.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("Analytics Pro", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/",
            ),
            # Right side navigation items
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [
                        # GitHub link
                        dbc.NavItem(
                            dbc.NavLink(
                                html.Span(
                                    [html.I(className="fab fa-github mr-1"), "GitHub"]
                                ),
                                href="https://github.com/yourusername/your-repo",
                                target="_blank",
                            )
                        ),
                        # About modal (will be implemented with callback)
                        dbc.NavItem(dbc.NavLink("About", id="about-link")),
                        # Language dropdown
                        dbc.DropdownMenu(
                            [
                                dbc.DropdownMenuItem("English", id="lang-en"),
                                dbc.DropdownMenuItem("Español", id="lang-es"),
                                dbc.DropdownMenuItem("Français", id="lang-fr"),
                                dbc.DropdownMenuItem("Deutsch", id="lang-de"),
                            ],
                            label="Language",
                            nav=True,
                        ),
                        # User Guide/Wiki link
                        dbc.NavItem(
                            dbc.NavLink(
                                html.Span(
                                    [html.I(className="fas fa-book mr-1"), "User Guide"]
                                ),
                                href="https://github.com/yourusername/your-repo/wiki",
                                target="_blank",
                            )
                        ),
                    ],
                    className="ml-auto",
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ],
        color="primary",
        dark=True,
        sticky="top",
    )

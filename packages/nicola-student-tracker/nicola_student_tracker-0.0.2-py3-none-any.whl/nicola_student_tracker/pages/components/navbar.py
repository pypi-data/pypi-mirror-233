import dash
from dash import html
import dash_bootstrap_components as dbc


# Define the navbar structure
def simple_navbar() -> html.Div:
    """Return the nav bar for the dash application."""
    layout = html.Div(
        [
            dbc.NavbarSimple(
                children=[
                    dbc.NavItem(dbc.NavLink(page["name"], href=page["relative_path"]))
                    for page in dash.page_registry.values()
                ],
                brand="Nicola Hearne",
                brand_href="/attendance",
                color="dark",
                dark=True,
            ),
        ]
    )

    return layout

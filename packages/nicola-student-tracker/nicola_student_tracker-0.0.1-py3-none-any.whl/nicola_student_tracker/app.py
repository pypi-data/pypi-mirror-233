# Import necessary libraries
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output


# Define the Dash App and it's properties here
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True,
)

from pages import about, subjects, overview
from pages.components import navbar

# define the navbar
nav = navbar.simple_navbar()

# Define the index page layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        nav,
        html.Div(id="page-content", children=[]),
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname: str) -> dbc.Container | str:
    """Display the specified page for the corresponding pathname.

    Args:
        pathname (str): Name of the page to display.

    Returns:
        result (dbc.Container | str): Container of the requested page, or a string message
         indicating a 404 error.

    """
    path_dict = {
        "/": subjects.layout,
        "/about": about.layout,
        "/subjects": subjects.layout,
        "/overview": overview.layout,
    }

    if layout := path_dict.get(pathname):
        return layout

    return "404 Page Error! Please choose a link"


# Run the app on localhost:8050
if __name__ == "__main__":
    app.run_server(debug=True)

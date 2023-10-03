import dash_bootstrap_components as dbc
from dash import html


subjects_card = dbc.Card(
    [
        dbc.CardBody([html.Center(html.H4("Track Students By Subject", className="card-title"))]),
        dbc.CardImg(src="assets/static/images/subjects.png", bottom=True),
    ],
    style={"width": "70rem", "margin-bottom": 25},
)

table_card = dbc.Card(
    [
        dbc.CardBody([html.Center(html.H4("View/Organise Statistics", className="card-title"))]),
        dbc.CardImg(src="assets/static/images/table_stats.png", top=False),
    ],
    style={"width": "70rem", "margin-bottom": 25},
)

overview_card = dbc.Card(
    [
        dbc.CardBody([html.Center(html.H4("Visualise Teaching Load  ", className="card-title"))]),
        dbc.CardImg(src="assets/static/images/overview.png", top=False),
    ],
    style={"width": "70rem", "margin-bottom": 25},
)

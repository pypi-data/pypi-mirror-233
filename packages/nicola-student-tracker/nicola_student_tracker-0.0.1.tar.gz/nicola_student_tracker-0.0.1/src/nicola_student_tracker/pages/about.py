# Import necessary libraries
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from pages.components.card import overview_card, subjects_card, table_card

dash.register_page(__name__, order=3)

layout = dbc.Container(
    [
        dbc.Row(
            [
                html.Center(html.H1("About")),
                html.Br(),
                html.Hr(),
                dbc.Col(
                    [
                        dcc.Markdown(
                            """
                            
                            Student tracker was designed to provide a visual and quantitative 
                            assessment of all students taught. By monitoring student performance 
                            over time it is possible to:
                            
                            * Spot potential issues early.
                            * Notice patterns (good and bad) that may exist.
                            * Gain a quantitative assessment of student performance.
                            * Be better equipped to remove any barriers to learning.
                            
                            Currently you can:
                            * View attendance for all students filtered by subject and date range.
                            * Organise student statistics by column values.
                            * Get an overview of teaching workload broken down by subject and 
                            days taught.
                            """
                        ),
                    ],
                    style={"margin-bottom": 25},
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(subjects_card, width="auto"),
            ],
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(table_card, width="auto"),
            ],
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(overview_card, width="auto"),
            ],
            justify="center",
        ),
    ]
)

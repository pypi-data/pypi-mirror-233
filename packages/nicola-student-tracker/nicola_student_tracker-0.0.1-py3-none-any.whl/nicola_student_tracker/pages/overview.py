import warnings

import dash
from dash import html
import dash_bootstrap_components as dbc

from resources.dash_logic import generate_subject_stats_dict, create_plots

warnings.simplefilter(action="ignore", category=FutureWarning)

dash.register_page(__name__, order=2)

# Generate necessary page statistics
subject_stats, days_taught, num_students, num_subjects = generate_subject_stats_dict()

layout = dbc.Container(
    [
        html.Br(),
        # Title
        dbc.Row(
            [
                html.Center(html.H1("Teaching Stats", id="student_title")),
            ],
            style={"margin-bottom": 25},
        ),
        # Teaching Stats
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Center(html.H3("Total Subjects")),
                        html.Center(html.H1(f"{num_subjects}")),
                    ],
                    style={"display": "row  ", "flexWrap": "wrap"},
                ),
                dbc.Col(
                    [
                        html.Center(html.H3("Days Teaching")),
                        html.Center(html.H1(f"{days_taught}")),
                    ],
                    style={"display": "row  ", "flexWrap": "wrap"},
                ),
                dbc.Col(
                    [
                        html.Center(html.H3("Total Students")),
                        html.Center(html.H1(f"{num_students}")),
                    ],
                    style={"display": "row  ", "flexWrap": "wrap"},
                ),
            ]
        ),
        # Line plots of student attendance by subject
        dbc.Row(create_plots(stats_dict=subject_stats)),
    ]
)

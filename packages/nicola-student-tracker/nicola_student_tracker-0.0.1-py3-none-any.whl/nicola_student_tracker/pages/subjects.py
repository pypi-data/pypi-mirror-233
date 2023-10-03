# Import necessary libraries
import os
import warnings
from datetime import datetime
from typing import Any

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Output, callback, dcc, Input, html, dash_table

from config import settings
from pages.components.table import table_conditionals
from resources.dash_logic import calculate_data_table
from resources.dataframe import (
    process_dataframes,
    group_students_by_day,
    xlsx_student_data_to_dataframe,
)

warnings.simplefilter(action="ignore", category=FutureWarning)

dash.register_page(__name__, order=1)

xl_file = pd.ExcelFile(os.path.join(settings.DATA_DIR, settings.FILE_NAME))

dfs = {sheet_name: xl_file.parse(sheet_name) for sheet_name in xl_file.sheet_names}

dfs = process_dataframes(dataframe_dict=dfs)

df = pd.DataFrame(
    {
        "name": ["one", "two", "three"],
        "total_lessons": [3, 3, 3],
        "attended_lessons": [1, 2, 3],
        "missed_lessons": [1, 2, 3],
        "total_minutes_missed": [1, 2, 3],
        "attendance_percentage": [1, 2, 3],
        "subject": ["Monday", "Monday", "Wednesday"],
    }
)

SUBJECTS = list(dfs.keys())

# Define the page layout
layout = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            [
                html.Center(html.H1("", id="title")),
            ],
            style={"margin-bottom": 25},
        ),
        # Row of dropdown menus
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.DropdownMenu(
                            children=[dbc.DropdownMenuItem(sub, id=sub) for sub in SUBJECTS],
                            label="Subject",
                            color="primary",
                            className="m-1",
                            id="subject_dropdown",
                        ),
                    ],
                    style={"display": "flex", "flexWrap": "wrap"},
                ),
                dbc.Col([]),
                dbc.Col(
                    [
                        dcc.DatePickerRange(
                            start_date=datetime(2023, 1, 1),
                            end_date=datetime(2099, 1, 1),
                            start_date_id="start_date",
                            end_date_id="end_date",
                            id="date_picker",
                            display_format="DD-MM-YYYY",
                        ),
                    ]
                ),
            ]
        ),
        # Line plots of student attendance
        dbc.Row(
            dcc.Graph(id="line-chart", figure={}, className="twelve columns"),
            id="plots",
        ),
        # Table of student statistics
        dbc.Row(
            html.Div(
                dash_table.DataTable(
                    data=df.to_dict("records"),
                    sort_action="native",
                    columns=[{"name": i, "id": i} for i in df.columns],
                    style_data_conditional=table_conditionals(),
                    style_as_list_view=True,
                    style_header={
                        "backgroundColor": "rgb(30, 30, 30)",
                        "color": "white",
                    },
                    style_cell={"textAlign": "center"},
                    id="data_table_plot",
                ),
                className="row",
                style={"margin-bottom": 50},
            )
        ),
    ]
)


@callback(
    [
        Output(component_id="title", component_property="children"),
        Output(component_id="plots", component_property="children"),
        Output("data_table_plot", "data"),
    ],
    Input("date_picker", "start_date"),
    Input("date_picker", "end_date"),
    [Input(component_id=sub, component_property="n_clicks") for sub in SUBJECTS],
)
def pick_data_by_subject(
    start_date: str, end_date: str, *args: Any
) -> tuple[str, dbc.Row, list[dict[str, str | int | float]]]:
    """Output subject related data.

    Args:
        start_date (str): Earliest date filter.
        end_date (str): Latest date filter.
        args (tuple[Any]): Additional arguments from the dash context.

    Returns:
        data (tuple[subject, dbc.Row(plots), new_table_data]): Chosen subject name, plots of
        subject data, and table data for chosen subject.

    """
    ctx = dash.callback_context

    subject = ctx.triggered[0]["prop_id"].split(".")[0]

    if not subject or subject in ["date_picker", "start_date", "end_date"]:
        subject = SUBJECTS[0]

    # Get all student data for subject
    df = xlsx_student_data_to_dataframe(subject=subject)

    # Apply date range filter
    df = df[(df["date"] > start_date) & (df["date"] < end_date)]

    # Separate students according to days taught
    df_by_days = group_students_by_day(df=df)

    figures = {}

    for day, student_df in df_by_days.items():
        student_names = [
            col
            for col in student_df.columns
            if col not in ["date", "lesson time (minutes)", "day"]
        ]

        student_data_df = df[["date"] + student_names]
        student_data_df["date"] = [dt.date() for dt in student_data_df["date"]]
        student_data_df.set_index("date", inplace=True)
        fig = px.scatter(student_data_df, x=student_data_df.index, y=student_names)
        fig.update_layout(yaxis_range=[0, max(df["lesson time (minutes)"]) * 1.1])
        figures[day] = fig

    plots = []

    for day, fig in figures.items():
        fig.update_layout({"title": day, "legend_title_text": "Student Name"})
        plots.append(dcc.Graph(id="line-chart", figure=fig, className="twelve columns"))
    new_table_data = calculate_data_table(dfs)
    new_table_data = [row for row in new_table_data if row["subject"] == subject]
    return subject, dbc.Row(plots), new_table_data

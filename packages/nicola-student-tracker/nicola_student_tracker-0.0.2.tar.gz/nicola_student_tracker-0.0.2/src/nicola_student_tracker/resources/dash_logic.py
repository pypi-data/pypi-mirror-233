import os
from typing import Any

import pandas as pd
from dash import dcc

from config import settings
from resources.dataframe import xlsx_student_data_to_dataframe, group_students_by_day


def calculate_data_table(
    dataframe_dict: dict[str, pd.DataFrame]
) -> list[dict[str, str | int | float]]:
    """Generate list of dicts for data data_table info.

    Args:
        dataframe_dict (dict[str, pd.DataFrame]): Dict of key(day)-value(DataFrame) pairs
        relating to student info for a particular subject.

    Returns:
        student_data (list[dict[str, str | int | float]]): List of dictionaries representing
        statistics for a particular student.

    """
    student_data = []

    for subject, df in dataframe_dict.items():
        student_names = [
            col for col in df.columns if col not in ["date", "lesson time (minutes)", "day"]
        ]
        for name in student_names:
            temp_df = df[["date", "lesson time (minutes)", name]]
            temp_df = temp_df[temp_df[name].notna()]
            missed_lessons = sum(temp_df[name] == 0)
            total_lessons = len(temp_df)
            total_minutes = sum(temp_df["lesson time (minutes)"])
            total_minutes_missed = sum(temp_df["lesson time (minutes)"]) - sum(temp_df[name])

            student_data.append(
                {
                    "name": name,
                    "total_lessons": len(temp_df),
                    "missed_lessons": sum(temp_df[name] == 0),
                    "attended_lessons": total_lessons - missed_lessons,
                    "total_minutes_missed": total_minutes - sum(temp_df[name]),
                    "attendance_percentage": 100
                    - round(100 * (total_minutes_missed / total_minutes), 2),
                    "subject": subject,
                }
            )

    return student_data


def generate_subject_stats_dict() -> tuple[dict[str, dict[str, Any]], int, int, int]:
    """Generate stats objects related to all subjects taught.

    Reads the .xlsx file and generates statistics related to student data.

    Returns
        stats (tuple[dict[str, dict[str, Any]], int, int, int]): dict of subject stats, number of
        days taught, number of students taught, number of subjects taught.
    """
    xl_file = pd.ExcelFile(os.path.join(settings.DATA_DIR, settings.FILE_NAME))

    dfs_dict = {sheet_name: xl_file.parse(sheet_name) for sheet_name in xl_file.sheet_names}

    # dfs = process_dataframes(dataframe_dict=dfs_dict)

    subjects = list(dfs_dict.keys())

    subject_stats: dict[str, Any] = {}

    num_students = 0
    total_student_hours = 0
    total_missed_time = 0
    total_missed_days = 0
    days_taught = set()

    for subject in subjects:
        df = xlsx_student_data_to_dataframe(subject=subject)
        df_by_days = group_students_by_day(df=df)

        subject_stats[subject] = {}

        for day, subject_df in df_by_days.items():
            days_taught.add(day)
            day_student_hours = 0
            day_missed_time = 0
            day_missed_days = 0
            day_num_students = 0

            subject_stats[subject][day] = {}
            student_names = [
                name
                for name in subject_df.columns
                if name not in ["date", "lesson time (minutes)", "day"]
            ]

            day_num_students += len(student_names)
            num_students += len(student_names)

            for name in student_names:
                temp_df = subject_df[["lesson time (minutes)", name]].copy()
                temp_df.dropna(inplace=True)

                # Number of potential teaching minutes student could have attended
                teaching_minutes = round(sum(temp_df["lesson time (minutes)"]), 2)

                # Number of teaching minutes missed by student
                total_minutes = temp_df["lesson time (minutes)"] - temp_df[name]
                missing_minutes = round(sum(total_minutes), 2)

                # Days student did not attend
                missed_days = sum(temp_df[name] == 0)

                attendance_percentage = round(
                    100 * (1 - ((missing_minutes / teaching_minutes))), 2
                )

                subject_stats[subject][day][name] = {
                    "day": day,
                    "teaching_minutes": teaching_minutes,
                    "missed_days": missed_days,
                    "missed_minutes": missing_minutes,
                    "attendance_percentage": attendance_percentage,
                }

                day_missed_time += missing_minutes
                day_student_hours += sum(temp_df["lesson time (minutes)"])
                day_missed_days += missed_days

                total_missed_time += missing_minutes
                total_student_hours += sum(temp_df["lesson time (minutes)"])
                total_missed_days += missed_days

            subject_stats[subject][day]["total_missed_time"] = day_missed_time
            subject_stats[subject][day]["total_student_hours"] = day_student_hours
            subject_stats[subject][day]["total_missed_days"] = day_missed_days
            subject_stats[subject][day]["total_students"] = day_num_students

    subject_stats["total_missed_time"] = total_missed_time
    subject_stats["total_student_hours"] = total_student_hours
    subject_stats["total_missed_days"] = total_missed_days

    return subject_stats, len(days_taught), num_students, len(subjects)


def create_plots(stats_dict: dict[str, dict[str, Any]]) -> list[dcc.Graph]:
    """Create plots for each subject by day taught.

    Args:
        stats_dict (dict[str, Any]): Dictionary of student data split by days taught.

    Returns:
        plots (list[Graph]): list of plots.

    """
    plots = []

    for subject, day_dicts in stats_dict.items():
        if subject in ["total_missed_time", "total_student_hours", "total_missed_days"]:
            continue

        data = []
        for day, info_dict in day_dicts.items():
            absent_pct = info_dict["total_missed_time"] / info_dict["total_student_hours"]
            absent_pct = round(100 * (1 - absent_pct), 2)

            data.append(
                {
                    "x": ["Attendance"],
                    "y": [absent_pct],
                    "type": "bar",
                    "name": day,
                }
            )

        graph = dcc.Graph(
            figure={
                "data": data,
                "layout": {"title": subject, "yaxis": {"range": [0, 100]}},
            },
        )
        plots.append(graph)

    return plots

import os

import pandas as pd

from config import settings


def add_day_of_week_column(df: pd.DataFrame) -> pd.DataFrame:
    """Add corresponding week day column to DataFrame.

    Expects existing column 'date' with datetime format YYYY-mm-dd.

    Args:
        df (pd.DataFrame): DataFrame of subject.

    Returns:
        df (pd.DataFrame): Original dataframe with new 'day' column.

    """
    dates = pd.to_datetime(df["date"], format="%d-%m-%Y")

    df["day"] = [dt.strftime("%A") for dt in dates]

    return df


def process_dataframes(dataframe_dict: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Preprocessing of dataframes.

    Steps include:
        1. Converting all column names to lower-case.
        2. Adding a 'day' column.

    Args:
        dataframe_dict (dict[str, pd.DataFrame]): Student info by subject separated into days.

    Returns:
        data_dict (dict[str, pd.DataFrame]): Processed student info.

    """
    data_dict = {}

    for sheet_name, df in dataframe_dict.items():
        df.columns = df.columns.str.lower()
        data_dict[sheet_name] = add_day_of_week_column(df=df)

    return data_dict


def group_students_by_day(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Group students into separate DataFrames according to the day they are taught.

    Args:
        df (pd.DataFrame): DataFrame of students by subject taught.

    Returns:
        df_by_days (dict[str, pd.DataFrame]): Dict of day, dataframe pairs for each day taught.
    """
    df_by_days = {}

    for day in df["day"].unique():
        # Group students by day
        temp_df = df[df["day"] == day].copy()

        # Remove students never in on those days
        temp_df.dropna(axis=1, how="all", inplace=True)

        df_by_days[day] = temp_df

    return df_by_days


def xlsx_student_data_to_dataframe(subject: str) -> pd.DataFrame:
    """Return DataFrame of student data given a subject.

    Args:
        subject (str): Lesson subject.

    Returns:
        dataframe (pd.DataFrame): DataFrame of student info relating to subject specified.

    """
    xl_file = pd.ExcelFile(os.path.join(settings.DATA_DIR, settings.FILE_NAME))

    dfs = {sheet_name: xl_file.parse(sheet_name) for sheet_name in xl_file.sheet_names}

    dfs = process_dataframes(dataframe_dict=dfs)

    return dfs[subject]

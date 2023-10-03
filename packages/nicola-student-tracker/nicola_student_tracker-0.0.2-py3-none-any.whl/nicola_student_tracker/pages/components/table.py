from config import settings


condition_dict = dict[str, str | dict[str, str | list[str]]]


def table_conditionals() -> list[condition_dict]:
    """Conditional statements for dash table.

    Returns
        conditionals (list[dict]): Conditional statements for dash table.
    """
    return [
        {
            "if": {
                "filter_query": f"{{attendance_percentage}} >= {settings.ATTENDANCE_GREEN}",
                "column_id": ["name", "attendance_percentage"],
            },
            "color": settings.COLOUR_GREEN_RGB,
        },
        {
            "if": {
                "filter_query": f"{{attendance_percentage}} >= {settings.ATTENDANCE_AMBER} && "
                f"{{attendance_percentage}} < {settings.ATTENDANCE_GREEN}",
                "column_id": ["name", "attendance_percentage"],
            },
            "color": settings.COLOUR_AMBER_RGB,
        },
        {
            "if": {
                "filter_query": f"{{attendance_percentage}} < {settings.ATTENDANCE_AMBER}",
                "column_id": ["name", "attendance_percentage"],
            },
            "color": settings.COLOUR_RED_RGB,
        },
    ]

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".config"))


class BaseConfig(BaseSettings):
    """Object to hold project level configuration."""

    BASE_DIR: str = os.path.dirname(os.path.realpath(__file__))
    DATA_DIR: str = os.path.join(os.getcwd(), "data")
    FILE_NAME: str = "attendance.xlsx"

    # dashboard config

    # Attendance range colours
    ATTENDANCE_GREEN: float = 80
    ATTENDANCE_AMBER: float = 70

    # Attendance range to highlight
    COLOUR_GREEN_RGB: str = "rgb(0, 153, 51)"
    COLOUR_AMBER_RGB: str = "rgb(255, 102, 0)"
    COLOUR_RED_RGB: str = "rgb(255, 0, 0)"


settings = BaseConfig()

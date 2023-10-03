import os
import shutil
import sys

from config import settings


def start_dash() -> None:
    """CLI to start dash application."""
    try:
        user_input = sys.argv[1]
    except IndexError:
        print("To start the dashboard type 'nicola dashboard'")
        sys.exit(1)

    if user_input == "init":
        print("*" * 50)
        print("*" * 14, "Initialising project", "*" * 14)
        print("*" * 50)
        cwd = os.getcwd()

        if not os.path.isdir(os.path.join(cwd, "data")):
            os.mkdir(os.path.join(cwd, "data"))

        print("\n\t* Created data directory")
        shutil.copy(
            src=os.path.join(os.path.join(settings.BASE_DIR, "data", "attendance.xlsx")),
            dst=os.path.join(cwd, "data", "attendance.xlsx")
        )
        print("\t* Copied example .xlsx file")
        shutil.copy(
            src=os.path.join(settings.BASE_DIR, "README.md"),
            dst=os.path.join(cwd, "README.md")
        )
        print("\t* Copied README.md")
        shutil.copy(
            src=os.path.join(settings.BASE_DIR, ".config"),
            dst=os.path.join(cwd, ".config")
        )
        print("\t* Copied .config file\n")

        print("*" * 50)
        print("*" * 13, "Project Setup Complete", "*" * 13)
        print("*" * 50)
        print("\n-  To start the dashboard type 'nicola dashboard'")
        print("-  Please Read 'README.md' for full instructions.\n")
        sys.exit(1)

    if user_input != "dashboard":
        print("To start the dashboard type 'nicola dashboard'")
        sys.exit(1)

    os.system(f"python {os.path.join(settings.BASE_DIR, 'app.py')}")

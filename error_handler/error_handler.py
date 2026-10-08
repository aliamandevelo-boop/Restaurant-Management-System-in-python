import os
from datetime import datetime



BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

LOG_DIR = os.path.join(BASE_DIR, "logs")
ERROR_FILE = os.path.join(LOG_DIR, "error.log")



def create_log_folder():

    try:

        os.makedirs(LOG_DIR, exist_ok=True)

    except Exception:
        pass

def log_error(error_message):

    try:

        create_log_folder()

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            ERROR_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write("\n")
            file.write("========================================\n")
            file.write("ZAYKA RESTAURANT MANAGEMENT SYSTEM\n")
            file.write("ERROR LOG\n")
            file.write("========================================\n")
            file.write("Date & Time : " + current_time + "\n")
            file.write("Error       : " + str(error_message) + "\n")
            file.write("========================================\n")

    except Exception:
        pass



def log_message(message):

    try:

        create_log_folder()

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            ERROR_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                current_time
                + " - "
                + str(message)
                + "\n"
            )

    except Exception:
        pass


def create_log_file():

    try:

        create_log_folder()

        if not os.path.exists(ERROR_FILE):

            with open(
                ERROR_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    "ZAYKA RESTAURANT MANAGEMENT SYSTEM\n"
                )

                file.write(
                    "ERROR LOG FILE\n"
                )

                file.write(
                    "========================================\n"
                )

    except Exception:
        pass



create_log_file()
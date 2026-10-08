import json
import os
import maskpass
from datetime import datetime


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE_DIR = os.path.join(BASE_DIR, "database")
LOG_DIR = os.path.join(BASE_DIR, "logs")

ADMIN_FILE = os.path.join(DATABASE_DIR, "admin.json")
STAFF_FILE = os.path.join(DATABASE_DIR, "staff.json")
ERROR_FILE = os.path.join(LOG_DIR, "error.log")


def create_folders():

    os.makedirs(DATABASE_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)


def log_error(error_message):

    create_folders()

    try:

        with open(ERROR_FILE, "a", encoding="utf-8") as file:

            date_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            file.write(
                f"[{date_time}] {error_message}\n"
            )

    except Exception:
        pass



def create_admin():

    create_folders()

    admin_data = {
        "username": "amanali",
        "password": "291769"
    }

    try:

       
        if not os.path.exists(ADMIN_FILE):

            with open(
                ADMIN_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    admin_data,
                    file,
                    indent=4
                )

    except Exception as error:

        log_error(
            f"Admin file error: {error}"
        )


def create_staff_file():

    create_folders()

    try:

        if not os.path.exists(STAFF_FILE):

            with open(
                STAFF_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )

    except Exception as error:

        log_error(
            f"Staff file error: {error}"
        )



def admin_login():

    create_admin()

    print("\n========== ADMIN LOGIN ==========")

    username = input(
        "Enter Admin Username: "
    ).strip()

    if username == "":

        print("Username cannot be empty!")

        return False

    try:

        password = maskpass.askpass(
            prompt="Enter Admin Password: "
        )

        if password == "":

            print("Password cannot be empty!")

            return False

        with open(
            ADMIN_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            admin_data = json.load(file)

        if (
            username == admin_data["username"]
            and password == admin_data["password"]
        ):

            print(
                "\nAdmin Login Successful!"
            )

            return True

        print(
            "\nInvalid username or password!"
        )

        return False

    except ValueError as error:

        log_error(
            f"Admin login input error: {error}"
        )

        print(
            "Invalid input! Please try again."
        )

        return False

    except Exception as error:

        log_error(
            f"Admin login error: {error}"
        )

        print(
            "Something went wrong. "
            "Error has been logged."
        )

        return False


def staff_login():

    create_staff_file()

    print("\n========== STAFF LOGIN ==========")

    try:

        username = input(
            "Enter Staff Username: "
        ).strip()

        if username == "":

            print(
                "Username cannot be empty!"
            )

            return False

        password = maskpass.askpass(
            prompt="Enter Staff Password: "
        )

        if password == "":

            print(
                "Password cannot be empty!"
            )

            return False

        with open(
            STAFF_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            staff_data = json.load(file)

        for staff in staff_data:

            if (
                staff["username"] == username
                and staff["password"] == password
            ):

                print(
                    "\nStaff Login Successful!"
                )

                print(
                    f"Welcome, {staff['name']}!"
                )

                return True

        print(
            "\nInvalid username or password!"
        )

        return False

    except ValueError as error:

        log_error(
            f"Staff login input error: {error}"
        )

        print(
            "Invalid input! Please try again."
        )

        return False

    except Exception as error:

        log_error(
            f"Staff login error: {error}"
        )

        print(
            "Something went wrong. "
            "Error has been logged."
        )

        return False



def logout():

    print(
        "\nLogout successful. Goodbye!"
    )
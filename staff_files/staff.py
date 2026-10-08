import json
import os
from datetime import datetime


# ==============================
# BASE DIRECTORY
# ==============================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DATABASE_DIR = os.path.join(BASE_DIR, "database")
LOG_DIR = os.path.join(BASE_DIR, "logs")

STAFF_FILE = os.path.join(DATABASE_DIR, "staff.json")
ERROR_FILE = os.path.join(LOG_DIR, "error.log")


# ==============================
# CREATE FOLDERS
# ==============================

def create_folders():

    try:

        os.makedirs(DATABASE_DIR, exist_ok=True)
        os.makedirs(LOG_DIR, exist_ok=True)

    except Exception as error:

        log_error(error)


# ==============================
# ERROR LOG
# ==============================

def log_error(error_message):

    try:

        os.makedirs(LOG_DIR, exist_ok=True)

        with open(ERROR_FILE, "a", encoding="utf-8") as file:

            file.write("\n")
            file.write("========================================\n")

            file.write(
                "DATE & TIME: "
                + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                + "\n"
            )

            file.write(
                "ERROR: "
                + str(error_message)
                + "\n"
            )

            file.write("========================================\n")

    except Exception:

        pass


# ==============================
# CREATE STAFF JSON FILE
# ==============================

def create_staff_file():

    try:

        create_folders()

        if not os.path.exists(STAFF_FILE):

            with open(
                STAFF_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump([], file, indent=4)

    except Exception as error:

        log_error(error)


# ==============================
# READ STAFF
# ==============================

def read_staff():

    try:

        create_staff_file()

        with open(
            STAFF_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            staff_data = json.load(file)

        if not isinstance(staff_data, list):

            return []

        return staff_data

    except Exception as error:

        log_error(error)

        print("\nUnable to read staff data.")

        return []


# ==============================
# SAVE STAFF
# ==============================

def save_staff(staff_data):

    try:

        create_folders()

        with open(
            STAFF_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                staff_data,
                file,
                indent=4
            )

        return True

    except Exception as error:

        log_error(error)

        print("\nUnable to save staff data.")

        return False


# ==============================
# VIEW STAFF
# ==============================

def view_staff():

    try:

        staff_data = read_staff()

        print("\n")
        print("========== STAFF LIST ==========")

        if len(staff_data) == 0:

            print("No staff registered.")
            return

        for staff in staff_data:

            print("\nStaff ID      :", staff.get("id"))
            print("Name          :", staff.get("name"))
            print("Username      :", staff.get("username"))
            print("Role          :", staff.get("role"))
            print("--------------------------------")

    except Exception as error:

        log_error(error)

        print("\nUnable to display staff.")


# ==============================
# ADD STAFF
# ==============================

def add_staff():

    try:

        staff_data = read_staff()

        print("\n")
        print("========== ADD STAFF ==========")

        # NAME
        name = input(
            "Enter staff name: "
        ).strip()

        if name == "":

            print("Name cannot be empty.")
            return

        # USERNAME
        username = input(
            "Enter username: "
        ).strip()

        if username == "":

            print("Username cannot be empty.")
            return

        # CHECK DUPLICATE USERNAME
        for staff in staff_data:

            old_username = staff.get(
                "username",
                ""
            )

            if old_username.lower() == username.lower():

                print(
                    "This username already exists."
                )

                return

        # PASSWORD
        password = input(
            "Enter password: "
        ).strip()

        if password == "":

            print("Password cannot be empty.")
            return

        # CONFIRM PASSWORD
        confirm_password = input(
            "Confirm password: "
        ).strip()

        if password != confirm_password:

            print("Passwords do not match.")
            return

        # CREATE NEW ID
        highest_id = 0

        for staff in staff_data:

            try:

                staff_id = int(
                    staff.get("id", 0)
                )

                if staff_id > highest_id:

                    highest_id = staff_id

            except (ValueError, TypeError):

                continue

        new_id = highest_id + 1

        # NEW STAFF
        new_staff = {

            "id": new_id,

            "name": name,

            "username": username,

            "password": password,

            "role": "Staff"

        }

        staff_data.append(new_staff)

        # SAVE
        if save_staff(staff_data):

            print("\nStaff added successfully.")

            print(
                "Staff ID :",
                new_id
            )

            print(
                "Username :",
                username
            )

    except Exception as error:

        log_error(error)

        print("\nUnable to add staff.")


# ==============================
# REMOVE STAFF
# ==============================

def remove_staff():

    try:

        staff_data = read_staff()

        print("\n")
        print("========== REMOVE STAFF ==========")

        if len(staff_data) == 0:

            print("No staff available.")
            return

        view_staff()

        staff_id_input = input(
            "\nEnter Staff ID to remove: "
        ).strip()

        if staff_id_input == "":

            print("Staff ID cannot be empty.")
            return

        try:

            staff_id = int(
                staff_id_input
            )

        except ValueError:

            print(
                "Invalid input! Please enter a number."
            )

            return

        found_staff = None

        for staff in staff_data:

            try:

                if int(
                    staff.get("id", 0)
                ) == staff_id:

                    found_staff = staff
                    break

            except (ValueError, TypeError):

                continue

        if found_staff is None:

            print("Staff ID not found.")
            return

        print(
            "\nStaff Name :",
            found_staff.get("name")
        )

        print(
            "Username   :",
            found_staff.get("username")
        )

        confirm = input(
            "Are you sure you want to remove this staff? (yes/no): "
        ).strip().lower()

        if confirm != "yes":

            print(
                "Staff removal cancelled."
            )

            return

        staff_data.remove(found_staff)

        if save_staff(staff_data):

            print(
                "Staff removed successfully."
            )

    except Exception as error:

        log_error(error)

        print("\nUnable to remove staff.")


# ==============================
# STAFF MANAGEMENT
# ==============================

def staff_management():

    try:

        create_staff_file()

        while True:

            print("\n")
            print("========== STAFF MANAGEMENT ==========")

            print("1. Add Staff")
            print("2. View Staff")
            print("3. Remove Staff")
            print("4. Back")

            choice = input(
                "Enter choice: "
            ).strip()

            if choice == "1":

                add_staff()

            elif choice == "2":

                view_staff()

            elif choice == "3":

                remove_staff()

            elif choice == "4":

                print(
                    "Returning to Admin Panel..."
                )

                break

            else:

                print(
                    "Invalid choice. Please try again."
                )

    except Exception as error:

        log_error(error)

        print("\nSomething went wrong.")
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "error.log")


def log_error(error):

    try:

        os.makedirs(LOG_DIR, exist_ok=True)

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(LOG_FILE, "a", encoding="utf-8") as file:

            file.write(
                f"[{current_time}] ERROR: {error}\n"
            )

    except Exception:
        pass

from user_auth_files.auth import (
    create_folders,
    create_admin,
    create_staff_file,
    admin_login,
    staff_login
)


from menu_files.menu import (
    menu_management,
    view_menu
)


from order_files.order import order_management
from billing_files.billing import billing_management
from inventory_files.inventory import inventory_management
from table_booking_files.table import table_management
from staff_files.staff import staff_management



def admin_panel():

    while True:

        try:

            print("\n")
            print("==========================================")
            print("       ZAYKA RESTAURANT & HOTEL")
            print("             ADMIN PANEL")
            print("==========================================")
            print("1. Menu Management")
            print("2. Order Management")
            print("3. Billing")
            print("4. Inventory Management")
            print("5. Table Booking")
            print("6. Staff Management")
            print("7. Logout")
            print("==========================================")

            choice = input("Enter choice: ").strip()

            if choice == "1":

                menu_management()

            elif choice == "2":

                order_management()

            elif choice == "3":

                billing_management()

            elif choice == "4":

                inventory_management()

            elif choice == "5":

                table_management()

            elif choice == "6":

                staff_management()

            elif choice == "7":

                print("\nAdmin logged out successfully.")
                break

            else:

                print("\nInvalid choice. Please try again.")

        except Exception as error:

            log_error(error)

            print(
                "\nSomething went wrong. "
                "Error has been logged."
            )




def staff_panel():

    while True:

        try:

            print("\n")
            print("==========================================")
            print("       ZAYKA RESTAURANT & HOTEL")
            print("             STAFF PANEL")
            print("==========================================")
            print("1. View Menu")
            print("2. Order Management")
            print("3. Table Booking")
            print("4. Logout")
            print("==========================================")

            choice = input("Enter choice: ").strip()

            if choice == "1":

                view_menu()

            elif choice == "2":

                order_management()

            elif choice == "3":

                table_management()

            elif choice == "4":

                print("\nStaff logged out successfully.")
                break

            else:

                print("\nInvalid choice. Please try again.")

        except Exception as error:

            log_error(error)

            print(
                "\nSomething went wrong. "
                "Error has been logged."
            )


def admin_login_display():

    try:

        print("\n")
        print("==========================================")
        print("             ADMIN LOGIN")
        print("==========================================")

        if admin_login():

            print("\nAdmin login successful.")

            admin_panel()

        else:

            print("\nInvalid username or password.")

    except Exception as error:

        log_error(error)

        print(
            "\nSomething went wrong. "
            "Error has been logged."
        )

def staff_login_display():

    try:

        print("\n")
        print("==========================================")
        print("             STAFF LOGIN")
        print("==========================================")

        if staff_login():

            print("\nStaff login successful.")

            staff_panel()

        else:

            print("\nInvalid username or password.")

    except Exception as error:

        log_error(error)

        print(
            "\nSomething went wrong. "
            "Error has been logged."
        )


def display():

    try:

    
        os.makedirs(LOG_DIR, exist_ok=True)

    
        create_folders()
        create_admin()
        create_staff_file()

        while True:

            print("\n")
            print("==========================================")
            print("       WELCOME TO ZAYKA")
            print("       RESTAURANT & HOTEL")
            print("==========================================")
            print("1. Admin Login")
            print("2. Staff Login")
            print("3. Exit")
            print("==========================================")

            choice = input("Enter choice: ").strip()

            if choice == "1":

                admin_login_display()

            elif choice == "2":

                staff_login_display()

            elif choice == "3":

                print(
                    "\nThank you for using "
                    "Velmora Restaurant & Hotel."
                )

                print("Goodbye!")

                break

            else:

                print("\nInvalid choice. Please try again.")

    except Exception as error:

        log_error(error)

        print(
            "\nSomething went wrong. "
            "Error has been logged."
        )
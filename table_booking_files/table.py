import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE_DIR = os.path.join(BASE_DIR, "database")
LOG_DIR = os.path.join(BASE_DIR, "logs")

TABLE_FILE = os.path.join(
    DATABASE_DIR,
    "tables.json"
)

ERROR_FILE = os.path.join(
    LOG_DIR,
    "error.log"
)


def create_folders():

    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    os.makedirs(
        LOG_DIR,
        exist_ok=True
    )



def log_error(error_message):

    create_folders()

    try:

        with open(
            ERROR_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            date_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            file.write(
                f"[{date_time}] {error_message}\n"
            )

    except Exception:
        pass


def create_table_file():

    create_folders()

    try:

        if not os.path.exists(TABLE_FILE):

            table_data = [

                {
                    "table_id": 1,
                    "table_number": 1,
                    "capacity": 2,
                    "status": "Available",
                    "customer_name": "",
                    "phone": "",
                    "booking_date": "",
                    "booking_time": ""
                },

                {
                    "table_id": 2,
                    "table_number": 2,
                    "capacity": 2,
                    "status": "Available",
                    "customer_name": "",
                    "phone": "",
                    "booking_date": "",
                    "booking_time": ""
                },

                {
                    "table_id": 3,
                    "table_number": 3,
                    "capacity": 4,
                    "status": "Available",
                    "customer_name": "",
                    "phone": "",
                    "booking_date": "",
                    "booking_time": ""
                },

                {
                    "table_id": 4,
                    "table_number": 4,
                    "capacity": 4,
                    "status": "Available",
                    "customer_name": "",
                    "phone": "",
                    "booking_date": "",
                    "booking_time": ""
                },

                {
                    "table_id": 5,
                    "table_number": 5,
                    "capacity": 6,
                    "status": "Available",
                    "customer_name": "",
                    "phone": "",
                    "booking_date": "",
                    "booking_time": ""
                },

                {
                    "table_id": 6,
                    "table_number": 6,
                    "capacity": 6,
                    "status": "Available",
                    "customer_name": "",
                    "phone": "",
                    "booking_date": "",
                    "booking_time": ""
                },

                {
                    "table_id": 7,
                    "table_number": 7,
                    "capacity": 8,
                    "status": "Available",
                    "customer_name": "",
                    "phone": "",
                    "booking_date": "",
                    "booking_time": ""
                },

                {
                    "table_id": 8,
                    "table_number": 8,
                    "capacity": 10,
                    "status": "Available",
                    "customer_name": "",
                    "phone": "",
                    "booking_date": "",
                    "booking_time": ""
                }

            ]

            with open(
                TABLE_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    table_data,
                    file,
                    indent=4
                )

    except Exception as error:

        log_error(
            f"Table file creation error: {error}"
        )


def read_tables():

    create_table_file()

    try:

        with open(
            TABLE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as error:

        log_error(
            f"Table reading error: {error}"
        )

        return []



def save_tables(table_data):

    create_folders()

    try:

        with open(
            TABLE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                table_data,
                file,
                indent=4
            )

        return True

    except Exception as error:

        log_error(
            f"Table saving error: {error}"
        )

        return False


def view_tables():

    print("\n========== ZAYKA TABLES ==========")

    table_data = read_tables()

    if not table_data:

        print("No tables found.")
        return

    print("-" * 85)

    print(
        f"{'ID':<5}"
        f"{'TABLE':<10}"
        f"{'CAPACITY':<12}"
        f"{'STATUS':<15}"
        f"{'CUSTOMER':<20}"
        f"{'DATE':<15}"
    )

    print("-" * 85)

    for table in table_data:

        print(
            f"{table['table_id']:<5}"
            f"{table['table_number']:<10}"
            f"{table['capacity']:<12}"
            f"{table['status']:<15}"
            f"{table['customer_name']:<20}"
            f"{table['booking_date']:<15}"
        )

    print("-" * 85)


def book_table():

    print("\n========== BOOK TABLE ==========")

    table_data = read_tables()

    if not table_data:

        print("No tables available.")
        return

    try:

        
        print("\nAvailable Tables:")

        found_available = False

        for table in table_data:

            if table["status"] == "Available":

                found_available = True

                print(
                    f"Table {table['table_number']} "
                    f"- Capacity: "
                    f"{table['capacity']} persons"
                )

        if not found_available:

            print(
                "No table is currently available."
            )

            return

        table_number = int(
            input(
                "\nEnter table number: "
            )
        )

        selected_table = None

        for table in table_data:

            if table["table_number"] == table_number:

                selected_table = table
                break

        if selected_table is None:

            print("Table number not found!")
            return

        if selected_table["status"] == "Booked":

            print(
                "This table is already booked!"
            )

            return

        customer_name = input(
            "Enter customer name: "
        ).strip()

        if customer_name == "":

            print(
                "Customer name cannot be empty!"
            )

            return

        phone = input(
            "Enter phone number: "
        ).strip()

        if phone == "":

            print(
                "Phone number cannot be empty!"
            )

            return

        if not phone.isdigit():

            log_error(
                "Invalid phone number entered during table booking."
            )

            print(
                "Phone number must contain only numbers!"
            )

            return

        if len(phone) != 10:

            print(
                "Phone number must contain 10 digits!"
            )

            return

        booking_date = input(
            "Enter booking date (YYYY-MM-DD): "
        ).strip()

        if booking_date == "":

            print(
                "Booking date cannot be empty!"
            )

            return

        booking_time = input(
            "Enter booking time (HH:MM): "
        ).strip()

        if booking_time == "":

            print(
                "Booking time cannot be empty!"
            )

            return

        
        try:

            datetime.strptime(
                booking_date,
                "%Y-%m-%d"
            )

        except ValueError as error:

            log_error(
                f"Invalid booking date: {error}"
            )

            print(
                "Invalid date! Use YYYY-MM-DD."
            )

            return

        
        try:

            datetime.strptime(
                booking_time,
                "%H:%M"
            )

        except ValueError as error:

            log_error(
                f"Invalid booking time: {error}"
            )

            print(
                "Invalid time! Use HH:MM."
            )

            return

        selected_table["status"] = "Booked"

        selected_table["customer_name"] = (
            customer_name
        )

        selected_table["phone"] = phone

        selected_table["booking_date"] = (
            booking_date
        )

        selected_table["booking_time"] = (
            booking_time
        )

        if save_tables(table_data):

            print(
                "\nTable booked successfully!"
            )

            print(
                f"Table Number : "
                f"{selected_table['table_number']}"
            )

            print(
                f"Customer     : "
                f"{customer_name}"
            )

            print(
                f"Date         : "
                f"{booking_date}"
            )

            print(
                f"Time         : "
                f"{booking_time}"
            )

    except ValueError as error:

        log_error(
            f"Book table value error: {error}"
        )

        print(
            "Invalid input! Please enter a valid number."
        )

    except Exception as error:

        log_error(
            f"Book table error: {error}"
        )

        print(
            "Something went wrong. Error has been logged."
        )


def cancel_booking():

    print("\n========== CANCEL BOOKING ==========")

    table_data = read_tables()

    if not table_data:

        print("No tables found.")
        return

    view_tables()

    try:

        table_number = int(
            input(
                "\nEnter table number: "
            )
        )

        selected_table = None

        for table in table_data:

            if table["table_number"] == table_number:

                selected_table = table
                break

        if selected_table is None:

            print(
                "Table number not found!"
            )

            return

        if selected_table["status"] == "Available":

            print(
                "This table is not booked."
            )

            return

        confirm = input(
            "Cancel this booking? (yes/no): "
        ).strip().lower()

        if confirm != "yes":

            print(
                "Booking cancellation stopped."
            )

            return

        selected_table["status"] = "Available"

        selected_table["customer_name"] = ""

        selected_table["phone"] = ""

        selected_table["booking_date"] = ""

        selected_table["booking_time"] = ""

        if save_tables(table_data):

            print(
                "\nBooking cancelled successfully!"
            )

    except ValueError as error:

        log_error(
            f"Cancel booking value error: {error}"
        )

        print(
            "Invalid input! Please enter a valid table number."
        )

    except Exception as error:

        log_error(
            f"Cancel booking error: {error}"
        )

        print(
            "Something went wrong. Error has been logged."
        )



def booking_status():

    print("\n========== BOOKING STATUS ==========")

    table_data = read_tables()

    if not table_data:

        print("No tables found.")
        return

    try:

        table_number = int(
            input(
                "Enter table number: "
            )
        )

        selected_table = None

        for table in table_data:

            if table["table_number"] == table_number:

                selected_table = table
                break

        if selected_table is None:

            print(
                "Table number not found!"
            )

            return

        print("\n---------- TABLE STATUS ----------")

        print(
            f"Table Number : "
            f"{selected_table['table_number']}"
        )

        print(
            f"Capacity     : "
            f"{selected_table['capacity']} persons"
        )

        print(
            f"Status       : "
            f"{selected_table['status']}"
        )

        if selected_table["status"] == "Booked":

            print(
                f"Customer     : "
                f"{selected_table['customer_name']}"
            )

            print(
                f"Phone        : "
                f"{selected_table['phone']}"
            )

            print(
                f"Date         : "
                f"{selected_table['booking_date']}"
            )

            print(
                f"Time         : "
                f"{selected_table['booking_time']}"
            )

        print("----------------------------------")

    except ValueError as error:

        log_error(
            f"Booking status value error: {error}"
        )

        print(
            "Invalid input! Please enter a valid table number."
        )

    except Exception as error:

        log_error(
            f"Booking status error: {error}"
        )

        print(
            "Something went wrong. Error has been logged."
        )



def table_management():

    create_table_file()

    while True:

        print(
            "\n========== TABLE BOOKING =========="
        )

        print("1. View Tables")
        print("2. Book Table")
        print("3. Cancel Booking")
        print("4. Booking Status")
        print("5. Back")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            view_tables()

        elif choice == "2":

            book_table()

        elif choice == "3":

            cancel_booking()

        elif choice == "4":

            booking_status()

        elif choice == "5":

            print(
                "Returning to previous menu..."
            )

            break

        else:

            print(
                "Invalid choice! Please try again."
            )



create_table_file()
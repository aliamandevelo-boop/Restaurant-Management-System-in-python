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

MENU_FILE = os.path.join(DATABASE_DIR, "menu.json")
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


def create_menu_file():

    create_folders()

    if not os.path.exists(MENU_FILE):

        menu_data = [

            {
                "id": 1,
                "name": "Chicken Biryani",
                "category": "Asian",
                "full_price": 220,
                "half_price": 130
            },

            {
                "id": 2,
                "name": "Chicken Korma",
                "category": "Asian",
                "full_price": 240,
                "half_price": 140
            },

            {
                "id": 3,
                "name": "Chicken Nihari",
                "category": "Asian",
                "full_price": 250,
                "half_price": 150
            },

            {
                "id": 4,
                "name": "Chicken Handi",
                "category": "Asian",
                "full_price": 280,
                "half_price": 170
            },

            {
                "id": 5,
                "name": "Chicken Kebab",
                "category": "Asian",
                "full_price": 200,
                "half_price": 120
            },

            {
                "id": 6,
                "name": "Fried Rice",
                "category": "Asian",
                "full_price": 180,
                "half_price": 110
            },

            {
                "id": 7,
                "name": "Chicken Chow Mein",
                "category": "Asian",
                "full_price": 200,
                "half_price": 120
            },

            {
                "id": 8,
                "name": "Spring Rolls",
                "category": "Asian",
                "full_price": 150,
                "half_price": 90
            },

            {
                "id": 9,
                "name": "Chicken Burger",
                "category": "Western",
                "full_price": 180,
                "half_price": 110
            },

            {
                "id": 10,
                "name": "Chicken Pizza",
                "category": "Western",
                "full_price": 350,
                "half_price": 200
            },

            {
                "id": 11,
                "name": "Chicken Pasta",
                "category": "Western",
                "full_price": 250,
                "half_price": 150
            },

            {
                "id": 12,
                "name": "French Fries",
                "category": "Western",
                "full_price": 120,
                "half_price": 70
            },

            {
                "id": 13,
                "name": "Grilled Chicken",
                "category": "Western",
                "full_price": 320,
                "half_price": 190
            },

            {
                "id": 14,
                "name": "Chocolate Cake",
                "category": "Western",
                "full_price": 160,
                "half_price": 90
            },

            {
                "id": 15,
                "name": "Masala Chai",
                "category": "Drinks",
                "full_price": 60,
                "half_price": 35
            }

        ]

        try:
            with open(MENU_FILE, "w", encoding="utf-8") as file:
                json.dump(menu_data, file, indent=4)

        except Exception as error:
            log_error(f"Menu file creation error: {error}")



def read_menu():

    create_menu_file()

    try:
        with open(MENU_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as error:
        log_error(f"Menu read error: {error}")
        return []



def save_menu(menu_data):

    create_folders()

    try:
        with open(MENU_FILE, "w", encoding="utf-8") as file:
            json.dump(menu_data, file, indent=4)

        return True

    except Exception as error:
        log_error(f"Menu save error: {error}")
        return False



def view_menu():

    print("\n========== VELMORA MENU ==========")

    menu_data = read_menu()

    if not menu_data:
        print("Menu is empty.")
        return

    print("-" * 70)
    print(
        f"{'ID':<5}"
        f"{'ITEM':<25}"
        f"{'CATEGORY':<15}"
        f"{'FULL':<10}"
        f"{'HALF':<10}"
    )
    print("-" * 70)

    for item in menu_data:

        print(
            f"{item['id']:<5}"
            f"{item['name']:<25}"
            f"{item['category']:<15}"
            f"Rs.{item['full_price']:<7}"
            f"Rs.{item['half_price']:<7}"
        )

    print("-" * 70)


# ==============================
# ADD ITEM
# ==============================

def add_item():

    print("\n========== ADD MENU ITEM ==========")

    try:

        name = input("Enter food name: ").strip()

        if name == "":
            print("Food name cannot be empty!")
            return

        category = input(
            "Enter category (Asian/Western/Drinks): "
        ).strip()

        if category == "":
            print("Category cannot be empty!")
            return

        full_price = float(
            input("Enter full price: ")
        )

        if full_price <= 0:
            print("Price must be greater than 0!")
            return

        half_price = float(
            input("Enter half price: ")
        )

        if half_price <= 0:
            print("Price must be greater than 0!")
            return

        if half_price >= full_price:
            print("Half price should be less than full price!")
            return

        menu_data = read_menu()

        for item in menu_data:

            if item["name"].lower() == name.lower():
                print("This food item already exists!")
                return

        if menu_data:
            new_id = menu_data[-1]["id"] + 1
        else:
            new_id = 1

        new_item = {
            "id": new_id,
            "name": name,
            "category": category,
            "full_price": full_price,
            "half_price": half_price
        }

        menu_data.append(new_item)

        if save_menu(menu_data):
            print("\nFood item added successfully!")

    except ValueError as error:

        log_error(f"Add menu item value error: {error}")
        print("Invalid input! Please enter a valid number.")

    except Exception as error:

        log_error(f"Add menu item error: {error}")
        print("Something went wrong. Error has been logged.")


# ==============================
# UPDATE ITEM
# ==============================

def update_item():

    print("\n========== UPDATE MENU ITEM ==========")

    try:

        menu_data = read_menu()

        if not menu_data:
            print("Menu is empty.")
            return

        view_menu()

        item_id = int(
            input("Enter item ID to update: ")
        )

        found = False

        for item in menu_data:

            if item["id"] == item_id:

                found = True

                print("\nLeave input empty to keep old value.")

                name = input(
                    f"Food name [{item['name']}]: "
                ).strip()

                if name != "":
                    item["name"] = name

                category = input(
                    f"Category [{item['category']}]: "
                ).strip()

                if category != "":
                    item["category"] = category

                full_price = input(
                    f"Full price [{item['full_price']}]: "
                ).strip()

                if full_price != "":
                    full_price = float(full_price)

                    if full_price <= 0:
                        print("Price must be greater than 0!")
                        return

                    item["full_price"] = full_price

                half_price = input(
                    f"Half price [{item['half_price']}]: "
                ).strip()

                if half_price != "":
                    half_price = float(half_price)

                    if half_price <= 0:
                        print("Price must be greater than 0!")
                        return

                    item["half_price"] = half_price

                if item["half_price"] >= item["full_price"]:
                    print(
                        "Half price should be less than full price!"
                    )
                    return

                if save_menu(menu_data):
                    print("\nMenu item updated successfully!")

                break

        if not found:
            print("Item ID not found!")

    except ValueError as error:

        log_error(f"Update menu value error: {error}")
        print("Invalid input! Please enter a valid value.")

    except Exception as error:

        log_error(f"Update menu error: {error}")
        print("Something went wrong. Error has been logged.")


# ==============================
# DELETE ITEM
# ==============================

def delete_item():

    print("\n========== DELETE MENU ITEM ==========")

    try:

        menu_data = read_menu()

        if not menu_data:
            print("Menu is empty.")
            return

        view_menu()

        item_id = int(
            input("Enter item ID to delete: ")
        )

        found = False

        for item in menu_data:

            if item["id"] == item_id:

                found = True

                confirm = input(
                    f"Delete '{item['name']}'? (yes/no): "
                ).strip().lower()

                if confirm == "yes":

                    menu_data.remove(item)

                    if save_menu(menu_data):
                        print(
                            "\nMenu item deleted successfully!"
                        )

                else:
                    print("Delete operation cancelled.")

                break

        if not found:
            print("Item ID not found!")

    except ValueError as error:

        log_error(f"Delete menu value error: {error}")
        print("Invalid input! Please enter a valid item ID.")

    except Exception as error:

        log_error(f"Delete menu error: {error}")
        print("Something went wrong. Error has been logged.")


# ==============================
# MENU MANAGEMENT
# ==============================

def menu_management():

    create_menu_file()

    while True:

        print("\n========== MENU MANAGEMENT ==========")
        print("1. Add Item")
        print("2. View Items")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_item()

        elif choice == "2":
            view_menu()

        elif choice == "3":
            update_item()

        elif choice == "4":
            delete_item()

        elif choice == "5":
            print("Returning to previous menu...")
            break

        else:
            print("Invalid choice! Please try again.")


# ==============================
# FIRST RUN
# ==============================

create_menu_file()

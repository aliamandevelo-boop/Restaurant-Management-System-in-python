import json
import os
from datetime import datetime




BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)

INVENTORY_FILE = os.path.join(
    DATABASE_DIR,
    "inventory.json"
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

    try:

        create_folders()

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


def create_inventory_file():

    try:

        create_folders()

        if not os.path.exists(INVENTORY_FILE):

            inventory_data = [

                {
                    "id": 1,
                    "item_name": "Rice",
                    "quantity": 50,
                    "unit": "kg"
                },

                {
                    "id": 2,
                    "item_name": "Chicken",
                    "quantity": 30,
                    "unit": "kg"
                },

                {
                    "id": 3,
                    "item_name": "Cooking Oil",
                    "quantity": 20,
                    "unit": "litre"
                },

                {
                    "id": 4,
                    "item_name": "Flour",
                    "quantity": 25,
                    "unit": "kg"
                },

                {
                    "id": 5,
                    "item_name": "Tea",
                    "quantity": 10,
                    "unit": "kg"
                },

                {
                    "id": 6,
                    "item_name": "Sugar",
                    "quantity": 15,
                    "unit": "kg"
                }

            ]

            with open(
                INVENTORY_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    inventory_data,
                    file,
                    indent=4
                )

    except Exception as error:

        log_error(
            f"Inventory file creation error: {error}"
        )

        print(
            "Inventory file create nahi ho saki."
        )


def read_inventory():

    create_inventory_file()

    try:

        with open(
            INVENTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except Exception as error:

        log_error(
            f"Inventory read error: {error}"
        )

        print(
            "Inventory data read nahi ho saka."
        )

        return []


def save_inventory(inventory_data):

    try:

        create_folders()

        with open(
            INVENTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                inventory_data,
                file,
                indent=4
            )

        return True

    except Exception as error:

        log_error(
            f"Inventory save error: {error}"
        )

        return False


def view_stock():

    print(
        "\n========== CURRENT STOCK =========="
    )

    inventory_data = read_inventory()

    if not inventory_data:

        print("Stock is empty.")

        return

    print("-" * 60)

    print(
        f"{'ID':<5}"
        f"{'ITEM NAME':<25}"
        f"{'QUANTITY':<15}"
        f"{'UNIT':<10}"
    )

    print("-" * 60)

    for item in inventory_data:

        print(
            f"{item['id']:<5}"
            f"{item['item_name']:<25}"
            f"{item['quantity']:<15}"
            f"{item['unit']:<10}"
        )

    print("-" * 60)

def add_stock():

    print(
        "\n========== ADD STOCK =========="
    )

    try:

        item_name = input(
            "Enter item name: "
        ).strip()

        if item_name == "":

            print(
                "Item name cannot be empty!"
            )

            return

        quantity = float(
            input("Enter quantity: ")
        )

        if quantity <= 0:

            print(
                "Quantity must be greater than 0!"
            )

            return

        unit = input(
            "Enter unit (kg/litre/packet/piece): "
        ).strip()

        if unit == "":

            print(
                "Unit cannot be empty!"
            )

            return

        inventory_data = read_inventory()

        
        for item in inventory_data:

            if (
                item["item_name"].lower()
                == item_name.lower()
            ):

                print(
                    "This item already exists!"
                )

                print(
                    "Use Update Stock to change quantity."
                )

                return

        
        if inventory_data:

            new_id = max(
                item["id"]
                for item in inventory_data
            ) + 1

        else:

            new_id = 1

        new_item = {

            "id": new_id,

            "item_name": item_name,

            "quantity": quantity,

            "unit": unit

        }

        inventory_data.append(
            new_item
        )

        if save_inventory(
            inventory_data
        ):

            print(
                "\nStock added successfully!"
            )

        else:

            print(
                "Stock save nahi ho saka."
            )

    except ValueError as error:

        log_error(
            f"Add stock value error: {error}"
        )

        print(
            "Invalid quantity! Please enter a number."
        )

    except Exception as error:

        log_error(
            f"Add stock error: {error}"
        )

        print(
            "Something went wrong."
        )


def update_stock():

    print(
        "\n========== UPDATE STOCK =========="
    )

    try:

        inventory_data = read_inventory()

        if not inventory_data:

            print(
                "Stock is empty."
            )

            return

        view_stock()

        item_id = int( 
            input(
                "Enter item ID to update: "
            )
        )

        found = False

        for item in inventory_data:

            if item["id"] == item_id:

                found = True

                print(
                    "\nLeave input empty to keep old value."
                )

                item_name = input(
                    f"Item name [{item['item_name']}]: "
                ).strip()

                if item_name != "":

                    item["item_name"] = item_name

                quantity = input(
                    f"Quantity [{item['quantity']}]: "
                ).strip()

                if quantity != "":

                    quantity = float(
                        quantity
                    )

                    if quantity <= 0:

                        print(
                            "Quantity must be greater than 0!"
                        )

                        return

                    item["quantity"] = quantity

                unit = input(
                    f"Unit [{item['unit']}]: "
                ).strip()

                if unit != "":

                    item["unit"] = unit

                if save_inventory(
                    inventory_data
                ):

                    print(
                        "\nStock updated successfully!"
                    )

                else:

                    print(
                        "Stock update nahi ho saka."
                    )

                break

        if not found:

            print(
                "Item ID not found!"
            )

    except ValueError as error:

        log_error(
            f"Update stock value error: {error}"
        )

        print(
            "Invalid input! Please enter a valid value."
        )

    except Exception as error:

        log_error(
            f"Update stock error: {error}"
        )

        print(
            "Something went wrong."
        )



def inventory_management():

    create_inventory_file()

    while True:

        print(
            "\n========== INVENTORY MANAGEMENT =========="
        )

        print("1. View Stock")
        print("2. Add Stock")
        print("3. Update Stock")
        print("4. Back")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            view_stock()

        elif choice == "2":

            add_stock()

        elif choice == "3":

            update_stock()

        elif choice == "4":

            print(
                "Returning to previous menu..."
            )

            break

        else:

            print(
                "Invalid choice! Please try again."
            )

create_inventory_file()
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
ORDER_FILE = os.path.join(DATABASE_DIR, "orders.json")
ERROR_FILE = os.path.join(LOG_DIR, "error.log")



def create_folders():

    os.makedirs(DATABASE_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)



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

def create_order_file():

    create_folders()

    try:

        if not os.path.exists(ORDER_FILE):

            with open(
                ORDER_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump([], file, indent=4)

    except Exception as error:

        log_error(
            f"Order file creation error: {error}"
        )


def read_menu():

    create_folders()

    try:

        if not os.path.exists(MENU_FILE):

            print("\nMenu is not available.")
            print("Please create menu first.")

            return []

        with open(
            MENU_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            menu_data = json.load(file)

            return menu_data

    except Exception as error:

        log_error(
            f"Menu reading error: {error}"
        )

        print("Unable to read menu.")

        return []


def read_orders():

    create_order_file()

    try:

        with open(
            ORDER_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            orders = json.load(file)

            return orders

    except Exception as error:

        log_error(
            f"Order reading error: {error}"
        )

        return []



def save_orders(order_data):

    create_folders()

    try:

        with open(
            ORDER_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                order_data,
                file,
                indent=4
            )

        return True

    except Exception as error:

        log_error(
            f"Order saving error: {error}"
        )

        return False


def show_menu_for_order():

    menu_data = read_menu()

    if not menu_data:

        return False

    print("\n========== VELMORA MENU ==========")

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

    return True


def new_order():

    print("\n========== NEW ORDER ==========")

    try:

        menu_data = read_menu()

        if not menu_data:

            print("Menu is not available.")
            print("Please add menu items first.")

            return

        show_menu_for_order()

        orders = read_orders()



        if orders:

            order_id = orders[-1]["order_id"] + 1

        else:

            order_id = 1

        

        customer_name = input(
            "\nEnter customer name: "
        ).strip()

        if customer_name == "":

            print(
                "Customer name cannot be empty!"
            )

            return

        order_items = []

        

        while True:

            print(
                "\nEnter 0 when you want to finish the order."
            )

            item_id = input(
                "Enter food item ID: "
            ).strip()

            if item_id == "0":

                break

            try:

                item_id = int(item_id)

            except ValueError as error:

                log_error(
                    f"New order item ID error: {error}"
                )

                print(
                    "Invalid input! Please enter a number."
                )

                continue

            selected_item = None

            for item in menu_data:

                if item["id"] == item_id:

                    selected_item = item

                    break

            if selected_item is None:

                print(
                    "Food item ID not found!"
                )

                continue

            print(
                f"\nSelected: {selected_item['name']}"
            )

            print(
                f"1. Full - Rs.{selected_item['full_price']}"
            )

            print(
                f"2. Half - Rs.{selected_item['half_price']}"
            )

            portion = input(
                "Enter portion: "
            ).strip()

            if portion == "1":

                portion_name = "Full"
                price = selected_item["full_price"]

            elif portion == "2":

                portion_name = "Half"
                price = selected_item["half_price"]

            else:

                print(
                    "Invalid portion! Please select 1 or 2."
                )

                continue

            quantity = input(
                "Enter quantity: "
            ).strip()

            try:

                quantity = int(quantity)

                if quantity <= 0:

                    print(
                        "Quantity must be greater than 0!"
                    )

                    continue

            except ValueError as error:

                log_error(
                    f"Quantity input error: {error}"
                )

                print(
                    "Invalid quantity! Please enter a number."
                )

                continue

            item_total = price * quantity

            order_item = {

                "item_id": selected_item["id"],

                "name": selected_item["name"],

                "portion": portion_name,

                "price": price,

                "quantity": quantity,

                "total": item_total
            }

            order_items.append(order_item)

            print(
                f"{selected_item['name']} added to order."
            )

            print(
                f"Item Total: Rs.{item_total}"
            )

       

        if not order_items:

            print(
                "No item added to order."
            )

            return

        

        subtotal = 0

        for item in order_items:

            subtotal += item["total"]



        current_datetime = datetime.now()

        new_order_data = {

            "order_id": order_id,

            "customer_name": customer_name,

            "date": current_datetime.strftime(
                "%Y-%m-%d"
            ),

            "time": current_datetime.strftime(
                "%H:%M:%S"
            ),

            "status": "Pending",

            "items": order_items,

            "subtotal": subtotal
        }

        orders.append(new_order_data)

        

        if save_orders(orders):

            print(
                "\n========== ORDER CREATED =========="
            )

            print(
                f"Order ID : {order_id}"
            )

            print(
                f"Customer : {customer_name}"
            )

            print(
                f"Subtotal : Rs.{subtotal}"
            )

            print(
                "Status   : Pending"
            )

            print(
                "\nOrder saved successfully!"
            )


    except Exception as error:

        log_error(
            f"New order error: {error}"
        )

        print(
            "Something went wrong. Error has been logged."
        )



def view_orders():

    print("\n========== VIEW ORDERS ==========")

    orders = read_orders()

    if not orders:

        print("No orders found.")

        return

    for order in orders:

        print("\n" + "=" * 55)

        print(
            f"Order ID : {order['order_id']}"
        )

        print(
            f"Customer : {order['customer_name']}"
        )

        print(
            f"Date     : {order['date']}"
        )

        print(
            f"Time     : {order['time']}"
        )

        print(
            f"Status   : {order['status']}"
        )

        print("-" * 55)

        for item in order["items"]:

            print(
                f"{item['name']} "
                f"({item['portion']}) "
                f"x{item['quantity']} "
                f"= Rs.{item['total']}"
            )

        print("-" * 55)

        print(
            f"Subtotal : Rs.{order['subtotal']}"
        )

    print("=" * 55)


def update_order():

    print("\n========== UPDATE ORDER ==========")

    orders = read_orders()

    if not orders:

        print("No orders found.")

        return

    view_orders()

    try:

        order_id = int(
            input("\nEnter Order ID: ")
        )

        selected_order = None

        for order in orders:

            if order["order_id"] == order_id:

                selected_order = order

                break

        if selected_order is None:

            print("Order ID not found!")

            return

        if selected_order["status"] == "Cancelled":

            print(
                "Cancelled order cannot be updated."
            )

            return

        print("\n1. Add Item")
        print("2. Change Quantity")
        print("3. Back")

        choice = input(
            "Enter choice: "
        ).strip()

    

        if choice == "1":

            menu_data = read_menu()

            if not menu_data:

                print(
                    "Menu is not available."
                )

                return

            show_menu_for_order()

            item_id = int(
                input(
                    "Enter food item ID: "
                )
            )

            selected_item = None

            for item in menu_data:

                if item["id"] == item_id:

                    selected_item = item

                    break

            if selected_item is None:

                print(
                    "Food item not found!"
                )

                return

            print("1. Full")
            print("2. Half")

            portion = input(
                "Enter portion: "
            ).strip()

            if portion == "1":

                portion_name = "Full"

                price = selected_item["full_price"]

            elif portion == "2":

                portion_name = "Half"

                price = selected_item["half_price"]

            else:

                print(
                    "Invalid portion!"
                )

                return

            quantity = int(
                input(
                    "Enter quantity: "
                )
            )

            if quantity <= 0:

                print(
                    "Quantity must be greater than 0!"
                )

                return

            new_item = {

                "item_id": selected_item["id"],

                "name": selected_item["name"],

                "portion": portion_name,

                "price": price,

                "quantity": quantity,

                "total": price * quantity
            }

            selected_order["items"].append(
                new_item
            )

            subtotal = 0

            for item in selected_order["items"]:

                subtotal += item["total"]

            selected_order["subtotal"] = subtotal

            if save_orders(orders):

                print(
                    "Item added to order successfully!"
                )

        elif choice == "2":

            if not selected_order["items"]:

                print(
                    "No items in this order."
                )

                return

            print("\nOrder Items:")

            for index, item in enumerate(
                selected_order["items"],
                start=1
            ):

                print(
                    f"{index}. "
                    f"{item['name']} "
                    f"({item['portion']}) "
                    f"x{item['quantity']}"
                )

            item_number = int(
                input(
                    "Enter item number to update: "
                )
            )

            if (
                item_number < 1
                or
                item_number > len(
                    selected_order["items"]
                )
            ):

                print(
                    "Invalid item number!"
                )

                return

            new_quantity = int(
                input(
                    "Enter new quantity: "
                )
            )

            if new_quantity <= 0:

                print(
                    "Quantity must be greater than 0!"
                )

                return

            selected_item = selected_order[
                "items"
            ][item_number - 1]

            selected_item["quantity"] = new_quantity

            selected_item["total"] = (
                selected_item["price"]
                * new_quantity
            )

            subtotal = 0

            for item in selected_order["items"]:

                subtotal += item["total"]

            selected_order["subtotal"] = subtotal

            if save_orders(orders):

                print(
                    "Order updated successfully!"
                )

    

        elif choice == "3":

            return

        else:

            print(
                "Invalid choice! Please try again."
            )

    except ValueError as error:

        log_error(
            f"Update order value error: {error}"
        )

        print(
            "Invalid input! Please enter a valid number."
        )

    except Exception as error:

        log_error(
            f"Update order error: {error}"
        )

        print(
            "Something went wrong. Error has been logged."
        )


def cancel_order():

    print("\n========== CANCEL ORDER ==========")

    orders = read_orders()

    if not orders:

        print("No orders found.")

        return

    view_orders()

    try:

        order_id = int(
            input("\nEnter Order ID: ")
        )

        selected_order = None

        for order in orders:

            if order["order_id"] == order_id:

                selected_order = order

                break

        if selected_order is None:

            print(
                "Order ID not found!"
            )

            return

        if selected_order["status"] == "Cancelled":

            print(
                "Order is already cancelled."
            )

            return

        confirm = input(
            "Are you sure you want to cancel this order? (yes/no): "
        ).strip().lower()

        if confirm == "yes":

            selected_order["status"] = "Cancelled"

            if save_orders(orders):

                print(
                    "\nOrder cancelled successfully!"
                )

        else:

            print(
                "Order cancellation stopped."
            )

    except ValueError as error:

        log_error(
            f"Cancel order value error: {error}"
        )

        print(
            "Invalid input! Please enter a valid Order ID."
        )

    except Exception as error:

        log_error(
            f"Cancel order error: {error}"
        )

        print(
            "Something went wrong. Error has been logged."
        )



def order_management():

    create_order_file()

    while True:

        print(
            "\n========== ORDER MANAGEMENT =========="
        )

        print("1. New Order")
        print("2. View Orders")
        print("3. Update Order")
        print("4. Cancel Order")
        print("5. Back")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            new_order()

        elif choice == "2":

            view_orders()

        elif choice == "3":

            update_order()

        elif choice == "4":

            cancel_order()

        elif choice == "5":

            print(
                "Returning to previous menu..."
            )

            break

        else:

            print(
                "Invalid choice! Please try again."
            )




create_order_file()
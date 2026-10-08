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

ORDER_FILE = os.path.join(DATABASE_DIR, "orders.json")
BILL_FILE = os.path.join(DATABASE_DIR, "bills.json")
ERROR_FILE = os.path.join(LOG_DIR, "error.log")



GST_RATE = 5


def create_folders():

    try:

        os.makedirs(
            DATABASE_DIR,
            exist_ok=True
        )

        os.makedirs(
            LOG_DIR,
            exist_ok=True
        )

    except Exception as error:

        print(
            f"Folder creation error: {error}"
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


def create_bill_file():

    create_folders()

    try:

        if not os.path.exists(BILL_FILE):

            with open(
                BILL_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )

        return True

    except Exception as error:

        log_error(
            f"Bill file creation error: {error}"
        )

        return False



def read_orders():

    try:

        if not os.path.exists(ORDER_FILE):

            print(
                "\nOrder file not found."
            )

            return []

        with open(
            ORDER_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as error:

        log_error(
            f"Order reading error: {error}"
        )

        print(
            "Unable to read orders."
        )

        return []

def read_bills():

    create_bill_file()

    try:

        with open(
            BILL_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as error:

        log_error(
            f"Bill reading error: {error}"
        )

        return []


def save_bills(bills):

    create_folders()

    try:

        with open(
            BILL_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                bills,
                file,
                indent=4
            )

        return True

    except Exception as error:

        log_error(
            f"Bill saving error: {error}"
        )

        return False


def find_order(order_id):

    orders = read_orders()

    for order in orders:

        if order["order_id"] == order_id:

            return order

    return None


def generate_bill():

    print(
        "\n========== ZAYKA BILLING SYSTEM =========="
    )

    orders = read_orders()

    if not orders:

        print(
            "No order found."
        )

        print(
            "Please create an order first."
        )

        return

    try:

        order_id = int(
            input(
                "Enter Order ID: "
            ).strip()
        )

        order = find_order(order_id)

        if order is None:

            print(
                "Order ID not found."
            )

            return

        if order["status"] == "Cancelled":

            print(
                "Bill cannot be generated "
                "for a cancelled order."
            )

            return

    
        bills = read_bills()

        for bill in bills:

            if bill["order_id"] == order_id:

                print(
                    "\nBill for this order already exists."
                )

                print(
                    f"Bill ID: {bill['bill_id']}"
                )

                return

    
        subtotal = float(
            order["subtotal"]
        )

        print(
            f"\nSubtotal: Rs.{subtotal:.2f}"
        )

        discount_input = input(
            "Enter discount percentage "
            "(0 for no discount): "
        ).strip()

        if discount_input == "":

            discount_percentage = 0

        else:

            discount_percentage = float(
                discount_input
            )

        if discount_percentage < 0:

            print(
                "Discount cannot be negative."
            )

            return

        if discount_percentage > 100:

            print(
                "Discount cannot be more than 100%."
            )

            return

        discount_amount = (
            subtotal
            * discount_percentage
            / 100
        )

        amount_after_discount = (
            subtotal
            - discount_amount
        )

    

        gst_amount = (
            amount_after_discount
            * GST_RATE
            / 100
        )

        
        final_total = (
            amount_after_discount
            + gst_amount
        )

    
        if bills:

            bill_id = (
                bills[-1]["bill_id"]
                + 1
            )

        else:

            bill_id = 1

    
        current_time = datetime.now()

        bill = {

            "bill_id": bill_id,

            "order_id": order_id,

            "customer_name": order[
                "customer_name"
            ],

            "date": current_time.strftime(
                "%Y-%m-%d"
            ),

            "time": current_time.strftime(
                "%H:%M:%S"
            ),

            "items": order["items"],

            "subtotal": round(
                subtotal,
                2
            ),

            "discount_percentage": round(
                discount_percentage,
                2
            ),

            "discount_amount": round(
                discount_amount,
                2
            ),

            "gst_percentage": GST_RATE,

            "gst_amount": round(
                gst_amount,
                2
            ),

            "final_total": round(
                final_total,
                2
            )
        }


        bills.append(
            bill
        )

        if save_bills(bills):

            print_bill(bill)

            print(
                "\nBill generated successfully!"
            )


    except ValueError as error:

        log_error(
            f"Billing value error: {error}"
        )

        print(
            "Invalid input! Please enter a valid number."
        )

    except Exception as error:

        log_error(
            f"Billing error: {error}"
        )

        print(
            "Something went wrong. "
            "Error has been logged."
        )

def print_bill(bill):

    print("\n")

    print("=" * 55)

    print(
        "                    VELMORA"
    )

    print(
        "              HOTEL & RESTAURANT"
    )

    print("=" * 55)

    print(
        f"Bill ID      : {bill['bill_id']}"
    )

    print(
        f"Order ID     : {bill['order_id']}"
    )

    print(
        f"Customer     : {bill['customer_name']}"
    )

    print(
        f"Date         : {bill['date']}"
    )

    print(
        f"Time         : {bill['time']}"
    )

    print("-" * 55)

    print(
        f"{'Item':<22}"
        f"{'Portion':<10}"
        f"{'Qty':<6}"
        f"{'Total':<10}"
    )

    print("-" * 55)

    for item in bill["items"]:

        print(
            f"{item['name']:<22}"
            f"{item['portion']:<10}"
            f"{item['quantity']:<6}"
            f"Rs.{item['total']:<7}"
        )

    print("-" * 55)

    print(
        f"Subtotal        : "
        f"Rs.{bill['subtotal']:.2f}"
    )

    print(
        f"Discount "
        f"({bill['discount_percentage']:.2f}%): "
        f"-Rs.{bill['discount_amount']:.2f}"
    )

    print(
        f"GST "
        f"({bill['gst_percentage']}%): "
        f"Rs.{bill['gst_amount']:.2f}"
    )

    print("-" * 55)

    print(
        f"FINAL TOTAL     : "
        f"Rs.{bill['final_total']:.2f}"
    )

    print("=" * 55)

    print(
        "        Thank you for visiting Velmora!"
    )

    print("=" * 55)

def view_bills():

    print(
        "\n========== VIEW BILLS =========="
    )

    bills = read_bills()

    if not bills:

        print(
            "No bills found."
        )

        return

    for bill in bills:

        print(
            "\n" + "=" * 50
        )

        print(
            f"Bill ID      : {bill['bill_id']}"
        )

        print(
            f"Order ID     : {bill['order_id']}"
        )

        print(
            f"Customer     : {bill['customer_name']}"
        )

        print(
            f"Date         : {bill['date']}"
        )

        print(
            f"Subtotal     : "
            f"Rs.{bill['subtotal']:.2f}"
        )

        print(
            f"Discount     : "
            f"Rs.{bill['discount_amount']:.2f}"
        )

        print(
            f"GST          : "
            f"Rs.{bill['gst_amount']:.2f}"
        )

        print(
            f"Final Total  : "
            f"Rs.{bill['final_total']:.2f}"
        )

    print(
        "=" * 50
    )


def billing_management():

    create_bill_file()

    while True:

        print(
            "\n========== BILLING SYSTEM =========="
        )

        print(
            "1. Generate Bill"
        )

        print(
            "2. View Bills"
        )

        print(
            "3. Back"
        )

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            generate_bill()

        elif choice == "2":

            view_bills()

        elif choice == "3":

            print(
                "Returning to previous menu..."
            )

            break

        else:

            print(
                "Invalid choice! Please try again."
            )


create_bill_file()
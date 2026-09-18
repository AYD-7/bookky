from datetime import datetime
from utilities.choice_maker import select_category
from data.messages import not_available


def id_generator(receipts_list: list[dict]) -> str:
    """
        Generates a sequential ID like RN0001, RN0002.
    """

    if not receipts_list:
        return "RN0001"

    # Gets last numeric portion and increments
    last_id_str = receipts_list[-1]["id"][2:]
    next_num = int(last_id_str) + 1

    # :04d automatically pads numbers with leading zeros up to 4 digits
    return f"RN{next_num:04d}"


def add_receipt(receipts_list: list[dict]) -> dict:
    """
        Prompts for input and returns a new receipt dictionary.
    """

    print("Enter receipt details")

    # next lines of code get different details needed for the receipt
    business: str = input("Business name: ")
    date: str = input("Date (dd/mm/yyyy): ")
    category: str = select_category()

    while True:
        try:
            amount: float = float(input("Amount: "))
            # rejects negative numbers and zero
            if amount <= 0:
                print("Enter a valid amount. Please try again")
                continue
            break
        except ValueError:
            print("Enter a valid amount. Please try again")

    while True:
        try:
            vat: float = float(input("VAT: "))
            if vat < 0:  # allows 0 VAT if needed
                print("Enter a valid amount. Please try again")
                continue
            break
        except ValueError:
            print("Enter a valid VAT. Please try again!")

    payment_method: str = input("Payment Method: ")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Pass the active list to generator
    receipt_id = id_generator(receipts_list)
    print("Receipt added successfully!")

    return {
        "id": receipt_id,
        "business_name": business,
        "date": date,
        "category": category,
        "amount": amount,
        "vat": vat,
        "payment_method": payment_method,
        "created_at": current_time,
    }


def view_receipts(receipts_list: list[dict]) -> None:
    """
        Displays summary table of all receipts.
    """

    # safely returns when the JSON file is empty
    if not receipts_list:
        print(not_available)
        return

    # prints header
    print(f"\n{'ID':<8} | {'Business':<20} | {'Amount':<12} | {'Date':<10}")
    # prints divider
    print("-" * 60)

    # loops through the receipt list
    for receipt in receipts_list:
        formatted_amount = f"₦{receipt['amount']:,.2f}"
        print(
            f"{receipt['id']:<8} | {receipt['business_name'][:20]:<20} | {formatted_amount:<12} | {receipt['date']:<10}"
        )

    # prints footer divider
    print("-" * 60)


def view_single_receipt(receipts_list: list[dict]) -> None:
    """Searches and views details of a single receipt."""
    if not receipts_list: 
        print(not_available)
        return

    receipt_id: str = input("Enter the receipt's id: ")

    for receipt in receipts_list:
        if receipt_id.strip().upper() == receipt["id"].upper():
            print(f"\n--- RECEIPT DETAILS ({receipt['id']}) ---")
            print(f"Business Name:  {receipt['business_name']}")
            print(f"Date:           {receipt['date']}")
            print(f"Category:       {receipt['category']}")
            print(f"Amount:         ₦{receipt['amount']:,.2f}")
            print(f"VAT:            ₦{receipt['vat']:,.2f}")
            print(f"Payment Method: {receipt['payment_method']}")
            print(f"Logged At:      {receipt['created_at']}")
            print("-" * 32)
            return

    print("Cannot find the receipt")

def view_monthly_receipt (receipts_list: list[dict]) -> None:
    pass

def view_business_receipt (receipts_list: list[dict]) -> None:
    pass


def delete_single_receipt(receipts_list: list[dict]) -> bool:
    """
        Deletes a single receipt by ID. Returns True if modified.
    """
    if not receipts_list: 
        print(not_available)
        return
    
    receipt_id: str = input("Enter the receipt's id to delete: ")

    for receipt in receipts_list:
        if receipt_id.strip().upper() == receipt["id"].upper():
            receipts_list.remove(receipt)
            print(f"Receipt {receipt_id.upper()} deleted successfully!")
            return True  # signals that state changed

    print("Cannot find the receipt")
    return False


def clear_all_receipts(receipts_list: list[dict]) -> bool:
    """
        Clears all receipts. Returns True if modified.
    """
    # confirmation message
    confirm: str = input(
        "Are you sure you want to clear all receipts? (yes/no): "
    )

    # clearing the receipt
    if confirm.strip().lower() in ["yes", "y"]:
        receipts_list.clear()
        print("All receipts cleared successfully!")
        return True  # Signal that state changed
    else:
        print("Operation cancelled. Receipts were not deleted.")
        return False
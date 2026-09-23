from datetime import datetime
from utilities.choice_maker import choice, select_category
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
    """
        Filters and displays receipts for a user-specified month
    """
    if not receipts_list :
        print(not_available)
        return 

    # step 1. get and validate user's input
    while True:
        try:
            month: int = int(input("Enter month (1 - 12): "))
            if month not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
                print("Invalid input")
                continue
            break
        except ValueError:
            print("Invalid input")

    while True:
        try:
            year: int = int(input("Enter year (e.g., 2026): "))
            if len(str(year)) != 4:
                print("Invalid input")
                continue
            break
        except ValueError:
            print("Invalid input")

    # step 2. filtering receipts that match the month and year
    matching_receipts: list[dict] = []

    for receipt in receipts_list:
        try:
            # parses "dd/mm/yyyy" into datetime object
            receipt_date: str = datetime.strptime(receipt["date"].strip(), "%d/%m/%Y")

            if receipt_date.month == month and receipt_date.year == year:
                matching_receipts.append(receipt) 
        except ValueError:
            # skips receipt when it has invalid date
            continue  

    #step 3. display filtered receipts
    if not matching_receipts:
        print(f"\nNo receipts found for {month:02d}/{year}")
        return

    total_amount: float = 0
    total_vat: float = 0

    for receipt in matching_receipts:
        total_amount += receipt["amount"]
        total_vat += receipt["vat"]

    # reuse the existing receipt table formatter
    print(f"\n{"-" * 19} RECEIPTS FOR {month:02d}/{year} {"-" * 19} \n\nTotal no. of receipts: {len(matching_receipts)}")
    view_receipts(matching_receipts)
    print(f"Total Amount: ₦{total_amount:,.2f} \nTotal VAT: ₦{total_vat:,.2f}")

def view_yearly_receipt (receipts_list: list[dict]) -> None:
    """
        Filters and displays receipts for a user-specified year.
    """
    if not receipts_list:
        print("You currently don't have any receipts.")
        return

    # 1. prompt for year input
    while True:
        try:
            year: int = int(input("Enter year (e.g., 2026): "))
            if len(str(year)) != 4:
                print("Invalid input")
                continue
            break
        except ValueError:
            print("Invalid input")

    # 2. filter receipts matching the year
    matching_receipts: list[dict] = []

    for receipt in receipts_list:
        try:
            # parses "dd/mm/yyyy" string into a datetime object
            receipt_date: str = datetime.strptime(receipt["date"].strip(), "%d/%m/%Y")

            if receipt_date.year == year:
                matching_receipts.append(receipt)

        except ValueError:
            # skip receipts with invalid date formats
            continue

    # 3. display filtered results
    if not matching_receipts:
        print(f"\nNo receipts found for the year {year}.")
        return

    for receipt in matching_receipts:
        total_amount += receipt["amount"]
        total_vat += receipt["vat"]

    total_amount: float = 0
    total_vat: float = 0

    # reuse the existing receipt table formatter
    print(f"\n{"-" * 20} RECEIPTS FOR {year} {"-" * 20} \n\nTotal no. of receipts: {len(matching_receipts)}")
    view_receipts(matching_receipts)
    print(f"Total Amount: ₦{total_amount:,.2f} \nTotal VAT: ₦{total_vat:,.2f}")



def view_category_receipt(receipts_list: list[dict]) -> None:
    """
        Filters and displays all the receipts in a category 
    """

    if not receipts_list:
        print(not_available)
        return

    category: str = select_category()

    # filtering receipts that matches the category
    matching_receipts: list[dict] = [receipt for receipt in receipts_list if receipt["category"] == category]

    # display filtered receipts
    if not matching_receipts:
        print(f"\nNo receipts found for category: {category}")
        return

    total_amount: float = 0
    total_vat: float = 0

    for receipt in matching_receipts:
        total_amount += receipt["amount"]
        total_vat += receipt["vat"]

    # reuse the existing receipt table formatter
    print(f"\n{"-" * 12} RECEIPTS FOR {category.upper()[:20]}{"." if len(category) > 20 else ""} {"-" * 12} \n\nTotal no. of receipts: {len(matching_receipts)}")
    view_receipts(matching_receipts)

    print(f"Total Amount: ₦{total_amount:,.2f} \nTotal VAT: ₦{total_vat:,.2f}")


    

def view_business_receipt(receipts_list: list[dict]) -> None:
    """
        Filters and displays all receipts from a selected business.
    """
    if not receipts_list:
        print("You currently don't have any receipts.")
        return

    # 1. get unique business names 
    businesses: list[str] = list(
        {receipt["business_name"].strip() for receipt in receipts_list}
    )

    # 2. build the numbered menu 
    print("\nSelect a Business:")
    for index, business in enumerate(businesses, start=1):
        print(f"{index}. {business}")

    # 3. handle selection input safely
    selected_business = None

    while True:
        user_input = choice()

        # checks if the input is a valid numeric choice from the list
        if user_input.isdigit():
            selected_index = int(user_input) - 1
            if 0 <= selected_index < len(businesses):
                selected_business = businesses[selected_index]
                break

        print(f"Invalid input! Enter a number between 1 and {len(businesses)}.")

    # 4. filters receipts for the selected business
    matching_receipts = [
        receipt
        for receipt in receipts_list
        if receipt["business_name"].strip().lower() == selected_business.lower()
    ]

    total_amount: float = 0
    total_vat: float = 0

    for receipt in matching_receipts:
        total_amount += receipt["amount"]
        total_vat += receipt["vat"]

    # 5. displays the filtered results
    print(f"\n{"-" * 12} RECEIPTS FOR {selected_business.upper()[:20]}{"." if len(selected_business) > 20 else ""} {"-" * 12} \n\nTotal no. of receipts: {len(matching_receipts)}")
    view_receipts(matching_receipts)

    print(f"Total Amount: ₦{total_amount:,.2f} \nTotal VAT: ₦{total_vat:,.2f}")

    
    


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
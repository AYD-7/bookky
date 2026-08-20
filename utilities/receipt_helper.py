from datetime import datetime
from data.receipts import receipts



# generates new id
def id_generator () -> str:
    """
        Helper function to generate a new id number
    """
    last_receipt_no:str = receipts[-1]["id"][2:] # gets the last 4 characters of the id number of the last receipt

    new_receipt_no: int = int(last_receipt_no) + 1 # adds one
    new_receipt_no: str = str(new_receipt_no) # converts to a string
    place_value: int = len(new_receipt_no) # gets the no. of characters
    new_id: str = "RN"

    # checks if the place value is in units, tens hundreds, or thousands
    if place_value == 4: # thousands
        new_id += new_receipt_no 
    elif place_value == 3: # hundreds
        new_id += f"0{new_receipt_no}"
    elif place_value == 2: # tens
        new_id += f"00{new_receipt_no}"
    else: # units
        new_id += f"000{new_receipt_no}"

    return new_id # returns the new id


# adds a new receipt
def add_receipt () -> dict:
    """
        Helper function to add a receipt to a list of receipts
    """

    print("Enter receipt details")

    # details
    business: str = input("Business name: ")
    date: str = input("Date (dd/mm/yyyy): ")
    category: str = input("Category: ")

    # returns the field to fill in the amount and VAT when the user doesn't enter a valid number
    while True:
        try:
            amount: float = float(input("Amount: "))
            break
        except ValueError: 
            print("Enter a valid amount. Please try again")

    while True:
        try:
            vat:float = float(input("VAT: "))
            break
        except ValueError: 
            print("Enter a valid VAT. Please try again!")

    payment_method: str = input("Payment Method: ")

    # gets the date in this format: 2026-08-20 23:05:45 
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

    # generates a new id  when it's not the first receipt
    receipt_id: str = "RN0001" if len(receipts) <= 0 else id_generator() 
    print("Receipt added successfully!")

    return {
        "id": receipt_id,
        "business_name": business,
        "date": date,
        "category": category,
        "amount": amount,
        "vat": vat,
        "payment_method": payment_method,
        "created_at": current_time
    }


# views receipt(s)
def view_receipts (receipts_list: list[dict]) -> None:
    """
        Helper function finds and displays all receipts
    """
    if len(receipts_list) <= 0:
        print("You currently don't have any receipt")
        return
    
    # creates the table header
    print(f"\n{'ID':<8} | {'Business':<20} | {'Amount':<12} | {'Date':<10}")
    print("-" * 60)

    # renders each receipt as standard output
    for receipt in receipts_list:
        # formats the amount column to look neat
        formatted_amount = f"₦{receipt['amount']:,.2f}"
        
        # left-aligns columns using spacing markers (<8, <20, etc.)
        print(f"{receipt['id']:<8} | {receipt['business_name'][:20]:<20} | {formatted_amount:<12} | {receipt['date']:<10}")
    
    print("-" * 60)
    return


def view_single_receipt () -> None:
    """
        Helper function finds a single receipt
    """

    receipt_id: str = input("Enter the receipt's id: ")

    for receipt in receipts:
        if receipt_id.strip().upper() == receipt["id"].upper():
            print(f"\n--- RECEIPT DETAILS ({receipt['id']}) ---")
            
            # formats each key-value pair beautifully
            print(f"Business Name:  {receipt['business_name']}")
            print(f"Date:           {receipt['date']}")
            print(f"Category:       {receipt['category']}")
            print(f"Amount:         ₦{receipt['amount']:,.2f}")  # formatted currency
            print(f"VAT:            ₦{receipt['vat']:,.2f}")
            print(f"Payment Method: {receipt['payment_method']}")
            print(f"Logged At:      {receipt['created_at']}")
            print("-" * 32)
            return  # exits the function after printing
                
    print("Cannot find the receipt")
    return # exits after printing
    
    
# deletes a single receipt
def delete_single_receipt() -> None:
    """
        Helper function to delete a specific receipt by its ID
    """
    receipt_id: str = input("Enter the receipt's id to delete: ")

    # loops to find the receipt
    for receipt in receipts:
        if receipt_id.strip().upper() == receipt["id"].upper():
            receipts.remove(receipt) # removes the specific receipt from the list
            print(f"Receipt {receipt_id.upper()} deleted successfully!")
            return # exits the function after deleting

    print("Cannot find the receipt")
    return # exits after printing


# clears all receipts
def clear_all_receipts() -> None:
    """
        Helper function to delete all receipts in the system
    """
    # confirms if the user really wants to wipe out all data
    confirm: str = input("Are you sure you want to clear all receipts? (yes/no): ")

    if confirm.strip().lower() in ["yes", "y"]:
        receipts.clear() # empties the receipts list completely
        print("All receipts cleared successfully!")
    else:
        print("Operation cancelled. Receipts were not deleted.")
        
    return # exits the function


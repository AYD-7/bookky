from datetime import datetime

today = datetime.now() 
day = today.strftime("%a, %")

print(day)

def add_receipt ():
    """
        Helper function to add a receipt to a list of receipts
    """

    print("Enter receipt details")

    # details
    business = input("Business name: ")
    date = input("Date (dd/mm/yyyy): ")
    category = input("Category: ")
    # returning the field to fill in the amount and VAT when the user doesn't enter a valid number
    while True:
        try:
            amount = float(input("Amount: "))
            break
        except ValueError: 
            print("Enter a valid amount. Please try again")

    while True:
        try:
            vat = float(input("VAT: "))
            break
        except ValueError: 
            print("Enter a valid VAT. Please try again!")
    payment_method = input("Payment Method: ")

    print("Receipt added successfully!")

    return {
        "business_name": business,
        "date": date,
        "category": category,
        # "created_at": 
    }

    


# imports
from  collections import Counter

from data.messages import summary_header, not_available


def display_expense_summary (receipts_list: list[dict]) -> None:
    print(summary_header)

    # safely exists the function when no receipt is available
    if not receipts_list:
        print(not_available)
        return

    total_receipts: int = len(receipts_list)

    total_expenses: float = 0.00 
    total_vat: float = 0.00

    # aggregating costs
    for receipt in receipts_list:
        total_expenses += receipt["amount"]
        total_vat += receipt["vat"]

    # extracting all categories using a list comprehension
    categories = [receipt["category"] for receipt in receipts_list]

    top_cat, count = Counter(categories).most_common(1)[0] # destructuring the Counter tuple to get the category that appeared the most in the list

    top_expense_receipt = max(receipts_list, key= lambda receipt: receipt["amount"])

    print(f"Total Receipts: {total_receipts} \n\nTotal Expenses: ₦{total_expenses:,.2f} \nTotal VAT: ₦{total_vat:,.2f} \n\nTop Category: \n{top_cat} (appeared {count} times) \n\nHighest Expense: \n{top_expense_receipt["business_name"]} - {top_expense_receipt["amount"]:,.2f} - {top_expense_receipt["id"]} \n{"-" * 50}")



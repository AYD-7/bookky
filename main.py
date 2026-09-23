# imports
# built-in
import json
import os
from data.messages import (
    delete_options_list,
    goodbye_message,
    options_list,
    view_options_list,
    welcome_message,
)

# user-defined
from utilities.choice_maker import choice
from utilities.receipt_helper import (
    add_receipt,
    clear_all_receipts,
    delete_single_receipt,
    view_receipts,
    view_single_receipt,
    view_monthly_receipt,
    view_yearly_receipt,
    view_category_receipt,
    view_business_receipt,
)
from utilities.summary import display_expense_summary
from utilities.export_helper import export_receipts_to_downloads



JSON_FILE_PATH = "./data/receipts.json" # JSON file


def load_receipts() -> list[dict]:
    """
        Reads the JSON file
    """

    # creates a new directory, quietly moves on if file already exists
    os.makedirs(os.path.dirname(JSON_FILE_PATH), exist_ok=True)

    # loads the JSON file as a list if there's content in it
    if os.path.exists(JSON_FILE_PATH) and os.path.getsize(JSON_FILE_PATH) > 0:
        # content manager
        with open(JSON_FILE_PATH, "r") as file:
            return json.load(file)
        
    return [] # returns an empty list if there isn't


def save_receipts(receipts_list: list[dict]) -> None:
    """
        Saves update into the JSON file
    """
    # content manager: writes content into the JSON file
    with open(JSON_FILE_PATH, "w") as file:
        json.dump(receipts_list, file, indent=4)  # added indent for readable JSON


def ask_to_continue() -> bool:
    """
        Returns user to the main menu
    """

    # loop to keep the function alive
    while True:
        # gets use's input 
        user_input = (
            input("\nDo you want to return to the main menu? [yes/no] ")
            .strip()
            .lower()
        )

        # returns user to main menu
        if user_input in ["yes", "y"]:
            print("Returning to the main menu...\n")
            return True

        # triggers exiting the main function
        elif user_input in ["no", "n"]:
            return False


def bookky_main_function():
    """
        Main function. The entry function.
    """

    print(welcome_message)

    while True:
        # loads state at start of loop so all options access the freshest data
        current_receipts = load_receipts()

        print(options_list)
        option: str = choice()

        # handles invalid input
        if option not in ["1", "2", "3", "4", "5"]:
            print("You need to enter a valid input! Try again\n")
            continue

        # 1. Add receipt
        if option == "1":
            new_receipt = add_receipt(current_receipts)
            current_receipts.append(new_receipt)
            save_receipts(current_receipts)

        # 2. View receipts
        elif option == "2":
            print(view_options_list)

            while True:
                view_option = choice()
                if view_option in ["1", "2", "3", "4", "5", "6"]:
                    break
                print("Enter a valid input! Please try again!")

            # view all receipts
            if view_option == "1":
                view_receipts(current_receipts)

            # view a receipt
            elif view_option == "2":
                view_single_receipt(current_receipts)

            # view by month
            elif view_option == "3":
                view_monthly_receipt(current_receipts)

            # view by year
            elif view_option == "4":
                view_yearly_receipt(current_receipts)

            # view by category
            elif view_option == "5":
                view_category_receipt(current_receipts)

            # view by business
            elif view_option == "6":
                view_business_receipt(current_receipts)

        # 3. Delete receipts
        elif option == "3":
            print(delete_options_list)
            while True:
                delete_option = choice()
                if delete_option in ["1", "2"]:
                    break
                print("Enter a valid input! Please try again!")

            # Delete single receipt
            if delete_option == "1":
                if delete_single_receipt(current_receipts):
                    save_receipts(current_receipts)

            # Clear all receipts
            elif delete_option == "2":
                if clear_all_receipts(current_receipts):
                    save_receipts(current_receipts)

        # 4. Expense Summary
        elif option == "4":
            display_expense_summary(current_receipts)

        # 5. Exports
        elif option == "5":
            export_receipts_to_downloads(current_receipts)


        # 6. Exit
        else:
            print(f"\n{goodbye_message}")
            break

        # Check menu return after completing any option
        if not ask_to_continue():
            print(f"\n{goodbye_message}")
            break


if __name__ == "__main__":
    bookky_main_function()
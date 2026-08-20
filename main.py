# imports
from data.messages import goodbye_message, welcome_message, options_list, view_options_list, delete_options_list
from data.receipts import receipts
from utilities.choice_maker import choice
from utilities.receipt_helper import add_receipt, view_receipts, view_single_receipt, clear_all_receipts, delete_single_receipt


def ask_to_continue():
    """
        Asking the user if they want to go back to the main menu or exiting out of the function
    """
    while True:
        user_input = (
            input("Do you want to return to the main menu? [yes/no] ").strip().lower()
        )

        if user_input in ["yes", "y"]:
            print("Returning to the main menu...\n")
            return True
        elif user_input in ["no", "n"]:
            return False


# main function
def bookky_main_function ():
    """
        Main Bookky function. The entry function.
    """

    print(welcome_message) # showing the user the welcome message

    # keeping the program alive using a while loop
    while True:
        print(options_list)

        option: str = choice() # getting the user's answer

        # handling when the user input an invalid value
        if option not in ["1", "2", "3", "4"]:
            print("You need to enter a valid input! Try again\n")
            continue # skipping the current iteration and moving to a new one

        # 1. add a new receipt choice
        if option == "1":
            new_receipt: dict = add_receipt()
            receipts.append(new_receipt)

            # checking if the user still wants to continue
            if not ask_to_continue():
                print(f"\n{goodbye_message}")
                break

        # 2. view receipts choice
        elif option == "2":
            print(view_options_list)
            
            while True:
                view_option: str = choice() # gets what the user wants to view
                if view_option in ["1", "2"]:
                    break
                else:
                    print("Enter a valid input! Please try again!")



            # viewing all the receipts
            if view_option == "1":
                view_receipts(receipts)

                # checks if the user still wants to continue
                if not ask_to_continue():
                    print(f"\n{goodbye_message}")
                    break

            # viewing a single receipt
            else:
                view_single_receipt()

                # checks if the user still wants to continue
                if not ask_to_continue():
                    print(f"\n{goodbye_message}")
                    break

        # 3. delete choice
        elif option == "3":
            print(delete_options_list)

            while True:
                delete_option: str = choice() # gets what the user wants to delete
                if delete_option in ["1", "2"]:
                    break
                else:
                    print("Enter a valid input! Please try again!")

            # routes the user choice to the helper functions
            if delete_option == "1":
                delete_single_receipt()

                # checks if the user still wants to continue
                if not ask_to_continue():
                    print(f"\n{goodbye_message}")
                    break

            elif delete_option == "2":
                clear_all_receipts()
                # checks if the user still wants to continue
                if not ask_to_continue():
                    print(f"\n{goodbye_message}")
                    break



        # 4. exit choice
        else:
            print(f"\n{goodbye_message}")
            break


# invoking the function
if __name__ == "__main__":
    bookky_main_function()

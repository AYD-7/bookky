# imports
import time
from utilities.choice_maker import choice
from utilities.receipt_helper import add_receipt
from data.messages import goodbye_message, welcome_message

# main function
def bookky_main_function ():
    """
        Main Bookky function. The entry function.
    """

    print(welcome_message) # showing the user the welcome message

    option = choice() # getting the user's answer

    if option not in ["1", "2", "3"]:
        print("You need to enter a valid input")
        bookky_main_function() # recursion - calling the function again so the user can enter a valid input

    if option == "1":
        add_receipt()
    elif option == "2":
        view_receipts()
    else:
        print(f"\n{goodbye_message}")
        return


# invoking the function
bookky_main_function()
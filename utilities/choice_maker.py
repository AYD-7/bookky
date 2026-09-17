from data.messages import category_options_list

"""
    Helper function to collect the choice the user made.

"""
def choice () -> str:
    return input("Choose an option: ")


# returns a category
def select_category () -> str:
    print("Select a category")

    while True:
        print(category_options_list)

        option: str = choice()

        category: str = ""
        
        if option not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            print("You need to enter a valid input! Try again\n")
            continue # skipping the current iteration and moving to a new one

        # 1.
        if option == "1":
            category += "Food & Groceries"
            break

        # 2.
        elif option == "2":
            category += "Transportation"
            break

        # 3.
        elif option == "3":
            category += "Utilities"
            break

        # 4.
        elif option == "4":
            category += "Office Supplies"
            break
 
        # 5.
        elif option == "5":
            category += "Software & Subscriptions"
            break
         
        # 6.
        elif option == "6":
            category += "Equipment"
            break
         
        # 7.
        elif option == "7":
            category += "Entertainment"
            break

        # 8.
        elif option == "8":
            category += input("Enter the category: ")
            break

    return category



        



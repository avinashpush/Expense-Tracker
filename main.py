import sqlite3
import datetime

conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

while True:
    print("Select an Option")
    print("1. Enter a new expense")
    print("2. View Expense Summary")
    print("3. Edit Expenses")

    choice = int(input())

    if choice == 1:
        date = input("Enter the Date in format (YYYY-MM-DD): ")
        description = input("Enter the description of the expense: ")

        cur.execute("SELECT DISTINCT category FROM expenses")

        categories = cur.fetchall()

        print("Select a category by number: ")
        for index, category in enumerate(categories):
            print(f"{index + 1}. {category[0]}")

        print(f"{len(categories) + 1}. Create a New Category")

        category_choice = int(input())
        if category_choice == len(categories) + 1:
            category = input("Enter the new category name: ")
        else:
            category = categories[category_choice-1][0]

        price = input("Enter the price of the expense: ")
        cur.execute("INSERT INTO expenses (Date, description, category, price) VALUES (?, ?, ?, ?)", (date, description, category, price))

        conn.commit()

    elif choice == 2:
        print("Select an option: ")
        print("1. View all Expenses")
        print("2. View Monthly Expenses by Category")
        print("3. View Expenses by Category")


        view_choice = int(input())
        if view_choice == 1:
            cur.execute("SELECT * FROM expenses")
            expenses = cur.fetchall()
            sum = 0
            for expense in expenses:
                print(expense)
                sum += expense[4]
            print(f"Total: ${sum}")

        elif view_choice == 2:
            month = input("Enter the Month: (MM): ")
            year = input("Enter the Year: (YYYY): ")
            cur.execute("""SELECT category, SUM(price) FROM expenses
                        WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
                        GROUP BY category""", (month, year))
            expenses = cur.fetchall()
            for expense in expenses:
                print(f"Category: {expense[0]}, Total: {expense[1]}")

        elif view_choice == 3:
            #Sort by Category all expenses
            cur.execute("SELECT DISTINCT category FROM expenses")
            categories = cur.fetchall()

            if categories:
                print("All Available Categories:")
                for index, category in enumerate(categories):
                    print(f"{index+1}. {category}")
                chosen_category = int(input("Choose a Number Corresponding to its Category to Display its Expenses: "))
                if 1 <= chosen_category <= len(categories):
                    selected_category = categories[chosen_category - 1][0]
                    cur.execute("SELECT * FROM expenses WHERE category = ?", (selected_category))
                    expenses = cur.fetchall()
                    if expenses:
                        sum = 0
                        for expense in expenses:
                            print(expense)
                            sum += expense[4]
                        print(f"Total: ${sum}")
            else:
                print("No Categories Available")

        else:
            exit()

    elif choice == 3:
        print("Select an option: ")
        print("1. Delete Row")
        print("2. Update Row")

        view_choice = int(input())
        if view_choice == 1:
            cur.execute("SELECT * FROM expenses")
            expenses = cur.fetchall()
            for expense in expenses:
                print(expense)
            d = input("What do you want to delete (ID)? ")
            cur.execute("DELETE FROM expenses WHERE id = ? ", d)
            conn.commit()
        elif view_choice == 2:
            print("id | date | description | price")
            cur.execute("SELECT * FROM expenses")
            expenses = cur.fetchall()
            for expense in expenses:
                print(expense)

            col_name = input("What Column Name to Update: ?")
            new_col_value = input("What do you want to update?")

            if col_name == "price": #Convert price input to int
                new_col_value = float(new_col_value)

            retrieved_id = input("Which ID would you like to update?")

            cur.execute(f"UPDATE expenses SET {col_name} = ? where id = ?", (new_col_value, retrieved_id))
            conn.commit()
        else:
            exit()

    else:
        exit()

    repeat = input("Would you like to do something else (y/n)?\n")
    if repeat.lower() != "y":
        break

conn.close()

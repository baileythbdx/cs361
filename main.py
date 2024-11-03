from datetime import datetime
import json

budgets = {}
supported_currencies = ["USD", "EUR", "AUD", "CAD"]
currency = ""


def save_budgets():
    data_to_save = {"currency": currency, "budgets": budgets}
    with open("budgets.json", "w") as file:
        json.dump(data_to_save, file, indent=4)
    print("Budgets saved successfully.")


def load_budgets():
    global budgets, currency
    try:
        with open("budgets.json", "r") as file:
            data = json.load(file)
            currency = data.get("currency", "")  # Load saved currency
            budgets = data.get("budgets", {})    # Load saved budgets
            print(f"Budgets loaded successfully. Current currency: {currency}")
    except FileNotFoundError:
        print("No saved budgets found. Starting with an empty budget.")
    except json.JSONDecodeError:
        print("Error decoding the saved budget file. Starting with an empty budget.")


def select_currency():
    global currency
    if currency:  # If currency is already set, skip selection
        print(f"Currency already set to {currency}")
        return

    print("\nSelect the currency for your budget (e.g., USD, EUR, AUD, CAD):")

    while True:
        currency_input = input("Enter currency: ").upper()
        if currency_input in supported_currencies:
            currency = currency_input
            print(f"Currency set to {currency}")
            break
        else:
            print("Unsupported currency. Please choose from: USD, EUR, AUD, CAD.")


def main_menu():

    load_budgets()
    select_currency()

    while True:
        print("\nBudget Application Menu:")
        print("1. Add Actual Budget")
        print("2. Add Expected Budget")
        print("3. Edit/Delete Budget")
        print("4. View Budgets by Date Range")
        print("5. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            add_actual_budget()
        elif choice == "2":
            add_expected_budget()
        elif choice == "3":
            edit_delete_budget()
        elif choice == "4":
            view_budgets_by_date_range()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")


def add_actual_budget():

    print("\nPlease note that if you are adding information for a budget that already exists, information will be "
          "overwritten.")

    # Prompt user for year and month
    try:
        year = int(input("\nEnter year (e.g., 2024): "))
        month = int(input("Enter month (1-12): "))

        # Ensure the month is valid
        if month < 1 or month > 12:
            print("Invalid month. Please enter a number between 1 and 12.")
            return

        # Create a key in the format 'year-month'
        date_key = f"{year}-{month:02d}"

        # If this month/year entry doesn't exist, create it
        if date_key not in budgets:
            budgets[date_key] = {'actual_income': 0, 'expected_income': 0, 'actual_expenses': [],
                                 'expected_expenses': []}

        # Enter actual income for the month
        income = float(input("Enter the actual income for this month: "))
        budgets[date_key]['actual_income'] = income
        print(f"Income for {date_key} set to {income}.")

        # Adding line items for expenses
        while True:
            print("\nAdd an expense line item or type 'done' to finish.")
            expense_name = input("Enter expense name: ")
            if expense_name.lower() == 'done':
                break

            try:
                expense_amount = float(input(f"Enter amount for {expense_name}: "))
                budgets[date_key]['actual_expenses'].append({'name': expense_name, 'amount': expense_amount})
                print(f"Added expense: {expense_name} - {expense_amount}")
            except ValueError:
                print("Invalid amount. Please enter a number.")

    except ValueError:
        print("Invalid input. Please enter numeric values for year, month, income, and expense amounts.")

    save_budgets()

def add_expected_budget():

    print("\nPlease note that if you are adding information for a budget that already exists, information will be "
          "overwritten.")

    # Prompt user for year and month
    try:
        year = int(input("\nEnter year (e.g., 2024): "))
        month = int(input("Enter month (1-12): "))

        # Ensure the month is valid
        if month < 1 or month > 12:
            print("Invalid month. Please enter a number between 1 and 12.")
            return

        # Create a key in the format 'year-month'
        date_key = f"{year}-{month:02d}"

        # If this month/year entry doesn't exist, create it
        if date_key not in budgets:
            budgets[date_key] = {'actual_income': 0, 'expected_income': 0, 'actual_expenses': [],
                                 'expected_expenses': []}

        # Enter expected income for the month
        income = float(input("Enter the expected income for this month: "))
        budgets[date_key]['expected_income'] = income
        print(f"Expected income for {date_key} set to {income}.")

        # Adding line items for expenses
        while True:
            print("\nAdd an expected expense line item or type 'done' to finish.")
            expense_name = input("Enter expense name: ")
            if expense_name.lower() == 'done':
                break

            try:
                expense_amount = float(input(f"Enter amount for {expense_name}: "))
                budgets[date_key]['expected_expenses'].append({'name': expense_name, 'amount': expense_amount})
                print(f"Added expected expense: {expense_name} - {expense_amount}")
            except ValueError:
                print("Invalid amount. Please enter a number.")

    except ValueError:
        print("Invalid input. Please enter numeric values for year, month, income, and expense amounts.")

    save_budgets()


def edit_delete_budget():

    print("\nWarning: Editing a budget modifies the stored data. Deleting a budget is permanent and cannot be undone.")

    # Prompt user for a valid year
    while True:
        try:
            year = int(input("\nEnter the year of the budget to edit/delete (e.g., 2024): "))
            if year < 1900 or year > 2100:
                print("Please enter a realistic year (e.g., between 1900 and 2100).")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the year.")

    # Prompt user for a valid month
    while True:
        try:
            month = int(input("Enter the month of the budget to edit/delete (1-12): "))
            if 1 <= month <= 12:
                break
            else:
                print("Invalid month. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for the month.")

    # Create date_key
    date_key = f"{year}-{month:02d}"

    # Check if budget exists for this month/year
    if date_key not in budgets:
        print(f"\nNo budget found for {date_key}.")
        return

    # Prompt user to select actual or expected budget
    while True:
        print("\nChoose which budget to edit:")
        print("1. Actual Budget")
        print("2. Expected Budget")
        budget_choice = input("Enter your choice (1 or 2): ")

        if budget_choice == "1":
            budget_type = 'actual'
            break
        elif budget_choice == "2":
            budget_type = 'expected'
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    # Initialize budget entries if they do not exist
    budgets[date_key].setdefault(f'{budget_type}_income', 0)
    budgets[date_key].setdefault(f'{budget_type}_expenses', [])

    # Display budget details and options
    print(f"\n{budget_type.capitalize()} Budget for {date_key}:")
    print(f"Income: {budgets[date_key][f'{budget_type}_income']}")
    if budgets[date_key][f'{budget_type}_expenses']:
        print("Expenses:")
        for i, expense in enumerate(budgets[date_key][f'{budget_type}_expenses'], 1):
            print(f"{i}. {expense['name']}: {expense['amount']}")
    else:
        print("No expenses recorded.")

    # Provide options to edit, delete line items, or delete entire budget
    while True:
        print("\nOptions:")
        print("1. Edit income")
        print("2. Edit an expense line item")
        print("3. Delete an expense line item")
        print("4. Delete the entire budget for this month")
        print("5. Exit to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            # Edit income
            try:
                new_income = float(input("Enter the new income amount: "))
                budgets[date_key][f'{budget_type}_income'] = new_income
                print(f"{budget_type.capitalize()} income for {date_key} updated to {new_income}.")
            except ValueError:
                print("Invalid input. Please enter a numeric value for income.")

        elif choice == "2":
            # Edit an expense line item
            if budgets[date_key][f'{budget_type}_expenses']:
                try:
                    item_index = int(input("Enter the number of the expense to edit: ")) - 1
                    if 0 <= item_index < len(budgets[date_key][f'{budget_type}_expenses']):
                        new_name = input(f"Enter new name for {budgets[date_key][f'{budget_type}_expenses'][item_index]['name']}: ")
                        new_amount = float(input(f"Enter new amount for {new_name}: "))
                        budgets[date_key][f'{budget_type}_expenses'][item_index] = {'name': new_name, 'amount': new_amount}
                        print(f"Expense updated: {new_name} - {new_amount}")
                    else:
                        print("Invalid item number.")
                except (ValueError, IndexError):
                    print("Invalid input. Please enter a valid expense number and amount.")
            else:
                print("No expenses to edit.")

        elif choice == "3":
            # Delete an expense line item
            if budgets[date_key][f'{budget_type}_expenses']:
                try:
                    item_index = int(input("Enter the number of the expense to delete: ")) - 1
                    if 0 <= item_index < len(budgets[date_key][f'{budget_type}_expenses']):
                        removed_expense = budgets[date_key][f'{budget_type}_expenses'].pop(item_index)
                        print(f"Deleted expense: {removed_expense['name']} - {removed_expense['amount']}")
                    else:
                        print("Invalid item number.")
                except (ValueError, IndexError):
                    print("Invalid input. Please enter a valid expense number.")
            else:
                print("No expenses to delete.")

        elif choice == "4":
            # Delete the entire budget with confirmation
            confirm = input(f"Are you sure you want to delete the entire {budget_type} budget for {date_key}? (yes/no): ")
            if confirm.lower() == 'yes':
                del budgets[date_key][f'{budget_type}_income']
                del budgets[date_key][f'{budget_type}_expenses']
                print(f"{budget_type.capitalize()} budget for {date_key} has been deleted.")
                break
            else:
                print("Budget deletion canceled.")

        elif choice == "5":
            print("Action canceled.")
            break

        else:
            print("Invalid choice. Please choose a valid option.")

    save_budgets()


def view_budgets_by_date_range():
    # Prompt user to select actual or expected budget to view

    print("\nView Budgets by Date Range")
    print("Note: Only budgets within the specified range will be displayed.")
    print("If there are no budgets recorded for certain months in the range, they will not be shown.")

    while True:
        print("\nChoose which budget to view:")
        print("1. Actual Budgets")
        print("2. Expected Budgets")
        budget_choice = input("Enter your choice (1 or 2): ")

        if budget_choice == "1":
            budget_type = 'actual'
            break
        elif budget_choice == "2":
            budget_type = 'expected'
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    # Prompt for start date
    while True:
        start_date_str = input("Enter the start date (YYYY-MM): ")
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m")
            break
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM format.")

    # Prompt for end date
    while True:
        end_date_str = input("Enter the end date (YYYY-MM): ")
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m")
            if end_date >= start_date:
                break
            else:
                print("End date must be after the start date.")
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM format.")

    # Filter and display budgets within the date range
    print(f"\n{budget_type.capitalize()} Budgets from {start_date_str} to {end_date_str}:")
    for date_key, budget in budgets.items():
        date_obj = datetime.strptime(date_key, "%Y-%m")
        if start_date <= date_obj <= end_date:
            income = budget.get(f'{budget_type}_income', 0)
            expenses = budget.get(f'{budget_type}_expenses', [])
            print(f"\nDate: {date_key}")
            print(f"Income: {income}")
            if expenses:
                print("Expenses:")
                for expense in expenses:
                    print(f"  {expense['name']}: {expense['amount']}")
            else:
                print("No expenses recorded.")


def view_budgets():
    if not budgets:
        print("\nNo budgets found.")
    else:
        print("\nCurrent Budgets:")
        for date, budget in budgets.items():
            income = budget['income']
            print(f"\n{date}: Income = {income}")
            if budget['expenses']:
                print("Expenses:")
                for expense in budget['expenses']:
                    print(f"  {expense['name']}: {expense['amount']}")
            else:
                print("No expenses recorded.")


# Start the application
main_menu()
from datetime import datetime
import json
import requests


budgets = {}
supported_currencies = ["USD", "EUR", "AUD", "CAD"]
currency = ""


def save_budgets():
    data_to_save = {"currency": currency or "USD", "budgets": budgets}

    with open("budgets.json", "w") as file:
        json.dump(data_to_save, file, indent=4)
    print("Budgets saved successfully.")


def load_budgets():
    global budgets, currency
    try:
        with open("budgets.json", "r") as file:
            data = json.load(file)
            currency = data.get("currency", "")
            budgets = data.get("budgets", {})
            print(f"\nBudgets loaded successfully. Current currency: {currency}")
    except FileNotFoundError:
        print("\nNo saved budgets found. Starting with an empty budget.")
        budgets = {}
        currency = ""
    except json.JSONDecodeError:
        print("Error decoding the saved budget file. Starting with an empty budget.")
        budgets = {}
        currency = ""


def select_currency():
    global currency
    if currency:
        print(f"\nCurrency already set to {currency}.")
        return

    print("\nEnter the currency for your budget (USD, EUR, AUD, CAD).")

    while True:
        currency_input = input("Enter currency: ").upper()
        if currency_input in supported_currencies:
            currency = currency_input
            print(f"Currency set to {currency}")
            break
        else:
            print("Unsupported currency. Please choose from: USD, EUR, AUD, CAD.")


print("\nHi! Welcome to the budget app. Please use the options below to add an expected budget for a specific month "
      "\nand year, add an actual budget for a month and year, or edit/delete any of your previously saved budgets. We "
      "\nhope you will come back monthly (or more often!) to update your budgets to help manage your spending.")


def main_menu():
    load_budgets()
    select_currency()

    while True:
        print("\nBudget Application Menu:")
        print("1. Add Actual Budget")
        print("2. Add Expected Budget")
        print("3. Edit/Delete Budget")
        print("4. View Budgets by Date Range")
        print("5. Convert Budgets to Another Currency")
        print("6. View Monthly Summary")
        print("7. Compare Actual and Expected Budgets for a Date Range")
        print("8. Exit")

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
            convert_currency()
        elif choice == "6":
            view_monthly_summary()
        elif choice == "7":
            compare_range()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Try again.")


def add_actual_budget():

    print("\nPlease note that if you are adding information for a budget that already exists, information will be "
          "overwritten.")

    try:
        while True:
            try:
                year = int(input("\nEnter the year of the budget to add/edit (e.g., 2024): "))
                if year < 1900 or year > 2100:
                    print("Please enter a realistic year (e.g., between 1900 and 2100).")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value for the year.")

        while True:
            try:
                month = int(input("Enter the month of the budget to add/edit (1-12): "))
                if 1 <= month <= 12:
                    break
                else:
                    print("Invalid month. Please enter a number between 1 and 12.")
            except ValueError:
                print("Invalid input. Please enter a numeric value for the month.")

        date_key = f"{year}-{month:02d}"

        budgets.setdefault(date_key, {
            'actual_income': 0,
            'expected_income': 0,
            'actual_expenses': [],
            'expected_expenses': []
        })

        if 'actual_expenses' not in budgets[date_key]:
            budgets[date_key]['actual_expenses'] = []

        income = float(input("Enter the actual income for this month: "))
        budgets[date_key]['actual_income'] = income
        print(f"Income for {date_key} set to {income}.")

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

        save_budgets()

    except ValueError as e:
        print(f"Invalid input: {e}")


def add_expected_budget():

    print("\nPlease note that if you are adding information for a budget that already exists, information will be "
          "overwritten.")

    try:
        while True:
            try:
                year = int(input("\nEnter the year of the budget to edit/delete (e.g., 2024): "))
                if year < 1900 or year > 2100:
                    print("Please enter a realistic year (e.g., between 1900 and 2100).")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value for the year.")

        while True:
            try:
                month = int(input("Enter the month of the budget to edit/delete (1-12): "))
                if 1 <= month <= 12:
                    break
                else:
                    print("Invalid month. Please enter a number between 1 and 12.")
            except ValueError:
                print("Invalid input. Please enter a numeric value for the month.")

        date_key = f"{year}-{month:02d}"

        if date_key not in budgets:
            budgets[date_key] = {'actual_income': 0, 'expected_income': 0, 'actual_expenses': [],
                                 'expected_expenses': []}

        income = float(input("Enter the expected income for this month: "))
        budgets[date_key]['expected_income'] = income
        print(f"Expected income for {date_key} set to {income}.")

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

    while True:
        try:
            year = int(input("\nEnter the year of the budget to edit/delete (e.g., 2024): "))
            if year < 1900 or year > 2100:
                print("Please enter a realistic year (e.g., between 1900 and 2100).")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the year.")

    while True:
        try:
            month = int(input("Enter the month of the budget to edit/delete (1-12): "))
            if 1 <= month <= 12:
                break
            else:
                print("Invalid month. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for the month.")

    date_key = f"{year}-{month:02d}"

    if date_key not in budgets:
        print(f"\nNo budget found for {date_key}.")
        return

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

    budgets[date_key].setdefault(f'{budget_type}_income', 0)
    budgets[date_key].setdefault(f'{budget_type}_expenses', [])

    print(f"\n{budget_type.capitalize()} Budget for {date_key}:")
    print(f"Income: {budgets[date_key][f'{budget_type}_income']}")
    if budgets[date_key][f'{budget_type}_expenses']:
        print("Expenses:")
        for i, expense in enumerate(budgets[date_key][f'{budget_type}_expenses'], 1):
            print(f"{i}. {expense['name']}: {expense['amount']}")
    else:
        print("No expenses recorded.")

    while True:
        print("\nOptions:")
        print("1. Edit income")
        print("2. Edit an expense line item")
        print("3. Delete an expense line item")
        print("4. Delete the entire budget for this month")
        print("5. Exit to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            try:
                new_income = float(input("Enter the new income amount: "))
                budgets[date_key][f'{budget_type}_income'] = new_income
                print(f"{budget_type.capitalize()} income for {date_key} updated to {new_income}.")
            except ValueError:
                print("Invalid input. Please enter a numeric value for income.")

        elif choice == "2":
            if budgets[date_key][f'{budget_type}_expenses']:
                try:
                    item_index = int(input("Enter the number of the expense to edit: ")) - 1
                    if 0 <= item_index < len(budgets[date_key][f'{budget_type}_expenses']):
                        new_name = input(
                            f"Enter new name for "
                            f"{budgets[date_key][f'{budget_type}_expenses'][item_index]['name']}: "
                        )
                        new_amount = float(input(f"Enter new amount for {new_name}: "))
                        budgets[date_key][f'{budget_type}_expenses'][item_index] = {
                            'name': new_name,
                            'amount': new_amount
                        }
                        print(f"Expense updated: {new_name} - {new_amount}")
                    else:
                        print("Invalid item number.")
                except (ValueError, IndexError):
                    print("Invalid input. Please enter a valid expense number and amount.")
            else:
                print("No expenses to edit.")

        elif choice == "3":
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
            confirm = input(
                f"Are you sure you want to delete the entire {budget_type} "
                f"budget for {date_key}? (yes/no): "
            )
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

    while True:
        start_date_str = input("Enter the start date (YYYY-MM): ")
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m")
            break
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM format.")

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


def convert_currency():
    global budgets, currency

    if not budgets:
        print("\nNo budgets available for conversion.")
        return

    print("\nConvert Budgets to Another Currency")
    print("Supported currencies:", ", ".join(supported_currencies))
    while True:
        target_currency = input("Enter the target currency (USD, EUR, AUD, CAD): ").upper()
        if target_currency in supported_currencies:
            break
        else:
            print("Invalid currency. Please enter a supported currency.")

    data = {
        "budgets": budgets,
        "currency": target_currency
    }

    try:
        response = requests.post("http://127.0.0.1:5000/convert", json=data)
        if response.status_code == 200:
            converted_budgets = response.json()

            for date_key, converted_budget in converted_budgets.items():
                if date_key in budgets:
                    budgets[date_key].update(converted_budget)

            currency = target_currency

            save_budgets()

            print("\nBudgets successfully converted and saved.")
            print(f"Current currency is now {currency}.")
        else:
            print(f"Error: Microservice returned status code {response.status_code} with message: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the microservice: {e}")


def view_monthly_summary():
    if not budgets:
        print("\nNo budgets recorded. Add a budget first.")
        return

    while True:
        month = input("\nEnter the month (YYYY-MM) for the summary: ")
        if month in budgets:
            break
        else:
            print("Invalid month or no data available for the entered month. Try again.")

    data = {
        "month": month,
        "budgets": budgets
    }

    try:
        response = requests.post("http://127.0.0.1:5001/monthly_summary", json=data)

        if response.status_code == 200:
            summary = response.json()
            print(f"\nMonthly Summary for {summary['month']}:")
            print(f"Total Income: {summary['total_income']}")
            print(f"Total Expenses: {summary['total_expenses']}")
            print(f"Remaining Balance: {summary['remaining_balance']}")
            if summary["overspending_categories"]:
                print("\nOverspending Categories:")
                for category in summary["overspending_categories"]:
                    print(f"  {category['category']}: Spent {category['actual_spent']} "
                          f"(Expected: {category['expected_budget']}, Overspent: {category['overspend']})")
            else:
                print("No overspending categories found.")
        else:
            print(f"Error: {response.json().get('error', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the microservice: {e}")


def compare_range():
    start_date = input("\nEnter the start date (YYYY-MM): ")
    end_date = input("Enter the end date (YYYY-MM): ")

    data = {"start_date": start_date, "end_date": end_date, "budgets": budgets}

    try:
        response = requests.post("http://127.0.0.1:5002/compare/range", json=data)

        if response.status_code == 200:
            comparison = response.json()
            print(f"\nComparison for {start_date} to {end_date}:")
            print(f"Total Income Difference: {comparison['income_difference']}")
            print("\nCategory Trends:")
            for category, trends in comparison["category_trends"].items():
                print(f"  {category}: Overspent {trends['total_overspend']}, "
                      f"Underspent {trends['total_underspend']}")
        else:
            print(f"Error: {response.json().get('error', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the microservice: {e}")

main_menu()

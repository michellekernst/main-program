import json
import os

# files where user data is stored
DATA_FILE = "transactions.json"
BUDGET_FILE = "budget.json"

# -------------------------------
# DATA MANAGEMENT FUNCTIONS
# -------------------------------

def load_transactions():
    """
    Reads transactions from the JSON file.
    If the file does not exist, it creates an empty list.
    """
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_transactions(transactions):
    """
    Writes the current transactions list
    back into the JSON file.
    """
    with open(DATA_FILE, "w") as file:
        json.dump(transactions, file, indent=4)


# -------------------------------
# TRANSACTION FUNCTIONS
# -------------------------------

def add_transaction(transaction_type):
    """
    Adds a new income or expense transaction.
    """

    # load existing transactions
    transactions = load_transactions()

    # get transaction information from the user
    amount = input("Enter amount (or enter C to cancel): ")

    if amount.upper() == "C":
        print("Transaction canceled.")
        return

    description = input("Enter description (or enter C to cancel): ")

    if description.upper() == "C":
        print("Transaction canceled.")
        return

    # create a new transaction record
    new_transaction = {
        "id": max([t["id"] for t in transactions], default=0) + 1,
        "type": transaction_type,
        "amount": amount,
        "description": description
    }

    print(f"""
    Type: {new_transaction['type']}
    Amount: ${new_transaction['amount']}
    Description: {new_transaction['description']}
    """)
    
    confirm = input("Do you want to add this transaction? (Y/N): ")

    if confirm.upper() == "Y":
        # add the new transaction to the list
        transactions.append(new_transaction)

        # save updated list to JSON file
        save_transactions(transactions)

        print("Transaction saved successfully!")

    else:
        print("Transaction canceled.")
        return

def view_transactions():
    """
    Display all transactions saved in the JSON file.
    """

    transactions = load_transactions()

    print("""
================================
VIEW TRANSACTIONS
================================
        """)

    if len(transactions) == 0:
        print("No transactions found.")
        return

    # display each transaction
    for transaction in transactions:
        print(
            f"ID: {transaction['id']} | "
            f"Type: {transaction['type']} | "
            f"Amount: ${transaction['amount']} | "
            f"Description: {transaction['description']}"
        )

def clear_transactions():
    """
    Deletes all transactions.
    """

    confirm = input("Are you sure you want to delete ALL transactions? (Y/N): ")

    if confirm.upper() == "Y":
        save_transactions([])
        print("All transactions have been deleted.")
    else:
        print("Operation canceled.")

def delete_transaction():
    """
    Deletes a transaction based on its ID.
    """

    view_transactions()

    transactions = load_transactions()

    transaction_id = input("\nEnter transaction ID to delete or ALL to delete all transactions: ")

    if transaction_id.upper() == "ALL":
        clear_transactions()
        return

    # validate input
    try:
        transaction_id = int(transaction_id)
    except ValueError:
        print("Invalid transaction ID.")
        return

    # find the transaction
    selected_transaction = None

    for transaction in transactions:
        if transaction["id"] == transaction_id:
            selected_transaction = transaction
            break

    if selected_transaction is None:
        print("Transaction not found.")
        return

    print(f"""
    Transaction Found:

    Type: {selected_transaction["type"]}
    Amount: ${selected_transaction["amount"]}
    Description: {selected_transaction["description"]}
    """)

    confirm = input("Delete this transaction? (Y/N): ")

    if confirm.upper() != "Y":
        print("Deletion canceled.")
        return

    # create a new list without the deleted transaction
    updated_transactions = []

    deleted = False

    for transaction in transactions:
        if transaction["id"] == transaction_id:
            deleted = True
        else:
            updated_transactions.append(transaction)

    # save updated transaction list
    save_transactions(updated_transactions)

    if deleted:
        print("Transaction deleted successfully!")
    else:
        print("Transaction not found.")

# -------------------------------
# BUDGET FUNCTIONS
# -------------------------------

def load_budget():
    if not os.path.exists(BUDGET_FILE):
        return 0

    with open(BUDGET_FILE, "r") as file:
        return json.load(file)["budget"]


def save_budget(budget):
    with open(BUDGET_FILE, "w") as file:
        json.dump({"budget": budget}, file, indent=4)


def budget_menu():
    while True:
        print("""
================================
BUDGET MENU
================================

1. Set Budget
- Set a goal amount to stay under or edit your existing budget

2. View Budget Status
- View how your income and expenses compare to the budget

3. Back
- Return to main menu
--------------------------------
""")

        choice = input("Enter choice: ")

        if choice == "1":
            budget = float(input("Enter your budget: $"))
            save_budget(budget)
            print("Budget saved!")

        elif choice == "2":
            budget = load_budget()

            transactions = load_transactions()

            spent = 0
            income = 0

            for transaction in transactions:
                if transaction["type"] == "Expense":
                    spent += float(transaction["amount"])

                elif transaction["type"] == "Income":
                    income += float(transaction["amount"])

            remaining_excluding_income = budget - spent
            remaining_including_income = remaining_excluding_income + income

            print(f"\nBudget: ${budget:.2f}")
            print(f"Income: ${income:.2f}")
            print(f"Spent: ${spent:.2f}")
            print(f"Remaining Budget Excluding Income: ${remaining_excluding_income:.2f}")
            print(f"Remaining Budget Including Income: ${remaining_including_income:.2f}")

        elif choice == "3":
            break

        else:
            print("Invalid option.")


# -------------------------------
# MENU NAV
# -------------------------------

def transactions_menu():
    """
    Displays the transaction submenu.
    """

    while True:
        print("""
================================
TRANSACTIONS MENU
================================

1. Add Income
- Report money earned

2. Add Expense
- Record money spent

3. View Transactions
- View existing transactions

4. Delete Transaction
- Remove a transaction

5. Back
- Return to main menu
--------------------------------
""")

        choice = input("Enter choice: ")

        if choice == "1":
            add_transaction("Income")

        elif choice == "2":
            add_transaction("Expense")

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            delete_transaction()

        elif choice == "5":
            break

        # check for valid input
        else:
            print("Invalid option.")


def main_menu():
    """
    Display main menu.
    """

    while True:
        print("""
================================
PERSONAL FINANCE TRACKER
================================
Welcome to the personal finance tracker!
Track your income and expenses.
This app helps you understand your spending and plan ahead.

--------------------------------
1. Transactions Menu
- Add, delete, and view income and expense

2. Budget Menu
- Set or edit your budget and view budget status

3. Exit
- Exit the application
--------------------------------
""")

        choice = input("Enter choice: ")

        if choice == "1":
            transactions_menu()

        elif choice == "2":
            budget_menu()

        elif choice == "3":
            print("Exiting application...")
            break

        # validate input
        else:
            print("Invalid option.")

main_menu()
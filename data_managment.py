import pandas as pd
from datetime import datetime
from utils import validate_index, get_valid_input

# Set pandas options to display more rows and columns
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.width', None)  # Allow unlimited width, to avoid wrapping lines
pd.set_option('display.max_colwidth', None)  # Prevent truncation of column content

def add_transaction(transactions: pd.DataFrame):
    today = datetime.today().date()

    # Validate date input
    new_date = None
    while new_date is None:
        date_input = input("\nType the DATE of the new transaction (YYYY-MM-DD): ")
        try:
            candidate = datetime.strptime(date_input, "%Y-%m-%d").date()
            if candidate > today:
                print("Invalid date. Transactions cannot be in the future.")
            else:
                new_date = candidate
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    # Validate category input
    new_category = None
    while new_category is None:
        candidate = input("\nType the CATEGORY of the new transaction: ").strip()
        if candidate == "":
            print("Category cannot be empty.")
        elif not candidate.replace(" ", "").isalpha():
            print("Invalid input. Please use only alphabetic characters for the category.")
        else:
            new_category = candidate.capitalize()

    # Validate description input
    new_description = None
    while new_description is None:
        candidate = input("\nType the DESCRIPTION of the new transaction: ").strip()
        if candidate == "":
            print("Description cannot be empty.")
        elif candidate.isnumeric():
            print("Invalid input. Description cannot be purely numeric.")
        else:
            new_description = candidate.capitalize()

    # Validate amount input
    new_amount = None
    while new_amount is None:
        candidate = input("\nType the AMOUNT of the new transaction: ")
        try:
            value = float(candidate)
            if value <= 0:
                print("Invalid value. Amount must be greater than zero.")
            else:
                new_amount = value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Validate type input
    new_type = None
    while new_type is None:
        candidate = input("\nType the TYPE of the new transaction (Expense or Income): ").strip().capitalize()
        if candidate not in ["Expense", "Income"]:
            print("Invalid type. Please enter either 'Expense' or 'Income'.")
        else:
            new_type = candidate

    # Create a new row as a dictionary and append it to the DataFrame
    new_row = {
        "Date": new_date,
        "Category": new_category,
        "Description": new_description,
        "Amount": new_amount,
        "Type": new_type
    }
    transactions.loc[len(transactions)] = new_row

    transactions.sort_values(by='Date', inplace=True)
    transactions.reset_index(drop=True, inplace=True)

    print("\nNew transaction added successfully!")
    print("\nNew Transaction Details:")
    print(new_row)

    return transactions

def view_transaction(transaction: pd.DataFrame):
    start_date = transaction["Date"].min()  # This will remain as datetime
    end_date = transaction["Date"].max()    # This will remain as datetime

    print(f"\nAvailable transaction dates: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    while True:
        try:
            date_input_init = input("\nType the start date (YYYY-MM-DD): ")
            valid_init_date = datetime.strptime(date_input_init, "%Y-%m-%d").date()

            date_input_end = input("Type the end date (YYYY-MM-DD): ")
            valid_end_date = datetime.strptime(date_input_end, "%Y-%m-%d").date()

            if valid_init_date > end_date or valid_end_date < start_date:  # Compare datetime objects
                print("\nNo transactions in the given date range. Please try again.")
                continue

            # Filter transactions by the user-provided date range
            transactions_range_date = transaction[transaction["Date"].between(valid_init_date, valid_end_date)]  # Use datetime objects

            if transactions_range_date.empty:  # Check if no transactions found
                print("\nNo transactions found in the selected date range. Please try again.")
                continue  # Skip to next iteration

            print("\nTransactions found:")
            print(transactions_range_date)
            return transactions_range_date

        except ValueError:
            print("\nInvalid date format. Please use YYYY-MM-DD.")  # Handling user mistakes

def edit_transactions(transactions: pd.DataFrame):
    today = datetime.today().date()  # Current date

    print(transactions)  # Display transactions

    # Get transaction index with proper validation
    index_transaction = get_valid_input(
        "Enter the INDEX of the transaction to edit",
        None,
        lambda i: validate_index(i, transactions)
    )

    print("\nCurrent Transaction Details:")
    # Copy the row and format date
    transaction_details = transactions.iloc[index_transaction].copy()
    transaction_details["Date"] = transaction_details["Date"].strftime("%Y-%m-%d")
    print(transaction_details)

    # Get updated values, now using the date object directly for the default value
    new_date = get_valid_input(
        "Enter new DATE (YYYY-MM-DD)",
        transactions.at[index_transaction, "Date"],
        lambda d: datetime.strptime(d, "%Y-%m-%d").date() if datetime.strptime(d, "%Y-%m-%d").date() <= today else (_ for _ in ()).throw(ValueError("Date cannot be in the future"))
    )

    new_category = get_valid_input(
        "Enter new CATEGORY",
        transactions.at[index_transaction, "Category"],
        lambda c: c.capitalize()
    )

    new_description = get_valid_input(
        "Enter new DESCRIPTION",
        transactions.at[index_transaction, "Description"],
        lambda d: d
    )

    new_amount = get_valid_input(
        "Enter new AMOUNT",
        transactions.at[index_transaction, "Amount"],
        lambda a: float(a) if float(a) > 0 else (_ for _ in ()).throw(ValueError("Amount must be greater than zero"))
    )

    new_type = get_valid_input(
        "Enter new TYPE (Expense/Income)",
        transactions.at[index_transaction, "Type"],
        lambda t: t.capitalize() if t.capitalize() in ["Expense", "Income"] else (_ for _ in ()).throw(ValueError("Must be 'Expense' or 'Income'"))
    )

    transactions.loc[index_transaction, "Date"] = new_date
    transactions.loc[index_transaction, "Category"] = new_category
    transactions.loc[index_transaction, "Description"] = new_description
    transactions.loc[index_transaction, "Amount"] = new_amount
    transactions.loc[index_transaction, "Type"] = new_type

    print("\n✅ Transaction updated successfully!")
    print("\nUpdated Transaction Details:")
    updated_transaction = transactions.iloc[index_transaction].copy()
    updated_transaction["Date"] = updated_transaction["Date"].strftime("%Y-%m-%d")
    print(updated_transaction)


def delete_transaction(transaction: pd.DataFrame):
    while True:
        try:
            print("\nCurrent Transaction List:\n", transaction)  # Show transactions before deletion

            index_transaction_del = input(
                "\nChoose the INDEX of the transaction that you want to DELETE (or type 'C' to cancel): ").strip().capitalize()

            if index_transaction_del == "C":  # Allow user to cancel
                print("\nDeletion canceled.")
                break  # Exit function

            if not index_transaction_del.isdigit():  # Ensure it's a valid number
                print("\nThe index must be a number. Please try again.")
                continue

            index_transaction_del = int(index_transaction_del)

            if index_transaction_del < 0 or index_transaction_del >= len(transaction):  # Check if index is valid
                print("\nInvalid index. Please choose a valid transaction.")
                continue

            print("\nCurrent Transaction Details:")
            print(transaction.iloc[index_transaction_del])  # Show selected transaction

            confirm_del = input("\nAre you sure you want to delete this transaction? (Y to confirm, N to cancel): ").strip().capitalize()
            print("\nWARNING! This Processes isn't reversible.")
            if confirm_del == "Y":
                transaction.drop(index_transaction_del, inplace = True)  # Delete the row
                transaction.reset_index(drop = True, inplace = True)  # Reset index after deletion
                print("\nTransaction deleted successfully!")

                print("\nUpdated Transaction List:\n", transaction)  # Show updated transactions

                # Ask user if they want to delete another transaction
                new_del = input("\nWould you like to delete another transaction? (Y/N): ").strip().capitalize()
                if new_del == "N":
                    print("\nAll done. See you next time!")
                    break  # Exit loop

            elif confirm_del == "N":
                print("\nOperation canceled.")
                break

            else:
                print("\nInvalid input. Please enter Y or N.")

        except ValueError:
            print("\nInvalid input. Please try again.")



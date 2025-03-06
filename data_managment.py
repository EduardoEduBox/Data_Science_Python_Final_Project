"""Data Management

Final Project: Personal Finance Tracker App

View Transactions by Date Range: Filter and display transactions within a
specified date range.

Add a Transaction: Add a new transaction with details like date, category,
description, and amount.

Edit a Transaction: Modify details of an existing transaction (date,
category, description, amount).

Delete a Transaction: Remove a specific transaction by its index.
"""

import pandas as pd
from datetime import datetime

"""
                                             VIEWING TRANSACTIONS FUNCTION
"""

df = pd.read_csv("transactions.csv")
df["Date"] = pd.to_datetime(df["Date"]) # Changing datatype to datetime

print(df.head())

def view_transaction(transaction):

    start_date = transaction["Date"].min() # Variable with the newest date
    end_date = transaction["Date"].max() # Variable with the oldest date

    print(f"\nAvailable transaction dates: {start_date.date()} to {end_date.date()}")

    while True:
        try:
            date_input_init = input("\nType the start date (YYYY-MM-DD): ")
            valid_init_date = datetime.strptime(date_input_init, "%Y-%m-%d") # Converting the user input to datetime

            date_input_end = input("Type the end date (YYYY-MM-DD): ")
            valid_end_date = datetime.strptime(date_input_end, "%Y-%m-%d") # Converting the user input to datetime

            if valid_init_date > end_date or valid_end_date < start_date:  # Check if dates are invalid
                print("\nNo transactions in the given date range. Please try again.")
                continue

            transactions_range_date = transaction[transaction["Date"].between(valid_init_date, valid_end_date)] # Filter transactions by date range

            if transactions_range_date.empty: # Check if no transactions found
                print("\nNo transactions found in the selected date range. Please try again.")
                continue # Skip to next iteration

            print("\nTransactions found:")
            print(transactions_range_date)
            return transactions_range_date

        except ValueError:
            print("\nInvalid date format. Please use YYYY-MM-DD.") #handling user mistakes

view_transaction(df)

"""
                                             ADDING TRANSACTIONS FUNCTION
"""

file_path = "transactions.csv"  # Ensure the correct file path
df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"])

def add_transaction():
    today = pd.to_datetime("today").date()

    # Store values separately
    new_type = None
    new_date = None
    new_amount = None
    new_category = None
    new_description = None

    while new_date is None:  # Ask only if new_date is missing
        try:
            date_input = input("\nType the DATE of the new transaction (YYYY-MM-DD): ")
            new_date = datetime.strptime(date_input, "%Y-%m-%d").date()
            if new_date > today:
                print("\n Invalid date. Transactions cannot be in the future.")
                new_date = None  # Reset value
        except ValueError:
            print("\n Invalid date format. Please use YYYY-MM-DD.")

    while new_category is None:  # Ask only if new_category is missing
        try:
            new_category = (input("\nType the CATEGORY of the new transaction: ")).strip()
            if not new_category:
                print("\n Category cannot be empty.")
                new_category = None
            elif not new_category.isalpha():
                print("\n Invalid input. Please try again.")
                new_category = None
        except ValueError:
            print("\n Invalid input. Please try again.")

    while not new_description:  # Ask only if new_description is missing
        try:
            new_description = (input("\nType the DESCRIPTION of the new transaction: ")).strip()
            if not new_description:
                print("\n Description cannot be empty.")
                new_description = None
            elif new_description.isnumeric():
                print("\n Invalid input. Please try again.")
                new_description = None
        except ValueError:
            print("\n Invalid input. Please try again.")

    while new_amount is None:  # Ask only if new_amount is missing
        try:
            new_amount = float(input("\nType the AMOUNT of the new transaction: "))
            if new_amount <= 0:
                print("\n Invalid value. Amount must be greater than zero.")
                new_amount = None  # Reset value
        except ValueError:
            print("\n Invalid input. Please try again.")

    while new_type is None:
        try:
            new_type = input("\nType the TYPE of the new transaction (Expense or Income): ").strip().capitalize()
            if new_type != "Expense" and new_type != "Income":
                print("\nThe type cannot be empty. Please enter only -> Expense or Income <- ")
                new_type = None
        except ValueError:
            print("\n Invalid input. Please try again.")
    # New transaction as a DataFrame
    new_tran = pd.DataFrame([{
        "Date": new_date,
        "Category": new_category.capitalize(),
        "Description": new_description.capitalize(),
        "Amount": new_amount,
        "Type": new_type.capitalize()
    }])

    # Append to CSV
    new_tran.to_csv(file_path, mode='a', header=False, index=False)
    print("\n New transaction added successfully!")

    # Reload and print last few transactions
    df_updated = pd.read_csv(file_path)
    print(df_updated.tail())

    return new_tran  # Return the new transaction for further use
add_transaction()


"""
                                             EDITING TRANSACTIONS FUNCTION
"""
# def edit():






"""
                                             ADDING TRANSACTIONS FUNCTION
"""
# def delete():





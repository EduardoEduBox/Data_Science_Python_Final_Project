import tkinter as tk
from tkinter import filedialog
import pandas as pd
from data_managment import add_transaction, view_transaction, delete_transaction, edit_transactions
from visualization import spending_by_categories, monthly_spending_trend, spending_distribution
from data_analysis import monthly_spending, top_5_spending_categories, spending_by_category

# Required fields for the CSV file
required_fields = {'Date', 'Category', 'Description', 'Amount', 'Type'}


def print_options():
    print("""
    === Personal Finance Tracker ===
        0. Import a CSV File
        1. View All Transactions
        2. View Transactions by Date Range
        3. Add a Transaction
        4. Edit a Transaction
        5. Delete a Transaction
        6. Analyze Spending by Category
        7. Calculate Average Monthly Spending
        8. Show Top Spending Category
        9. Visualize Monthly Spending Trend
        10. Save Transactions to CSV
        11. Exit
        Choose an option (1-11)
    """)


def run_application(transactions: pd.DataFrame):
    if transactions.empty:
        print("\nYour database is empty! Please select a new one.\n")
        return

    if not required_fields.issubset(transactions.columns):
        print("\nThe required fields do not match your database\n")
        return

    while True:
        print_options()
        try:
            user_choice = int(input("Please, select your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number corresponding to an option.")
            continue

        if user_choice == 0:
            choose_file()  # Open new file dialog
            return  # Exit the current loop to avoid nested loops
        elif user_choice == 1:
            print(transactions)
        elif user_choice == 2:
            view_transaction(transactions)
        elif user_choice == 3:
            add_transaction(transactions)
        elif user_choice == 4:
            edit_transactions(transactions)
        elif user_choice == 5:
            delete_transaction(transactions)
        elif user_choice == 6:
            spending_by_categories(transactions)
        elif user_choice == 7:
            df_monthly = monthly_spending(transactions)
            monthly_spending_trend(df_monthly)
        elif user_choice == 8:
            total_spent_by_cat = spending_by_category(transactions)  # Returns a Series
            top_5_spending_categories(total_spent_by_cat)
        elif user_choice == 9:
            spending_distribution(transactions)
        elif user_choice == 10:
            transactions.to_csv("transactions.csv", index=False)
            print("Transactions saved to transactions.csv")
        elif user_choice == 11:
            print("Exiting application.")
            break
        else:
            print("Please select a valid choice.")


def choose_file():
    # Create a temporary Tk window for file selection
    temp_root = tk.Tk()
    temp_root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Choose a CSV File",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )
    temp_root.destroy()  # Destroy the temporary window

    if file_path:
        data = pd.read_csv(file_path)
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        df.sort_values(by='Date', inplace=True)

        if not required_fields.issubset(df.columns):
            print("\nThe required fields do not match your database.\n")

        else:
            print("\nCSV file loaded successfully!")
            run_application(df)
    else:
        print("No file selected.")


def setup_gui():
    global root
    root = tk.Tk()
    root.withdraw()  # Initially hide the main window
    choose_file()


if __name__ == '__main__':
    setup_gui()

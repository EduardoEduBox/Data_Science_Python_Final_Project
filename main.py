import tkinter as tk
from tkinter import filedialog
import pandas as pd

required_fields = {'Date', 'Category', 'Description', 'Amount', 'Type'}

# The function to let the user choose a CSV file
def choose_file():
    # Hide the root window
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Choose a CSV File",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )

    # Check if a file was selected
    if file_path:
        data = pd.read_csv(file_path)
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime

        if not required_fields.issubset(df.columns):
            print("\nThe required fields do not match your database.\n")
        else:
            print("\nCSV file loaded successfully!")
            run_application(df)  # Start the app with the loaded CSV


# Function to display options to the user
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


# Function to run the application with transactions loaded
def run_application(transactions: pd.DataFrame):
    if transactions.empty:
        print("\nYour database is empty! Please select a new one.\n")
        return

    if not required_fields.issubset(transactions.columns):
        print("\nThe required fields do not match your database\n")
        return

    print_options()

    while True:
        user_choice = int(input("Please, select your choice: "))

        if user_choice == 0:
            choose_file()  # Let the user select a new file
        elif user_choice == 1:
            print(transactions)  # Example: Show all transactions
        elif user_choice == 11:
            print("Exiting application.")
            break
        else:
            print("Please select a valid choice.")


# Setting up the Tkinter interface
def setup_gui():
    # Create the main window but don't show it
    global root
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Start the process by showing the file dialog
    choose_file()

# Start the application
setup_gui()

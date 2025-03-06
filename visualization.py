import pandas as pd
import matplotlib.pyplot as plt
# from data_analysis import monthly_spending

# These lines are test for now
df = pd.read_csv('transactions.csv')
df = pd.DataFrame(df)
df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime

def monthly_spending_trend(formated: pd.DataFrame):
    """
    Function to plot the monthly spending trend.

    :param formated: A pandas DataFrame with 'Date' and 'Amount' columns.
    """
    if formated.empty:
        print("No data available to plot.")
        return

    plt.figure(figsize=(16, 8))  # Set figure size
    plt.plot(formated['Date'], formated['Amount'], marker='o', linestyle='-', color='b', label='Spending')

    plt.title('Monthly Spending Trend')
    plt.xlabel('Date')
    plt.ylabel('Amount Spent ($)')
    plt.xticks(rotation=23)  # Rotate dates for better visibility
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# monthly_spending_trend(monthly_spending(df))

df['Date'] = pd.to_datetime(df['Date']) # Convert 'Date' column to datetime type
expenses = df[df['Type'] == 'Expense'] # Filter only expenses
daily_expenses = expenses.groupby('Date')['Amount'].sum() # Group by Date and sum up the expenses

all_dates = pd.date_range(start=daily_expenses.index.min(), end=daily_expenses.index.max(), freq='D')
daily_expenses = daily_expenses.reindex(all_dates, fill_value=0)

daily_expenses.plot(kind= 'line', label='Daily Spending', marker= 'o', linestyle= '-', )

plt.title('Monthly Spending Trend')
plt.xlabel('Date')
plt.ylabel('Amount Spent ($)')
plt.grid(True)
plt.tight_layout()
plt.show()

# Spending by Category
spending_by_category = expenses.groupby('Category')['Amount'].sum() # Groups the expenses by Category and sum the Amount for each category

spending_by_category.plot(kind='bar')
plt.title('Total Spending by Category')
plt.xlabel('Category')
plt.ylabel('Amount Spent ($)')
plt.xticks(rotation= 0)
plt.show()

# Percentage Distribution
spending_by_category.plot(kind= 'pie', autopct='%1.1f%%', startangle= 90)
plt.title('Spending Distribution Across Categories')
plt.ylabel('')  # Remove the label
plt.show()

import pandas as pd

def spending_by_category(transactions):
    """
    Function to check the spending by each category

    :param transactions: original pandas dataframe
    :return: total by category
    """
    # Breaking the function if the value is nothing
    if transactions.empty:
        print("No transactions available.")
        return

    total_by_category = transactions.groupby('Category')['Amount'].sum()
    total_by_category = total_by_category.sort_values(ascending=False)
    print("\nTotal spent by category:\n")
    # returning it because the function that returns the Top 10 categories need it
    return total_by_category


def monthly_spending(transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Groups transactions by Year-Month and returns a DataFrame
    with columns ['Date', 'Amount'] where Amount is the total monthly spending.
    This function does not modify the original transactions DataFrame.
    """
    if transactions.empty:
        print("No transactions available.")
        return pd.DataFrame()

    # Work on a copy so the original DataFrame remains unmodified
    df = transactions.copy()

    # Convert 'Date' to a proper datetime if it's not already
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Create a 'YearMonth' column (e.g., 2024-10, 2024-11, etc.)
    df['YearMonth'] = df['Date'].dt.to_period('M')

    # Sum up the 'Amount' for each month (or use .mean() if desired)
    monthly_totals = df.groupby('YearMonth')['Amount'].sum().reset_index()

    # Convert the YearMonth period to a real timestamp for plotting
    monthly_totals['Date'] = monthly_totals['YearMonth'].dt.to_timestamp()

    # Drop the 'YearMonth' column so only 'Date' and 'Amount' remain
    monthly_totals.drop(columns='YearMonth', inplace=True)

    # Sort by date ascending
    monthly_totals.sort_values(by='Date', inplace=True)

    print("\nMonthly spending (aggregated):\n", monthly_totals)
    return monthly_totals


def top_5_spending_categories(transactions_by_category):
    """
    Prints the top 5 categories from a Series of total spending by category.
    """
    # If the user canceled or there's no data
    if transactions_by_category is None or transactions_by_category.empty:
        print("No spending data provided.")
        return

    print("\nTop 5 Spending Categories:\n")
    print(transactions_by_category.head())

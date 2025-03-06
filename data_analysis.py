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


def monthly_spending(transactions):
    """
    Function to check the monthly spending

    :param transactions: original pandas dataframe
    :return: total by month as a DataFrame
    """
    if transactions.empty:
        print("No transactions available.")
        return pd.DataFrame()  # Return empty DataFrame instead of None

    transactions["Date"] = pd.to_datetime(transactions["Date"])  # Ensure Date is datetime type
    total_by_month = transactions.groupby('Date')["Amount"].sum()

    total_by_month = total_by_month.sort_index(ascending=False).reset_index()  # Reset index

    print("\nTotal spent monthly:\n")
    return total_by_month


def top_5_spending_categories(transactions_by_category):
    """
    Function to grab the top 5 categories that the user spends the most

    :param transactions_by_category: function that grabs the spending by category
    """
    if not transactions_by_category:
        print("Getter function not provided")
        return

    print(transactions_by_category.head())
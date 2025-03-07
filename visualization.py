import pandas as pd
import matplotlib.pyplot as plt

def monthly_spending_trend(formated: pd.DataFrame):
    """
    Function to plot the monthly spending trend.
    Expects a DataFrame with columns 'Date' and 'Amount' (monthly aggregates).
    """
    if formated.empty:
        print("No data available to plot.")
        return

    plt.figure(figsize=(16, 8))

    plt.plot(
        formated['Date'], formated['Amount'],
        marker='o', markersize=8, linestyle='-', linewidth=2.5,
        color='#2E8B57', label='Monthly Spending', alpha=0.85
    )

    plt.title('Monthly Spending Trend', fontsize=16, fontweight='bold', pad=15)
    plt.xlabel('Date', fontsize=14, fontweight='bold', labelpad=10)
    plt.ylabel('Amount Spent ($)', fontsize=14, fontweight='bold', labelpad=10)

    plt.xticks(rotation=30, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.gca().set_facecolor('#f7f7f7')
    plt.legend(fontsize=12, loc='upper right', frameon=False)

    plt.tight_layout()
    plt.show()


def spending_by_categories(database: pd.DataFrame):
    """
    Function to plot as a bar chart the spending by category, descending order

    :param database: The Pandas dataframe with the transactions information
    """

    if database.empty:
        print("No transactions available.")
        return

    expenses = database.query('Type == "Expense"')

    if expenses.empty:
        print("No expenses found.")
        return

    spending_by_categories = expenses.groupby('Category')['Amount'].sum()
    spending_by_categories = spending_by_categories.sort_values(ascending=False)

    # Improved Bar Chart Visualization
    fig, ax = plt.subplots(figsize=(12, 6))  # Wider chart for clarity
    bars = spending_by_categories.plot(kind='bar', ax=ax)

    # Add labels on bars
    for bar in bars.patches:
        ax.annotate(f'${bar.get_height():,.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 5),  # Offset text above bar
                    textcoords='offset points',
                    ha='center', fontsize=10, fontweight='bold')

    plt.title('Total Spending by Category', fontsize=14, fontweight='bold')
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Amount Spent ($)', fontsize=12)
    plt.xticks(rotation=30, ha='right', fontsize=10)  # Better angle & alignment
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Light grid lines for better readability
    plt.tight_layout()
    plt.show()

def spending_distribution(database: pd.DataFrame):
    """
    Function to plot as a pie chart the distribution in percentage of the spending

    :param database: The Pandas dataframe with the transactions information
    """
    if database.empty:
        print("No transactions available.")
        return

    expenses = database.query('Type == "Expense"')

    if expenses.empty:
        print("No expenses found.")
        return

    spending_by_categories = expenses.groupby('Category')['Amount'].sum()

    # Improved Pie Chart Visualization
    explode = [0.05] * len(spending_by_categories)  # Slightly separate slices

    spending_by_categories.plot(
        kind='pie',
        autopct='%1.1f%%',
        startangle=140,  # Better alignment
        shadow=True,  # Add shadow for depth
        explode=explode,
        wedgeprops={'edgecolor': 'black', 'linewidth': 1}  # Add black edges
    )

    plt.title('Spending Distribution Across Categories', fontsize=14, fontweight='bold')
    plt.ylabel('')  # Remove default label
    plt.tight_layout()  # Optimize layout
    plt.show()
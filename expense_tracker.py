import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create sample dataset if CSV does not exist
if not os.path.exists("expenses.csv"):
    data = {
        "Date": ["2026-01-01", "2026-01-05", "2026-01-10",
                 "2026-02-02", "2026-02-10", "2026-02-15"],
        "Amount": [200, 500, 150, 300, 700, 250],
        "Category": ["Food", "Transport", "Food",
                     "Utilities", "Entertainment", "Transport"],
        "Description": ["Lunch", "Bus", "Dinner",
                        "Electricity", "Movie", "Auto"]
    }
    pd.DataFrame(data).to_csv("expenses.csv", index=False)


class ExpenseTracker:

    def __init__(self):
        self.file = "expenses.csv"
        self.df = pd.read_csv(self.file)
        self.df["Date"] = pd.to_datetime(self.df["Date"], errors="coerce")
        self.df["Amount"] = pd.to_numeric(
            self.df["Amount"], errors="coerce"
        )
        self.df = self.df.dropna(
            subset=["Date", "Amount", "Category"]
        )
        self.df = self.df[self.df["Amount"] > 0]
        self.df["Category"] = self.df["Category"].astype(str).str.strip()
        self.df = self.df[self.df["Category"] != ""]
        self.df = self.df.reset_index(drop=True)

    # Add a new expense
    def add_expense(self, date, amount, category, description):
        new_expense = {
            "Date": pd.to_datetime(date),
            "Amount": amount,
            "Category": category,
            "Description": description
        }

        self.df.loc[len(self.df)] = new_expense
        self.df.to_csv(self.file, index=False)
        print("Expense added successfully!")

    # Display total and average expenses
    def get_summary(self):
        if self.df.empty:
            print("No expenses available.")
            return

        amounts = self.df["Amount"].to_numpy()

        print("\n----- EXPENSE SUMMARY -----")
        print("Total Expenses:", np.sum(amounts))
        print("Average Expense:", round(np.mean(amounts), 2))
        print("Number of Expenses:", len(amounts))

        print("\nCategory-wise Total:")
        print(self.df.groupby("Category")["Amount"].sum())

        print("\nMonthly Expenses:")
        monthly = self.df.groupby(
            self.df["Date"].dt.to_period("M")
        )["Amount"].sum()
        print(monthly)

    # Filter expenses
    def filter_expenses(self):
        print("\n1. Filter by Category")
        print("2. Filter by Date Range")
        print("3. Filter by Amount")

        choice = input("Choose filter: ")
        result = self.df.copy()

        if choice == "1":
            category = input("Enter category: ")
            result = result[
                result["Category"].str.lower() == category.lower()
            ]

        elif choice == "2":
            try:
                start = pd.to_datetime(input("Start date (YYYY-MM-DD): "))
                end = pd.to_datetime(input("End date (YYYY-MM-DD): "))

                if start > end:
                    print("Start date must be before end date.")
                    return

                result = result[
                    (result["Date"] >= start) &
                    (result["Date"] <= end)
                ]
            except ValueError:
                print("Invalid date!")
                return

        elif choice == "3":
            try:
                amount = float(input("Enter minimum amount: "))
                if amount < 0:
                    print("Amount cannot be negative.")
                    return
                result = result[result["Amount"] >= amount]
            except ValueError:
                print("Invalid amount!")
                return

        else:
            print("Invalid choice!")
            return

        if result.empty:
            print("No matching expenses found.")
        else:
            print(result.to_string(index=False))

    # Generate report
    def generate_report(self):
        if self.df.empty:
            print("No expenses available for the report.")
            return

        print("\n========== EXPENSE REPORT ==========")
        print("Total Spending:", round(self.df["Amount"].sum(), 2))
        print("Average Spending:", round(self.df["Amount"].mean(), 2))
        print("Highest Expense:", self.df["Amount"].max())
        print("Lowest Expense:", self.df["Amount"].min())

        category_total = self.df.groupby("Category")["Amount"].sum()
        print("Highest Spending Category:", category_total.idxmax())
        print("Category-wise Spending Percentage:")
        print((category_total / category_total.sum() * 100).round(2))

    # Create all four charts
    def visualize(self):
        if self.df.empty:
            print("No data available for visualization.")
            return

        data = self.df.copy()
        data["Month"] = data["Date"].dt.to_period("M").astype(str)

        # 1. Bar Chart
        category_total = data.groupby("Category")["Amount"].sum()
        category_total.plot(kind="bar", title="Total Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.tight_layout()
        plt.show()

        # 2. Line Graph
        monthly = data.groupby("Month")["Amount"].sum()
        monthly.plot(kind="line", marker="o", title="Monthly Spending Trend")
        plt.xlabel("Month")
        plt.ylabel("Amount")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # 3. Pie Chart
        category_total.plot(
            kind="pie",
            autopct="%1.1f%%",
            title="Spending Distribution"
        )
        plt.ylabel("")
        plt.tight_layout()
        plt.show()

        # 4. Histogram using Seaborn
        sns.histplot(data=data, x="Amount", bins=5, kde=True)
        plt.title("Frequency of Expense Amounts")
        plt.xlabel("Amount")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()


# Main program
tracker = ExpenseTracker()

while True:
    print("\n====== SMART EXPENSE TRACKER ======")
    print("1. Add Expense")
    print("2. View Summary")
    print("3. Filter Expenses")
    print("4. Generate Report")
    print("5. Show Charts")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        try:
            date = input("Enter date (YYYY-MM-DD): ")
            date = pd.to_datetime(date, format="%Y-%m-%d")
            amount = float(input("Enter amount: "))

            if amount <= 0 or not np.isfinite(amount):
                print("Amount must be a positive number!")
                continue

            category = input("Enter category: ").strip()
            description = input("Enter description: ").strip()

            if not category or not description:
                print("Category and description cannot be empty!")
                continue

            tracker.add_expense(date, amount, category, description)

        except (ValueError, TypeError):
            print("Invalid date or amount!")

    elif choice == "2":
        tracker.get_summary()

    elif choice == "3":
        tracker.filter_expenses()

    elif choice == "4":
        tracker.generate_report()

    elif choice == "5":
        tracker.visualize()

    elif choice == "6":
        print("Thank you for using Smart Expense Tracker!")
        break

    else:
        print("Invalid choice! Please try again.")

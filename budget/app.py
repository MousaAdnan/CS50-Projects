import csv
from datetime import datetime

# File paths
EXPENSES_FILE = 'expenses.csv'
INCOME_FILE = 'income.csv'

def main():
    while True:
        print("\nPersonal Budget Tracker")
        print("1. Add Expense")
        print("2. Add Income")
        print("3. View Summary")
        print("4. Generate Report")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            add_income()
        elif choice == "3":
            view_summary()
        elif choice == "4":
            generate_report()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

def add_expense():
    category = input("Enter expense category (e.g., Food, Utilities, Entertainment): ")
    amount = float(input("Enter expense amount: "))
    date = datetime.now().strftime('%Y-%m-%d')

    with open(EXPENSES_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])

    print(f"Added expense of {amount} in {category} category.")

def add_income():
    source = input("Enter income source (e.g., Salary, Freelance): ")
    amount = float(input("Enter income amount: "))
    date = datetime.now().strftime('%Y-%m-%d')

    with open(INCOME_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, source, amount])

    print(f"Added income of {amount} from {source}.")

def view_summary():
    month = input("Enter month (YYYY-MM) to view summary: ")
    total_expenses = 0
    total_income = 0

    with open(EXPENSES_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0].startswith(month):
                total_expenses += float(row[2])

    with open(INCOME_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0].startswith(month):
                total_income += float(row[2])

    print(f"\nSummary for {month}")
    print(f"Total Income: ${total_income}")
    print(f"Total Expenses: ${total_expenses}")
    print(f"Net Savings: ${total_income - total_expenses}")

def generate_report():
    month = input("Enter month (YYYY-MM) for report: ")
    report_file = f"report_{month}.csv"

    with open(report_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount"])

        with open(EXPENSES_FILE, 'r') as expenses:
            reader = csv.reader(expenses)
            for row in reader:
                if row[0].startswith(month):
                    writer.writerow(row)

        writer.writerow([])
        writer.writerow(["Date", "Source", "Amount"])

        with open(INCOME_FILE, 'r') as income:
            reader = csv.reader(income)
            for row in reader:
                if row[0].startswith(month):
                    writer.writerow(row)

    print(f"Report generated: {report_file}")

if __name__ == "__main__":
    main()

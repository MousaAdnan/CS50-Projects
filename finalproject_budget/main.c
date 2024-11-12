#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "helpers.h"

// Function prototypes
void add_entry();
void view_balance();
void summary_by_category();

int main() {
    int choice;
    printf("Welcome to Personal Budget Tracker\n");

    do {
        printf("\nMenu:\n");
        printf("1. Add Entry\n");
        printf("2. View Balance\n");
        printf("3. Summary by Category\n");
        printf("4. Exit\n");
        printf("Enter choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                add_entry();
                break;
            case 2:
                view_balance();
                break;
            case 3:
                summary_by_category();
                break;
            case 4:
                printf("Goodbye!\n");
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 4);

    return 0;
}

// Adds a new entry to the CSV file
void add_entry() {
    char date[11], category[20], description[50];
    float amount;
    int type;

    printf("Enter date (YYYY-MM-DD): ");
    scanf("%10s", date);  // Limiting input size to prevent overflow
    printf("Enter amount: ");
    scanf("%f", &amount);
    printf("Enter type (1 for Income, 2 for Expense): ");
    scanf("%d", &type);
    printf("Enter category: ");
    scanf("%19s", category);
    printf("Enter description: ");
    scanf("%49s", description);

    if (type != 1 && type != 2) {
        printf("Invalid type. Please enter 1 for Income or 2 for Expense.\n");
        return;
    }

    if (write_entry("data.csv", date, amount, type, category, description)) {
        printf("Entry added successfully!\n");
    } else {
        printf("Failed to add entry.\n");
    }
}

// Views the current balance by summing income and expenses
void view_balance() {
    float balance = calculate_balance("data.csv");
    printf("Current Balance: $%.2f\n", balance);
}

// Shows a summary of expenses by category
void summary_by_category() {
    print_category_summary("data.csv");
}

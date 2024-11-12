#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "helpers.h"

#define MAX_LINE 1024
#define MAX_CATEGORIES 100

// Writes a new entry to the CSV file
int write_entry(const char *filename, const char *date, float amount, int type, const char *category, const char *description) {
    FILE *file = fopen(filename, "a");
    if (!file) {
        perror("Error opening file");
        return 0;
    }
    fprintf(file, "%s,%.2f,%d,%s,%s\n", date, amount, type, category, description);
    fclose(file);
    return 1;
}

// Calculates the current balance from the CSV file
float calculate_balance(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Error opening file");
        return 0;
    }

    float balance = 0.0;
    char line[MAX_LINE];
    while (fgets(line, sizeof(line), file)) {
        char *date = strtok(line, ",");
        char *amount_str = strtok(NULL, ",");
        char *type_str = strtok(NULL, ",");
        float amount = atof(amount_str);
        int type = atoi(type_str);

        if (type == 1) {
            balance += amount;
        } else if (type == 2) {
            balance -= amount;
        }
    }
    fclose(file);
    return balance;
}

// Prints a summary of expenses by category
void print_category_summary(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Error opening file");
        return;
    }

    float category_totals[MAX_CATEGORIES] = {0};
    char categories[MAX_CATEGORIES][20];
    int category_count = 0;

    char line[MAX_LINE];
    while (fgets(line, sizeof(line), file)) {
        char *date = strtok(line, ",");
        char *amount_str = strtok(NULL, ",");
        char *type_str = strtok(NULL, ",");
        char *category = strtok(NULL, ",");

        // Verify parsing success and ensure data is for an expense
        if (amount_str && type_str && category && atoi(type_str) == 2) {
            float amount = atof(amount_str);
            int found = 0;

            // Check if the category already exists in our array
            for (int i = 0; i < category_count; i++) {
                if (strcmp(categories[i], category) == 0) {
                    category_totals[i] += amount;
                    found = 1;
                    break;
                }
            }

            // If not found, add new category to the array
            if (!found && category_count < MAX_CATEGORIES) {
                strcpy(categories[category_count], category);
                category_totals[category_count] = amount;
                category_count++;
            }
        }
    }
    fclose(file);

    // Print the summary of expenses by category
    printf("Expense Summary by Category:\n");
    for (int i = 0; i < category_count; i++) {
        printf("%s: $%.2f\n", categories[i], category_totals[i]);
    }
}

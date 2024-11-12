#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "helpers.h"

#define MAX_LINE 1024
#define MAX_CATEGORIES 100

// Prints a summary of expenses by category
void print_category_summary(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Error opening file");
        return;
    }

    // Arrays to hold category names and totals
    float category_totals[MAX_CATEGORIES] = {0};
    char categories[MAX_CATEGORIES][20];
    int category_count = 0;

    char line[MAX_LINE];
    while (fgets(line, sizeof(line), file)) {
        // Parse the line with error checking for each field
        char *date = strtok(line, ",");
        char *amount_str = strtok(NULL, ",");
        char *type_str = strtok(NULL, ",");
        char *category = strtok(NULL, ",");

        // Verify all fields are parsed and type is '2' (expense)
        if (date && amount_str && type_str && category && atoi(type_str) == 2) {
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
    if (category_count == 0) {
        printf("No expenses found.\n");
    } else {
        printf("Expense Summary by Category:\n");
        for (int i = 0; i < category_count; i++) {
            printf("%s: $%.2f\n", categories[i], category_totals[i]);
        }
    }
}

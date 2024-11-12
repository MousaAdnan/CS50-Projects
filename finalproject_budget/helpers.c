#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "helpers.h"

#define MAX_LINE 1024

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

    float category_totals[100] = {0};
    char categories[100][20];
    int category_count = 0;

    char line[MAX_LINE];
    while (fgets(line, sizeof(line), file)) {
        char *date = strtok(line, ",");
        char *amount_str = strtok(NULL, ",");
        char *type_str = strtok(NULL, ",");
        char *category = strtok(NULL, ",");
        float amount = atof(amount_str);
        int type = atoi(type_str);

        if (type == 2) {
            int found = 0;
            for (int i = 0; i < category_count; i++) {
                if (strcmp(categories[i], category) == 0) {
                    category_totals[i] += amount;
                    found = 1;
                    break;
                }
            }
            if (!found && category_count < 100) {
                strcpy(categories[category_count], category);
                category_totals[category_count] = amount;
                category_count++;
            }
        }
    }
    fclose(file);

    printf("Expense Summary by Category:\n");
    for (int i = 0; i < category_count; i++) {
        printf("%s: $%.2f\n", categories[i], category_totals[i]);
    }
}

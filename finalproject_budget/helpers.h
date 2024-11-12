#ifndef HELPERS_H
#define HELPERS_H

int write_entry(const char *filename, const char *date, float amount, int type, const char *category, const char *description);
float calculate_balance(const char *filename);
void print_category_summary(const char *filename);

#endif

#include "cs50.h"
#include <stdio.h>

int getCents(void);
int numOfQuarters(cents);

int main(void)
{
    int cents = getCents();
    int quarters = numOfQuarters(cents);
    cents = cents - quarters * 25;
}

int getCents(void)
{
    int cents;
    do
    {
        cents = get_int("Num of cents: ");
    }
    while (cents < 0);
    return cents;
}

int numOfQuarters(int cents)
{
    int dimes = cents / 10
    return dimes;
}

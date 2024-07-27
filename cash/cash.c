#include "cs50.h"
#include <stdio.h>

int getCents(void);
int numOfQuarters(int cents);
int numOfDimes(int cents);
int numOfNickels(int cents);
int numOfPennies(int cents);

int main(void)
{
    int cents = getCents();
    int quarters = numOfQuarters(cents);
    cents = cents - quarters * 25;

    int dimes = numOfDimes(cents);
    cents = cents - dimes * 10;

    int nickels = numOfNickels(cents);
    cents = cents - nickels*5;

    int pennies = numOfPennies(cents);
    cents = cents - pennies;

    int coins = dimes + pennies + nickels + quarters;

    printf("%i\n", coins);
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
    int quarters = cents / 25;
    return quarters;
}

int numOfDimes(int cents)
{
    int dimes = cents/10;
    return dimes;
}

int numOfNickels(int cents)
{
    int nickels = cents / 5;
    return nickels;
}

int numOfPennies(int cents)
{
    int pennies = cents;
    return pennies;
}

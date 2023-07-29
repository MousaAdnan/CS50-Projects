#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int age;
    do
    {
    age = get_int("What is the starting population size? ");
    }
    while (age < 9);

    int endAge;
    do
    {
        endAge = get_int("What is the ending population size? ");
    }
    while (endAge <= age);

    printf("%i, %i\n", age, endAge);

    // TODO: Prompt for end size

    // TODO: Calculate number of years until we reach threshold

    // TODO: Print number of years
}

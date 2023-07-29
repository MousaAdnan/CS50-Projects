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

    while(age < endAge)
    {
        age = (age + (age / 3) - (age / 4));
    }
    printf("%i/n", age);
    // TODO: Prompt for end size

    // TODO: Calculate number of years until we reach threshold

    // TODO: Print number of years
}

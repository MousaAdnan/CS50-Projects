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

    // TODO: Prompt for end size
    int endAge;
    do
    {
        endAge = get_int("What is the ending population size? ");
    }
    while (age > endAge);

    // TODO: Calculate number of years until we reach threshold
    int count = 0;
    while(age < endAge)
    {
        age = (age + (age / 3) - (age / 4));
        count++;
    }

    // TODO: Print number of years
    printf("Years: %i \n", count);
}

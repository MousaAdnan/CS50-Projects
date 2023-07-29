#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height = get_int("How tall should it be? ");
    int n = 0;
    while (n < height)
    {
        printf("#/n");
    }
}
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height = get_int("How tall should it be? ");
    int r = 0;
    while (r < height)
    {
        printf("#");
        r++;

        for (column = 0; column <= r; column++)
        {
            printf("#");
        }
        printf("\n");
    }

}
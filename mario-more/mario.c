#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height = get_int("How tall should it be? ");
    int row = 0;
    int column;
    while (row < height)
    {
        printf("#");
        for (column = 0; column <= row; column++)
        {
            printf("#");
        }
        row++;
        printf("\n");
    }

}
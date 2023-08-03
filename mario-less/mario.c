#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    int row = 0;
    int column;
    int gap;
    
    do
    {
        height = get_int("How tall should it be? ");
    }
    while (height < 1 || height > 8);

    while (row < height)
    {
        printf("#");
        for (gap = 0; gap < (height - row - 1); gap++)
        {
            printf(" ");
        }

        for (column = 0; column <= row; column++)
        {
            printf("#");
        }
        printf("\n");
        row++;
    }

}
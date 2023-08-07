#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool only_digits(string str);
int main(int argc, string argv[])
{
    int key = atoi(argv[1]);

    if (argc == 2)
    {
        if (only_digits(argv[1]) == true)
        {
            if (key >= 0 && key <= 9)
            {
                return 0;
            }
            else
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        else
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}

bool only_digits(string str)
{
    for (int n = 0; str[n] != '\0'; n++)
    {
        if (!isdigit(str[n]) && (str[n] < 0 || str[n] > 9))
        {
            return false;
        }
    }
    return true;
}
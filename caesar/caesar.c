#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

bool only_digits(string str);

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        return 0;
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    only_digits(argv[1]);
}

bool only_digits(string str)
{
    if (((char) str >= 0) && ((char) str <= 9))
    {
        return true;
    }
    else
    {
        return false;
        printf("Usage: ./caesar key\n");
        return 1;
    }
}
#include <cs50.h>
#include <stdio.h>
#include <string.h>

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
}

bool only_digits(string str)
{
    if (((int) str >= 0) && ((int) str <= 9))
    {
        return true;
    }
    else
    {
        return false;
    }
}
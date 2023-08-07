#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool only_digits(string str);
char rotate(char c, int i);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        if (only_digits(argv[1]) == true)
        {
            int key = atoi(argv[1]);

            string text = get_string("plaintext: ");
            printf("ciphertext: ");
            for (int x = 0; x < strlen(text); x++)
            {
                printf("%c", rotate(text[x], key));
            }
            printf("\n");
            return 0;
        }
        else
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
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

char rotate(char c, int i)
{
    if (c >= 'a' && c <= 'z')
    {
        c -= 'a';
        c = ;
        c += 'a';
    }
    else if (c >= 'A' && c <= 'Z')
    {
        c -= 'A';
        c += i;
        c += 'A';
    }
    return c;
}
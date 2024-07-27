#include <cs50.h>
#include <math.h>
#include <ctype.h>
#include <stdio.h>

int main(void)
{
    string text = get_string("Text: ");
    int letters = 0;
    int words = 0;
    int sentences = 0;
    char c;
    bool inWord = false;

    for (int n = 0; text[n] != '\0'; n++)
    {
        c = text[n];

        if (isalpha(c))
        {
            letters++;
        }

        if(isspace(c) || c == '\n')
        {
            if (inWord)
            {
                words++;
                inWord = false;
            }
        }
        else
        {
            inWord = true;
        }

        if (c == '.' || c == '!' || c == '?')
        {
            sentences++;
        }
    }

    if (inWord)
    {
        words++;
    }

    if (words == 0)
    {
        printf("Before Grade 1\n");
        return 0;
    }

    double L = (double) letters/ words * 100;
    double S = (double) sentences / words * 100;

    double index = 0.0588 * L - 0.296 * S - 15.8;
    int grade = (int) round (index);

    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else{
        printf("Grade %d\n", grade);
    }

    return 0;
}

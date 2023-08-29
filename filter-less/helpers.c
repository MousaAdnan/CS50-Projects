#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int n = 0; n < height; n++)
    {
        for (int m = 0; m < width; m++)
        {
            float red = image[n][m].rgbtRed;
            float green = image[n][m].rgbtGreen;
            float blue = image[n][m].rgbtBlue;

            int grey = round((red + green + blue) / 3);

            image[n][m].rgbtRed = grey;
            image[n][m].rgbtGreen = grey;
            image[n][m].rgbtBlue = grey;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int n = 0; n < height; n++)
    {
        for (int m = 0; m < width; m++)
        {
            float red = round(.393 * image[n][m].rgbtRed + .769 * image[n][m].rgbtGreen + .189 * image[n][m].rgbtBlue);
            float green = round(.349 * image[n][m].rgbtRed + .686 * image[n][m].rgbtGreen + .168 * image[n][m].rgbtBlue);
            float blue = round(.272 * image[n][m].rgbtRed + .534 * image[n][m].rgbtGreen + .131 * image[n][m].rgbtBlue);

            int sepiaRed = red;
            int sepiaGreen = green;
            int sepiaBlue = blue;

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            image[n][m].rgbtRed = sepiaRed;
            image[n][m].rgbtGreen = sepiaGreen;
            image[n][m].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int w = (width / 2);
    for (int n = 0; n < height; n++)
    {
        for (int m = 0; m < w; m++)
        {
            int tred = image[n][m].rgbtRed;
            int tgreen = image[n][m].rgbtGreen;
            int tblue = image[n][m].rgbtBlue;

            image[n][m].rgbtRed = image[n][width - m - 1].rgbtRed;
            image[n][m].rgbtGreen = image[n][width - m - 1].rgbtGreen;
            image[n][m].rgbtBlue = image[n][width - m - 1].rgbtBlue;

            image[n][width - m - 1].rgbtRed = tred;
            image[n][width - m - 1].rgbtGreen = tgreen;
            image[n][width - m - 1].rgbtBlue = tblue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temporary[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int n = 0; n < width; n++)
        {
            temporary[i][n] = image[i][n];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int n = 0; n < width; n++)
        {
            float allRed = 0;
            float allGreen = 0;
            float allBlue = 0;
            float counter = 0;

            for (int p = -1; p < 2; p++)
            {
                for (int m = -1; m < 2; m++)
                {
                    if (i + p < 0 || i + p > height - 1)
                    {
                        continue;
                    }

                    if (n + m < 0 || n + m > width - 1)
                    {
                        continue;
                    }

                    allRed += image[i + p][n + m].rgbtRed;
                    allBlue += image[i + p][n + m].rgbtBlue;
                    allGreen += image[i + p][n + m].rgbtGreen;
                    counter++;
                }
            }

            temporary[i][n].rgbtBlue = round(allBlue / counter);
            temporary[i][n].rgbtGreen = round(allGreen / counter);
            temporary[i][n].rgbtRed = round(allRed / counter);
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int n = 0; n < width; n++)
        {
            image[i][n].rgbtBlue = temporary[i][n].rgbtBlue;
            image[i][n].rgbtGreen = temporary[i][n].rgbtGreen;
            image[i][n].rgbtRed = temporary[i][n].rgbtRed;
        }
    }

    return;
}

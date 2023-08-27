#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int n = 0; n < height; n+=)
    {
        for (int m = 0; m < width; m++)
        {
            float red = image[n][m].rgbtRed;
            float green = image[n][m].rgbtGreen;
            float blue = image[n][m].rgbtBlue;

            int grey = ((red + green + blue) / 3);

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
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

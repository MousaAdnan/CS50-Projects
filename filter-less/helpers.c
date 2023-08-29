#include "helpers.h"

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
    for (int n = 0; n < height; n++)
    {
        for (int m = 0; m < width; m++)
        {
            float red = .393 * image[n][m].rgbtRed + .769 * image[n][m].rgbtGreen + .189 * image[n][m].rgbtBlue;
            float green = .349 * image[n][m].rgbtRed + .686 * image[n][m].rgbtGreen + .168 * image[n][m].rgbtBlue;
            float blue = .272 * image[n][m].rgbtRed + .534 * image[n][m].rgbtGreen + .131 * image[n][m].rgbtBlue;

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
    
    return;
}

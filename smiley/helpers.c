#include "helpers.h"

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    for (int w = 0; w < width; w++)
    {
        for (int h = 0; h < height; h++)
        {
            if (image[width][height].rgbtBlue == 0 && image[width][height].rgbtRed == 0 && image[width][height].rgbtGreen == 0)
            {
                image[width][height].rgbtRed = 0;
                image[width][height].rgbtGreen = 255;
                image[width][height].rgbtBlue = 0;
            }
        }
    }

}

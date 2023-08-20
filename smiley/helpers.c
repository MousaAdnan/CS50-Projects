#include "helpers.h"

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    for (int w = 0; w < width; w++)
    {
        for (int h = 0; h < height; h++)
        {
            if (image[w][h].rgbtBlue == 0 && image[w][h].rgbtRed == 0 && image[w][h].rgbtGreen == 0)
            {
                image[w][h].rgbtRed = 0;
                image[w][h].rgbtGreen = 255;
                image[w][h].rgbtBlue = 0;
            }
        }
    }

}

#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Average the RGB values for each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int avg = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = avg;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Reverse the pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Make a copy of the array
    RGBTRIPLE neo_image[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            neo_image[i][j] = image[i][j];
        }
    }

    // The actual blurring
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Initilize all variables for each pixel
            float red = 0.0, green = 0.0, blue = 0.0;
            int count = 0;

            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    // See if pixel exists, if it does then add the RGB values to respectize variables
                    if (((i + k < height && i + k >= 0) && ((j + l >= 0) && (j + l < width))))
                    {
                        red += neo_image[i + k][j + l].rgbtRed;
                        green += neo_image[i + k][j + l].rgbtGreen;
                        blue += neo_image[i + k][j + l].rgbtBlue;
                        count++;
                    }
                    // If pixel does not exist
                    else
                    {
                        continue;
                    }
                }
            }

            // Average the RBG values and assign it to the pixel
            image[i][j].rgbtRed = round(red / (float) count);
            image[i][j].rgbtGreen = round(green / (float) count);
            image[i][j].rgbtBlue = round(blue / (float) count);
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Making copy of array
    RGBTRIPLE neo_image[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            neo_image[i][j] = image[i][j];
        }
    }

    // Edge detection
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int gx[3][3] = { {-1, 0, 1}, {-2, 0, 2}, {-1, 0 , 1} };
            int gy[3][3] = { {-1, -2, -1}, {0, 0, 0}, {1, 2, 1} };

            float gxred = 0.0, gxgreen = 0.0, gxblue = 0.0;
            float gyred = 0.0, gygreen = 0.0, gyblue = 0.0;

            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    if (((i + k < height && i + k >= 0) && ((j + l >= 0) && (j + l < width))))
                    {
                        gxred += neo_image[i + k][j + l].rgbtRed * gx[k + 1][l + 1];
                        gxgreen += neo_image[i + k][j + l].rgbtGreen * gx[k + 1][l + 1];
                        gxblue += neo_image[i + k][j + l].rgbtBlue * gx[k + 1][l + 1];

                        gyred += neo_image[i + k][j + l].rgbtRed * gy[k + 1][l + 1];
                        gygreen += neo_image[i + k][j + l].rgbtGreen * gy[k + 1][l + 1];
                        gyblue += neo_image[i + k][j + l].rgbtBlue * gy[k + 1][l + 1];
                    }
                }
            }
            int red = round(sqrt((gxred * gxred) + (gyred * gyred)));
            int green = round(sqrt((gxgreen * gxgreen) + (gygreen * gygreen)));
            int blue = round(sqrt((gxblue * gxblue) + (gyblue * gyblue)));

            if (red > 255)
            {
                red = 255;
            }
            if (blue > 255)
            {
                blue = 255;
            }
            if (green > 255)
            {
                green = 255;
            }

            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;
        }
    }

    return;
}

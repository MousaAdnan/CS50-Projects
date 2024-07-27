// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    unsigned char header[HEADER_SIZE];
    if (fread(header, sizeof(unsigned char), HEADER_SIZE, input) != HEADER_SIZE)
    {
        printf("Error reading header from input file.\n");
        fclose(input);
        fclose(output);
        return 1;
    }
    fwrite(header, sizeof(unsigned char), HEADER_SIZE, output);

    // TODO: Read samples from input file and write updated data to output file

    sample_t sample;
    while(fread(&sample, sizeof(sample_t), 1, input) == 1)
    {
        sample = (sample_t) (sample * factor);

        if (sample > INT16_MAX)
        {
            sample = INT16_MAX;
        }
        else if (sample < INT16_MIN)
        {
            sample = INT16_MIN;
        }

        fwrite(&sample, sizeof(sample_t), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);

    return 0;
}

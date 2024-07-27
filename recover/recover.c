#include <stdio.h>
#include <stdlib.h>
#include 

#define BLOCK_SIZE 512
#define JPEG_SIGNATURE_1 0xff
#define JPEG_SIGNATURE_2 0xd8
#define JPEG_SIGNATURE_3 0xff
#define JPEG_SIGNATURE_4_START 0xe0
#define JPEG_SIGNATURE_4_END 0xef

typedef uint8_t byte_t;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover card.raw\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open file.\n");
        return 1;
    }

    byte_t buffer[BLOCK_SIZE];
    FILE img = NULL;
    int img_count = 0;
    bool in_jpeg = false;
    char filename[8];

    while (fread(buffer, sizeof(byte_t), BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        if (buffer[0] == JPEG_SIGNATURE_1 && buffer[1] == JPEG_SIGNATURE_2 && buffer[2] == JPEG_SIGNATURE_3 && (buffer[3] >= JPEG_SIGNATURE_4_Start && buffer[3] <= JPEG_SIGNATURE_4_END))
        {
            if (in_jpeg)
            {
                fclose(img);
            }
            else
            {
                in_jpeg = true;
            }


            sprintf(filename, "%03i.jpg", img_count++);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                fprintf(stderr, "Could not create image file.\n");
                fclose(file);
                return 1;
            }
        }

        if(in_jpeg)
        {
            fwrite(buffer, sizeof(byte_t), BLOCK_SIZE, img);
        }
    }

    if (in_jpeg)
    {
        fclose(img);
    }

    fclose(file);
    return 0;
}

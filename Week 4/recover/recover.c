#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover [image to recover]\n");
        return 1;
    }
    char *name = argv[1];
    FILE *raw_file = fopen(name, "r");

    if (raw_file == NULL)
    {
        printf("File could not be opened!\n");
        return 1;
    }

    BYTE buffer[512];
    FILE *jpg = NULL;
    char filename[9];
    int count = 0;

    while (fread(&buffer, sizeof(BYTE) * 512, 1, raw_file) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && ((buffer[3] &0xf0) == 0xe0))
        {
            if (jpg != NULL)
            {
                fclose(jpg);
            }
            sprintf(filename, "%03i.jpg", count);
            jpg = fopen(filename, "w");
            count++;
        }

        if (jpg != NULL)
        {
            fwrite(buffer, sizeof(BYTE) * 512, 1, jpg);
        }

    }
    
    if (jpg != NULL)
    {
        fclose(jpg);
    }

    fclose(raw_file);
}

#include <stdio.h>
#include <stdlib.h>

#include "typedef.h"
#include "BASIC_OP.H"

#define TEST_LENGTH ((int)MAX_16 - (int)MIN_16 + 1)

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        printf("Usage : exe [r -OR- w] filename\n");
        printf("\n");
        exit(1);
    }

    FILE *f_file; /* File of 16-bit data */
    char *execCmd = argv[0];
    char *cmd = argv[1];
    char *filename = argv[2];

    if (cmd[0] == 'w')
    {
        if ((f_file = fopen(filename, "wb")) == NULL)
        {
            printf("%s - Error opening file  %s !!\n", execCmd, filename);
            exit(0);
        }
        printf(" Output file:  %s\n", filename);

        Word16 word16Numbers[TEST_LENGTH];
        Word16 counter = MIN_16;
        int index = 0;
        while (counter < MAX_16)
        {
            word16Numbers[index] = counter;
            index++;
            counter++;
        }
        word16Numbers[TEST_LENGTH-1] = MAX_16;

        fwrite(word16Numbers, sizeof(Word16), TEST_LENGTH, f_file);
    }
    else
    {
        if ((f_file = fopen(filename, "rb")) == NULL)
        {
            printf("%s - Error opening file  %s !!\n", execCmd, filename);
            exit(0);
        }
        printf(" Input file:  %s\n", filename);

        Word16 values[TEST_LENGTH];
        fread(values, sizeof(Word16), TEST_LENGTH, f_file);
        
        printf("value: %d\n", values[0]);
        for (int i = 0; i < TEST_LENGTH; i++) {
            if (i % 1000 == 0) {
                printf("value: %d\n", values[i]);
            }
        }
        printf("value: %d\n", values[TEST_LENGTH-1]);
        
    }

    return 0;
}

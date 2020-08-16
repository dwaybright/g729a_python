#include <stdio.h>
#include <stdlib.h>

#include "typedef.h"
#include "basic_op.h"

int main(int argc, char *argv[] )
{
    printf("I compiled!");
    printf("\n");

    Word16 var1 = 15;
    Word16 var2 = 10;

    Word16 result = add(var1, var2);

    printf("%d + %d = %d", var1, var2, result);    
}

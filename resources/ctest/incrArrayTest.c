#include <stdio.h>
#include <stdlib.h>

void SomeMethod(int test[]) {
    printf("method: test[0] = %d\n", test[0]);

    test += 2;

    printf("method: test[0] = %d\n", test[0]);
}

int main(int argc, char *argv[])
{
    int i;
    int test[10];

    for(i=0; i<10; i++) {
        test[i] = i;
    }

    printf("main: test[0] = %d\n", test[0]);

    SomeMethod(test);

    printf("main: test[0] = %d\n", test[0]);

    return 0;
}

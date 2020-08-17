#include <stdio.h>
#include <stdlib.h>

#include "typedef.h"
#include "basic_op.h"
#include "oper_32b.h"

#define LENGTH_WORD16_TEST_NUMBERS 13
Word16 stdWord16_TestNumbers[LENGTH_WORD16_TEST_NUMBERS] = {
    MIN_16 - (Word16)1,
    MIN_16,
    MIN_16 + (Word16)1,
    (MIN_16 / 2) - (Word16) 123,
    (MIN_16 / 2) + (Word16) 123,
    (Word16)-1,
    (Word16)0,
    (Word16)1,
    (MAX_16 / 2) - (Word16) 123,
    (MAX_16 / 2) + (Word16) 123,
    MAX_16 - (Word16)1,
    MAX_16,
    MAX_16 + (Word16)1,
};

#define LENGTH_WORD32_TEST_NUMBERS 23
Word32 stdWord32_TestNumbers[LENGTH_WORD32_TEST_NUMBERS] = {
    MIN_32 - (Word32)1,
    MIN_32,
    MIN_32 + (Word32)1,
    (MIN_32 / 2) - (Word32) 123,
    (MIN_32 / 2) + (Word32) 123,
    ((Word32)MIN_16) - (Word32)1,
    (Word32)MIN_16,
    ((Word32)MIN_16) + (Word32)1,
    ((Word32)(MIN_16 / 2)) - (Word32) 123,
    ((Word32)(MIN_16 / 2)) + (Word32) 123,
    (Word16)-1,
    (Word16)0,
    (Word16)1,
    ((Word32)(MAX_16 / 2)) - (Word32) 123,
    ((Word32)(MAX_16 / 2)) + (Word32) 123,
    ((Word32)MAX_16) - (Word32)1,
    (Word32)MAX_16,
    ((Word32)MAX_16) + (Word32)1,
    (MAX_32 / 2) - (Word32) 123,
    (MAX_32 / 2) + (Word32) 123,
    MAX_32 - (Word32)1,
    MAX_32,
    MAX_32 + (Word32)1
};

int main(int argc, char *argv[] )
{
    // Need to append path to python src
    printf("import sys");
    printf("\n");
    printf("sys.path.append(\"../../../src\")");
    printf("\n");

    //printf("from basic_op import *");
    printf("from oper_32b import *");
    printf("\n");
    printf("\n");

    // constants
    testConstants();

    // test methods
    test_Div_32();
    test_L_Comp();
    test_L_Extract();
    test_Mpy_32_16();
    test_Mpy_32();

    return 0;
}

void testConstants() {
    printf("print(\"Testing constants\")\n");

    // Others
    printf("print(f\"0x7fff = %d\")\n", (Word16)0x7fff);
    printf("print(f\"0x3fff = %d\")\n", (Word16)0x3fff);
    printf("print(f\"0x4000 = %d\")\n", (Word16)0x4000);
    printf("print(f\"0x7fffffffL = %d\")\n", (Word32)0x7fffffffL);
    
    printLineBreak(); 
}

void printLineBreak() {
    printf("print(\"\\n\")");
    printf("\n");
}

void test_Div_32() {
    printf("print(\"Testing Div_32\")\n");

    /*___________________________________________________________________________
    |                                                                           |
    |   Function Name : Div_32                                                  |
    |                                                                           |
    |   Purpose :                                                               |
    |             Fractional integer division of two 32 bit numbers.            |
    |             L_num / L_denom.                                              |
    |             L_num and L_denom must be positive and L_num < L_denom.       |
    |             L_denom = denom_hi<<16 + denom_lo<<1                          |
    |             denom_hi is a normalize number.                               |
    |             The result is in Q30.                                         |
    |                                                                           |
    |   Inputs :                                                                |
    |                                                                           |
    |   L_num                                                                  |
    |             32 bit long signed integer (Word32) whose value falls in the  |
    |             range : 0x0000 0000 < L_num < L_denom                         |
    |                                                                           |
    |   L_denom = denom_hi<<16 + denom_lo<<1      (DPF)                        |
    |                                                                           |
    |       denom_hi                                                            |
    |             16 bit positive normalized integer whose value falls in the   |
    |             range : 0x4000 < hi < 0x7fff                                  |
    |       denom_lo                                                            |
    |             16 bit positive integer whose value falls in the              |
    |             range : 0 < lo < 0x7fff                                       |
    |                                                                           |
    |   Return Value :                                                          |
    |                                                                           |
    |   L_div                                                                  |
    |             32 bit long signed integer (Word32) whose value falls in the  |
    |             range : 0x0000 0000 <= L_div <= 0x7fff ffff.                  |
    |             It's a Q31 value                                              |
    |                                                                           |
    |  Algorithm:                                                               |
    |                                                                           |
    |  - find = 1/L_denom.                                                      |
    |      First approximation: approx = 1 / denom_hi                           |
    |      1/L_denom = approx * (2.0 - L_denom * approx )                       |
    |                                                                           |
    |  -  result = L_num * (1/L_denom)                                          |
    |___________________________________________________________________________|
    */

    Word32 L_num;
    Word16 denom_hi, denom_lo;

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        L_num = stdWord32_TestNumbers[i];

        if (L_num > 0) {
            for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {

                denom_hi = stdWord16_TestNumbers[j];

                if(denom_hi > 16384 && denom_hi < 32767) {
                    for (int k=0; k<LENGTH_WORD16_TEST_NUMBERS; k++) {
                        denom_lo = stdWord16_TestNumbers[k];

                        if (denom_lo > 0 && denom_lo < 32767) {
                            test_Div_32_Helper(
                                L_num,
                                denom_hi,
                                denom_lo
                            );
                        }
                    }
                }
            }
        }
    }

    printLineBreak();
}

void test_Div_32_Helper(Word32 L_num, Word16 denom_hi, Word16 denom_lo) {
    Word32 L_result = Div_32(L_num, denom_hi, denom_lo);

    printf("pyResult = %s(%d, %d, %d)\n", "Div_32", L_num, denom_hi, denom_lo);
    printf("if pyResult != %d:\n", L_result);
    printf("\tprint(f\"{pyResult == %d} - %s(%d, %d, %d) => C = %d, Python = {pyResult}\")\n", L_result, "Div_32", L_num, denom_hi, denom_lo, L_result);
}


void test_L_Comp() {
    printf("print(\"Testing L_Comp\")\n");
    
    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            test_L_Comp_Helper(
                stdWord16_TestNumbers[i],
                stdWord16_TestNumbers[j]
            );
        }
    }
}

void test_L_Comp_Helper(Word16 hi, Word16 lo) {
    Word32 L_result = L_Comp(hi, lo);

    printf("pyResult = %s(%d, %d)\n", "L_Comp", hi, lo);
    printf("if pyResult != %d:\n", L_result);
    printf("\tprint(f\"{pyResult == %d} - %s(%d, %d) => C = %d, Python = {pyResult}\")\n", L_result, "L_Comp", hi, lo, L_result);
}


void test_L_Extract() {
    printf("print(\"Testing L_Extract\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        test_L_Extract_Helper(
            stdWord32_TestNumbers[i]
        );
    }

    printLineBreak();
}

void test_L_Extract_Helper(Word32 L_32) {
    Word32 hi, lo;
    L_Extract(L_32, &hi, &lo);

    printf("pyResultHi, pyResultLo = %s(%d)\n", "L_Extract", L_32);
    printf("if pyResultHi != %d and pyResultLo != %d:\n", hi, lo);
    printf("\tprint(f\"{pyResultHi == %d} - %s(%d) => C = %d, Python = {pyResultHi}\")\n", hi, "L_Extract", hi, hi);
    printf("\tprint(f\"{pyResultLo == %d} - %s(%d) => C = %d, Python = {pyResultLo}\")\n", lo, "L_Extract", lo, lo);
}

void test_Mpy_32_16() {
    printf("print(\"Testing Mpy_32_16\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            for (int k=0; k<LENGTH_WORD16_TEST_NUMBERS; k++) {
                test_Mpy_32_16_Helper(
                    stdWord16_TestNumbers[i],
                    stdWord16_TestNumbers[j],
                    stdWord16_TestNumbers[k]
                );
            }
        }
    }

    printLineBreak();
}

void test_Mpy_32_16_Helper(Word16 hi, Word16 lo, Word16 n) {
    Word32 L_result = Mpy_32_16(hi, lo, n);

    printf("pyResult = %s(%d, %d, %d)\n", "Mpy_32_16", hi, lo, n);
    printf("if pyResult != %d:\n", L_result);
    printf("\tprint(f\"{pyResult == %d} - %s(%d, %d, %d) => C = %d, Python = {pyResult}\")\n", L_result, "Mpy_32_16", hi, lo, n, L_result);
}

void test_Mpy_32() {
    printf("print(\"Testing Mpy_32\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j=j+2) {
            for (int k=0; k<LENGTH_WORD16_TEST_NUMBERS; k=k+2) {
                for (int l=0; l<LENGTH_WORD16_TEST_NUMBERS; l++) {
                    test_Mpy_32_Helper(
                        stdWord16_TestNumbers[i],
                        stdWord16_TestNumbers[j],
                        stdWord16_TestNumbers[k],
                        stdWord16_TestNumbers[l]
                    );
                }
            }
        }
    }

    printLineBreak();
}

void test_Mpy_32_Helper(Word16 hi1, Word16 lo1, Word16 hi2, Word16 lo2) {
    Word32 L_result = Mpy_32(hi1, lo1, hi2, lo2);

    printf("pyResult = %s(%d, %d, %d, %d)\n", "Mpy_32", hi1, lo1, hi2, lo2);
    printf("if pyResult != %d:\n", L_result);
    printf("\tprint(f\"{pyResult == %d} - %s(%d, %d, %d, %d) => C = %d, Python = {pyResult}\")\n", L_result, "Mpy_32", hi1, lo1, hi2, lo2, L_result);
}

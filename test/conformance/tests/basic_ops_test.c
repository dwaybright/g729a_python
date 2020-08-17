#include <stdio.h>
#include <stdlib.h>

#include "typedef.h"
#include "basic_op.h"

Word16 MAX_14 = (Word16) 0x00004000;
Word32 MAX_30 = (Word32) 0x3fffffffL;
Word32 MIN_30 = (Word32) 0xc0000000L;

extern Flag Overflow;
extern Flag Carry;

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
    printf("sys.path.append(\"../../../../src\")");
    printf("\n");

    printf("from basic_op import *");
    printf("\n");
    printf("\n");

    // Check constants
    testConstants();

    // Check methods ('failing' and 'passing with C alterations' are marked)
    // test_abs_s();
    // test_add();
    // test_div_s();
    // test_extract_h();
    // test_extract_l();
    // test_L_abs();
    // test_L_add_c();
    // test_L_add();
    // test_L_deposit_h();
    // test_L_deposit_l();
    // test_L_mac();
    // test_L_macNs();
    // test_L_msu();            // failing
    // test_L_msuNs();          // failing
    // test_L_mult();
    // test_L_negate();
    // test_L_sat();
    // test_L_shl();            // passing (with basic_op.c change for var2=MIN_32)
    // test_L_shr_r();
    // test_L_shr();            // passing (with basic_op.c change for var2=MIN_32)
    // test_L_sub_c();          // failing
    // test_L_sub();
    // test_mac_r();
    // test_msu_r();
    // test_mult_r();
    // test_mult();
    // test_negate();
    // test_norm_l();
    // test_norm_s();
    // test_round();
    // test_sature();
    // test_shl();              // passing (with basic_op.c change for var2=MIN_32)
    // test_shr();              // passing (with basic_op.c change for var2=MIN_32)
    // test_shr_r();
    // test_sub();

    return 0;
}

void clearFlags() {
    setFlags(0,0);
}

void setFlags(Flag overflow, Flag carry) {
    // Clear Python flags
    printf("\n");
    printf("setOverflow(%d)\n", overflow);
    printf("setCarry(%d)\n", carry);

    // Set C flags
    Overflow = overflow;
    Carry = carry;
}

void printLineBreak() {
    printf("print(\"\\n\")");
    printf("\n");
}


void testConstants() {
    printf("print(\"Testing constants\")\n");

    // Maxes
    printf("print(f\"{MAX_INT_14 == %d} - MAX_INT_14 matches %d\")\n", MAX_14, MAX_14);
    printf("print(f\"{MAX_INT_16 == %d} - MAX_INT_16 matches %d\")\n", MAX_16, MAX_16);
    printf("print(f\"{MAX_INT_30 == %d} - MAX_INT_30 matches %d\")\n", MAX_30, MAX_30);
    printf("print(f\"{MAX_INT_32 == %d} - MAX_INT_32 matches %d\")\n", MAX_32, MAX_32);
    printf("\n"); 

    // Mins
    printf("print(f\"{MIN_INT_16 == %d} - MIN_INT_16 matches %d\")\n", MIN_16, MIN_16);
    printf("print(f\"{MIN_INT_30 == %d} - MIN_INT_30 matches %d\")\n", MIN_30, MIN_30);
    printf("print(f\"{MIN_INT_32 == %d} - MIN_INT_32 matches %d\")\n", MIN_32, MIN_32);

    // Others
    printf("print(f\"0x00008000L = %d\")\n", (Word32)0x00008000L);
    printf("print(f\"0x00010000L = %d\")\n", (Word32)0x00010000L);
    printf("print(f\"0xffff8000L = %d\")\n", (Word32)0xffff8000L);
    printf("print(f\"0xffff0000L = %d\")\n", (Word32)0xffff0000L);
    printf("print(f\"0x40000000L = %d\")\n", (Word32)0x40000000L);
    printf("print(f\"0X00000001L = %d\")\n", (Word32)0X00000001L);
    printf("print(f\"0xffffffffL = %d\")\n", (Word32)0xffffffffL);
    
    printLineBreak(); 
}

void py_V1W16_ResultW16(char* method, Word16 var1, Word16 result) {
    printf("pyResult = %s(%d)\n", method, var1);
    printf("if pyResult != %d:\n", result);
    printf("\tprint(f\"{pyResult == %d} - %s(%d) => C = %d, Python = {pyResult}\")\n", result, method, var1, result);
}

void py_V1W16_ResultW32(char* method, Word16 L_var1, Word32 result) {
    printf("pyResult = %s(%d)\n", method, L_var1);
    printf("if pyResult != %d:\n", result);
    printf("\tprint(f\"{pyResult == %d} - %s(%d) => C = %d, Python = {pyResult}\")\n", result, method, L_var1, result);
}

void py_V1W16_V2W16_ResultW16(char* method, Word16 var1, Word16 var2, Word16 result) {
    printf("pyResult = %s(%d,%d)\n", method, var1, var2);
    printf("if pyResult != %d:\n", result);
    printf("\tprint(f\"{pyResult == %d} - %s(%d,%d) => C = %d, Python = {pyResult}\")\n", result, method, var1, var2, result);
}

void py_V1W16_V2W16_ResultW32(char* method, Word16 var1, Word16 var2, Word32 L_result) {
    printf("pyResult = %s(%d,%d)\n", method, var1, var2);
    printf("if pyResult != %d:\n", L_result);
    printf("\tprint(f\"{pyResult == %d} - %s(%d,%d) => C = %d, Python = {pyResult}\")\n", L_result, method, var1, var2, L_result);
}

void py_V1W32_ResultW32(char* method, Word32 L_var1, Word32 L_result) {
    printf("pyResult = %s(%d)\n", method, L_var1);
    printf("if pyResult != %d:\n", L_result);
    printf("\tprint(f\"{pyResult == %d} - %s(%d) => C = %d, Python = {pyResult}\")\n", L_result, method, L_var1, L_result);
}

void py_V1W32_ResultW32_Flags(char* method, char* message, Word32 L_var1, Word32 result) {
    printf("pyResult = %s(%d)\n", method, L_var1);
    printf("if pyResult != %d:\n", result);
    printf("\t%s\n", message);
    printf("\tprint(f\"{pyResult == %d} - %s(%d) => C = %d, Python = {pyResult}\")\n", result, method, L_var1, result);
    printf("\tprint(f\"\t{getOverflow() == %d} - Overflow => C = %d, Python = {getOverflow()}\")\n", Overflow, Overflow);
    printf("\tprint(f\"\t{getCarry() == %d} - Carry => C = %d, Python = {getCarry()}\")\n", Carry, Carry);
}

void py_V1W32_ResultW16(char* method, Word32 L_var1, Word16 result) {
    printf("pyResult = %s(%d)\n", method, L_var1);
    printf("if pyResult != %d:\n", result);
    printf("\tprint(f\"{pyResult == %d} - %s(%d) => C = %d, Python = {pyResult}\")\n", result, method, L_var1, result);
}

void py_V1W32_ResultW16_Flags(char* method, char* message, Word32 L_var1, Word16 result) {
    printf("pyResult = %s(%d)\n", method, L_var1);
    printf("if pyResult != %d:\n", result);
    printf("\t%s\n", message);
    printf("\tprint(f\"{pyResult == %d} - %s(%d) => C = %d, Python = {pyResult}\")\n", result, method, L_var1, result);
    printf("\tprint(f\"\t{getOverflow() == %d} - Overflow => C = %d, Python = {getOverflow()}\")\n", Overflow, Overflow);
    printf("\tprint(f\"\t{getCarry() == %d} - Carry => C = %d, Python = {getCarry()}\")\n", Carry, Carry);
}

void py_V1W32_V2W32_ResultW32(char* method, Word32 L_var1, Word32 L_var2, Word32 L_result) {
    printf("pyResult = %s(%d,%d)\n", method, L_var1, L_var2);
    printf("if pyResult != %d:\n", L_result);
    printf("\tprint(f\"{pyResult == %d} - %s(%d,%d) => C = %d, Python = {pyResult}\")\n", L_result, method, L_var1, L_var2, L_result);
}

void py_V1W32_V2W32_ResultW32_Flags(char* method, char* message, Word32 L_var1, Word32 L_var2, Word32 L_result) {
    printf("pyResult = %s(%d,%d)\n", method, L_var1, L_var2);
    printf("if pyResult != %d or getOverflow() != %d or getCarry() != %d:\n", L_result, Overflow, Carry);
    printf("\t%s\n", message);
    printf("\tprint(f\"\t{pyResult == %d} - %s(%d,%d) = %d, found {pyResult}\")\n", L_result, method, L_var1, L_var2, L_result);
    printf("\tprint(f\"\t{getOverflow() == %d} - Overflow => C = %d, Python = {getOverflow()}\")\n", Overflow, Overflow);
    printf("\tprint(f\"\t{getCarry() == %d} - Carry => C = %d, Python = {getCarry()}\")\n", Carry, Carry);
}

void py_V1W32_V2W16_ResultW32(char* method, Word32 L_var1, Word16 var2, Word32 L_result) {
    printf("pyResult = %s(%d, %d)\n", method, L_var1, var2);
    printf("if pyResult != %d:\n", L_result);
    printf("\tprint(f\"{pyResult == %d} - %s(%d,%d) => C = %d, Python = {pyResult}\")\n", L_result, method, L_var1, var2, L_result);
}

void py_V3W32_V1W16_V2W16_ResultW32(char* method, Word32 L_var3, Word16 var1, Word16 var2, Word32 L_result) {
    printf("pyResult = %s(%d, %d, %d)\n", method, L_var3, var1, var2);
    printf("if pyResult != %d:\n", L_result);
    printf("\tprint(f\"{pyResult == %d} - %s(%d, %d, %d) => C = %d, Python = {pyResult}\")\n", L_result, method, L_var3, var1, var2, L_result);
}

void py_V3W32_V1W16_V2W16_ResultW32_Flags(char* method, char* message, Word32 L_var3, Word16 var1, Word16 var2, Word32 L_result) {
    printf("pyResult = %s(%d, %d, %d)\n", method, L_var3, var1, var2);
    printf("if pyResult != %d or getOverflow() != %d or getCarry() != %d:\n", L_result, Overflow, Carry);
    printf("\t%s\n", message);
    printf("\tprint(f\"{pyResult == %d} - %s(%d, %d, %d) => C = %d, Python = {pyResult}\")\n", L_result, method, L_var3, var1, var2, L_result);
    printf("\tprint(f\"\t{getOverflow() == %d} - Overflow => C = %d, Python = {getOverflow()}\")\n", Overflow, Overflow);
    printf("\tprint(f\"\t{getCarry() == %d} - Carry => C = %d, Python = {getCarry()}\")\n", Carry, Carry);
}


void test_abs_s() {
    printf("print(\"Testing abs_s\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        test_abs_s_Helper(stdWord16_TestNumbers[i]);
    }

    printLineBreak(); 
}

void test_abs_s_Helper(Word16 var) {
    Word16 result = abs_s(var);

    py_V1W16_ResultW16("abs_s", var, result);
}

void test_add() {
    printf("print(\"Testing add\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            test_add_Helper(
                stdWord16_TestNumbers[i], 
                stdWord16_TestNumbers[j]
            );
        }
    }

    printLineBreak(); 
}

void test_add_Helper(Word16 var1, Word16 var2) {
    Word16 result = add(var1, var2);

    py_V1W16_V2W16_ResultW16("add", var1, var2, result);
}

void test_div_s() {
    printf("print(\"Testing div_s\")\n");

    test_div_s_Helper((Word16)0, (Word16)245);
    test_div_s_Helper((Word16)357, (Word16)357);
    test_div_s_Helper((Word16)1325, MAX_16);

    printLineBreak(); 
}

void test_div_s_Helper(Word16 var1, Word16 var2) {
    Word16 result = div_s(var1, var2);

    py_V1W16_V2W16_ResultW16("div_s", var1, var2, result);
}

void test_extract_h() {
    printf("print(\"Testing extract_h\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        test_extract_h_Helper(stdWord32_TestNumbers[i]);
    }

    printLineBreak(); 
}

void test_extract_h_Helper(Word32 var) {
    Word16 result = extract_h(var);

    py_V1W32_ResultW16("extract_h", var, result);
}

void test_extract_l() {
    printf("print(\"Testing extract_l\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        test_extract_l_Helper(stdWord32_TestNumbers[i]);
    }

    printLineBreak(); 
}

void test_extract_l_Helper(Word32 var) {
    Word16 result = extract_l(var);

    py_V1W32_ResultW16("extract_l", var, result);
}

void test_L_abs() {
    printf("print(\"Testing L_abs\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        test_L_abs_Helper(stdWord32_TestNumbers[i]);
    }

    printLineBreak(); 
}

void test_L_abs_Helper(Word32 var) {
    Word32 result = L_abs(var);

    py_V1W32_ResultW32("L_abs", var, result);
}

void test_L_add_c() {
    printf("print(\"Testing L_add_c\")\n");

    // Test
    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD32_TEST_NUMBERS; j++) {
            test_L_add_c_Helper(
                stdWord32_TestNumbers[i], 
                stdWord32_TestNumbers[j]
            );
        }
    }

    // Clear flags    
    clearFlags();

    printLineBreak(); 
}

void test_L_add_c_Helper(Word32 L_var1, Word32 L_var2) {
    // Run all 4 variations
    test_L_add_c_Helper_No_Flag(L_var1, L_var2);
    test_L_add_c_Helper_with_Overflow(L_var1, L_var2);
    test_L_add_c_Helper_with_Carry(L_var1, L_var2);
    test_L_add_c_Helper_with_OverflowAndCarry(L_var1, L_var2);
}

void test_L_add_c_Helper_No_Flag(Word32 L_var1, Word32 L_var2) {
    setFlags(0,0);

    // Run test
    test_L_add_c_Helper_Worker("__", L_var1, L_var2);
}

void test_L_add_c_Helper_with_Overflow(Word32 L_var1, Word32 L_var2) {
    setFlags(1,0);

    // Run test
    test_L_add_c_Helper_Worker("O_", L_var1, L_var2);
}

void test_L_add_c_Helper_with_Carry(Word32 L_var1, Word32 L_var2) {
    setFlags(0,1);

    // Run test
    test_L_add_c_Helper_Worker("_C", L_var1, L_var2);
}

void test_L_add_c_Helper_with_OverflowAndCarry(Word32 L_var1, Word32 L_var2) {
    setFlags(1,1);

    // Run test
    test_L_add_c_Helper_Worker("OC", L_var1, L_var2);
}

void test_L_add_c_Helper_Worker(char* flags, Word32 L_var1, Word32 L_var2) {
    Word32 result = L_add_c(L_var1, L_var2);

    char message[256];
    sprintf(message, "print(f\"Flags %s: testing var1=%d var2=%d\")\n", flags, L_var1, L_var2);

    // Check Comp
    py_V1W32_V2W32_ResultW32_Flags("L_add_c", message, L_var1, L_var2, result);
}

void test_L_add() {
    printf("print(\"Testing L_add\")\n");

    // Clear flags    
    clearFlags();

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD32_TEST_NUMBERS; j++) {
            test_L_add_Helper(
                stdWord32_TestNumbers[i], 
                stdWord32_TestNumbers[j]
            );
        }
    }

    printLineBreak();
}

void test_L_add_Helper(Word32 L_var1, Word32 L_var2) {
    Word32 result = L_add(L_var1, L_var2);

    char message[256];
    sprintf(message, "print(\"Checking Overflow flag\")\n");

    // Check Comp
    py_V1W32_V2W32_ResultW32_Flags("L_add", message, L_var1, L_var2, result);

    // Clear flags    
    clearFlags();
}

void test_L_deposit_h() {
    printf("print(\"Testing L_deposit_h\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        test_L_deposit_h_Helper(stdWord16_TestNumbers[i]);
    }

    printLineBreak();
}

void test_L_deposit_h_Helper(Word16 var) {
    Word32 result = L_deposit_h(var);

    py_V1W16_ResultW32("L_deposit_h", var, result);
}

void test_L_deposit_l() {
    printf("print(\"Testing L_deposit_l\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        test_L_deposit_l_Helper(stdWord16_TestNumbers[i]);
    }

    printLineBreak();
}

void test_L_deposit_l_Helper(Word16 var) {
    Word32 result = L_deposit_l(var);

    py_V1W16_ResultW32("L_deposit_l", var, result);
}

void test_L_mac() {
    printf("print(\"Testing L_mac\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            for (int k=0; k<LENGTH_WORD16_TEST_NUMBERS; k++) {
                test_L_mac_Helper(
                    stdWord32_TestNumbers[i],
                    stdWord16_TestNumbers[j],
                    stdWord16_TestNumbers[k]
                );
            }
        }
    }

    printLineBreak();
}

void test_L_mac_Helper(Word32 L_var3, Word16 var1, Word16 var2) {
    Word32 result = L_mac(L_var3, var1, var2);

    py_V3W32_V1W16_V2W16_ResultW32("L_mac", L_var3, var1, var2, result);

    // Clear flags    
    clearFlags();
}

void test_L_macNs() {
    printf("print(\"Testing L_macNs\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            for (int k=0; k<LENGTH_WORD16_TEST_NUMBERS; k++) {
                test_L_macNs_Helper(
                    stdWord32_TestNumbers[i],
                    stdWord16_TestNumbers[j],
                    stdWord16_TestNumbers[k]
                );
            }
        }
    }

    printLineBreak();
}

void test_L_macNs_Helper(Word32 L_var3, Word16 var1, Word16 var2) {
    Word32 result = L_macNs(L_var3, var1, var2);

    char message[256];
    sprintf(message, "print(\"Checking flags\")\n");

    py_V3W32_V1W16_V2W16_ResultW32_Flags("L_macNs", message, L_var3, var1, var2, result);

    // Clear flags    
    clearFlags();
}

void test_L_msu() {
    printf("print(\"Testing L_msu\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            for (int k=0; k<LENGTH_WORD16_TEST_NUMBERS; k++) {
                test_L_msu_Helper(
                    stdWord32_TestNumbers[i],
                    stdWord16_TestNumbers[j],
                    stdWord16_TestNumbers[k]
                );
            }
        }
    }

    printLineBreak();
}

void test_L_msu_Helper(Word32 L_var3, Word16 var1, Word16 var2) {
    Word32 result = L_msu(L_var3, var1, var2);

    char message[256];
    sprintf(message, "print(\"Checking flags\")\n");

    py_V3W32_V1W16_V2W16_ResultW32_Flags("L_msu", message, L_var3, var1, var2, result);

    // Clear flags    
    clearFlags();
}

void test_L_msuNs() {
    printf("print(\"Testing L_msuNs\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            for (int k=0; k<LENGTH_WORD16_TEST_NUMBERS; k++) {
                test_L_msuNs_Helper(
                    stdWord32_TestNumbers[i],
                    stdWord16_TestNumbers[j],
                    stdWord16_TestNumbers[k]
                );
            }
        }
    }

    printLineBreak();
}

void test_L_msuNs_Helper(Word32 L_var3, Word16 var1, Word16 var2) {
    Word32 result = L_msuNs(L_var3, var1, var2);

    char message[256];
    sprintf(message, "print(\"Checking flags\")\n");

    py_V3W32_V1W16_V2W16_ResultW32_Flags("L_msuNs", message, L_var3, var1, var2, result);

    // Clear flags    
    clearFlags();
}

void test_L_mult() {
    printf("print(\"Testing L_mult\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            test_L_mult_Helper(
                stdWord16_TestNumbers[i],
                stdWord16_TestNumbers[j]
            );
        }
    }
}

void test_L_mult_Helper(Word16 var1, Word16 var2) {
    Word32 result = L_mult(var1, var2);

    py_V1W16_V2W16_ResultW32("L_mult", var1, var2, result);

    // Clear flags    
    clearFlags();
}

void test_L_negate() {
    printf("print(\"Testing L_negate\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        test_L_negate_Helper(
            stdWord32_TestNumbers[i]
        );
    }
}

void test_L_negate_Helper(Word32 L_var1) {
    Word32 result = L_negate(L_var1);

    py_V1W32_ResultW32("L_negate", L_var1, result);
}

void test_L_sat() {
    printf("print(\"Testing L_sat\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        test_L_sat_Helper(
            stdWord32_TestNumbers[i]
        );
    }
}

void test_L_sat_Helper(Word32 L_var1) {
    test_L_sat_Helper_No_Flag(L_var1);
    test_L_sat_Helper_with_Overflow(L_var1);
    test_L_sat_Helper_with_Carry(L_var1);
    test_L_sat_Helper_with_OverflowAndCarry(L_var1);
}   

void test_L_sat_Helper_No_Flag(Word32 L_var1) {
    setFlags(0,0);

    // Run test
    test_L_sat_Helper_Worker("__", L_var1);
}

void test_L_sat_Helper_with_Overflow(Word32 L_var1) {
    setFlags(1,0);

    // Run test
    test_L_sat_Helper_Worker("O_", L_var1);
}

void test_L_sat_Helper_with_Carry(Word32 L_var1) {
    setFlags(0,1);

    // Run test
    test_L_sat_Helper_Worker("_C", L_var1);
}

void test_L_sat_Helper_with_OverflowAndCarry(Word32 L_var1) {
    setFlags(1,1);

    // Run test
    test_L_sat_Helper_Worker("OC", L_var1);
}

void test_L_sat_Helper_Worker(char* flags, Word32 L_var1) {
    Word32 result = L_sat(L_var1);

    char message[256];
    sprintf(message, "print(f\"Flags %s: testing var1=%d var2=%d\")\n", flags, L_var1);

    // Check Comp
    py_V1W32_ResultW32_Flags("L_sat", message, L_var1, result);
}

void test_L_shl() {
    printf("print(\"Testing L_shl\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            //if (stdWord16_TestNumbers[j] > 0) {             // L_shr is failing
                test_L_shl_Helper(
                    stdWord32_TestNumbers[i],
                    stdWord16_TestNumbers[j]
                );
            //}
        }
    }
}

void test_L_shl_Helper(Word32 L_var1, Word16 var2) {
    Word32 result = L_shl(L_var1, var2);

    py_V1W32_V2W16_ResultW32("L_shl", L_var1, var2, result);
}

void test_L_shr_r() {
    printf("print(\"Testing L_shr_r\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            test_L_shr_r_Helper(
                stdWord32_TestNumbers[i],
                stdWord16_TestNumbers[j]
            );
        }
    }
}   

void test_L_shr_r_Helper(Word32 L_var1, Word16 var2) {
    Word32 result = L_shr_r(L_var1, var2);

    py_V1W32_V2W16_ResultW32("L_shr_r", L_var1, var2, result);
}


void test_L_shr() {
    printf("print(\"Testing L_shr\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            test_L_shr_Helper(
                stdWord32_TestNumbers[i],
                stdWord16_TestNumbers[j]
            );
        }
    }
}

void test_L_shr_Helper(Word32 L_var1, Word16 var2) {
    Word32 result = L_shr(L_var1, var2);

    py_V1W32_V2W16_ResultW32("L_shr", L_var1, var2, result);
}


void test_L_sub_c() {
    printf("print(\"Testing L_sub_c\")\n");

    // Test
    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD32_TEST_NUMBERS; j++) {
            test_L_sub_c_Helper(
                stdWord32_TestNumbers[i], 
                stdWord32_TestNumbers[j]
            );
        }
    }

    // Clear flags    
    clearFlags();

    printLineBreak(); 
}

void test_L_sub_c_Helper(Word32 L_var1, Word32 L_var2) {
    // Run all 4 variations
    test_L_sub_c_Helper_No_Flag(L_var1, L_var2);
    test_L_sub_c_Helper_with_Overflow(L_var1, L_var2);
    test_L_sub_c_Helper_with_Carry(L_var1, L_var2);
    test_L_sub_c_Helper_with_OverflowAndCarry(L_var1, L_var2);
}

void test_L_sub_c_Helper_No_Flag(Word32 L_var1, Word32 L_var2) {
    setFlags(0,0);

    // Run test
    test_L_sub_c_Helper_Worker("__", L_var1, L_var2);
}

void test_L_sub_c_Helper_with_Overflow(Word32 L_var1, Word32 L_var2) {
    setFlags(1,0);

    // Run test
    test_L_sub_c_Helper_Worker("O_", L_var1, L_var2);
}

void test_L_sub_c_Helper_with_Carry(Word32 L_var1, Word32 L_var2) {
    setFlags(0,1);

    // Run test
    test_L_sub_c_Helper_Worker("_C", L_var1, L_var2);
}

void test_L_sub_c_Helper_with_OverflowAndCarry(Word32 L_var1, Word32 L_var2) {
    setFlags(1,1);

    // Run test
    test_L_sub_c_Helper_Worker("OC", L_var1, L_var2);
}

void test_L_sub_c_Helper_Worker(char* flags, Word32 L_var1, Word32 L_var2) {
    Word32 result = L_sub_c(L_var1, L_var2);

    char message[256];
    sprintf(message, "print(f\"Flags %s: testing var1=%d var2=%d\")\n", flags, L_var1, L_var2);

    // Check Comp
    py_V1W32_V2W32_ResultW32_Flags("L_sub_c", message, L_var1, L_var2, result);
}


void test_L_sub() {
    printf("print(\"Testing L_sub\")\n");

    // Clear flags    
    clearFlags();

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD32_TEST_NUMBERS; j++) {
            test_L_sub_Helper(
                stdWord32_TestNumbers[i], 
                stdWord32_TestNumbers[j]
            );
        }
    }

    printLineBreak();
}

void test_L_sub_Helper(Word32 L_var1, Word32 L_var2) {
    Word32 result = L_sub(L_var1, L_var2);

    char message[256];
    sprintf(message, "print(\"Checking Overflow flag\")\n");

    // Check Comp
    py_V1W32_V2W32_ResultW32_Flags("L_sub", message, L_var1, L_var2, result);

    // Clear flags    
    clearFlags();
}

void test_mac_r() {
    printf("print(\"Testing _mac_r\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            for (int k=0; k<LENGTH_WORD16_TEST_NUMBERS; k++) {
                test_mac_r_Helper(
                    stdWord32_TestNumbers[i],
                    stdWord16_TestNumbers[j],
                    stdWord16_TestNumbers[k]
                );
            }
        }
    }
}

void test_mac_r_Helper(Word32 L_var3, Word16 var1, Word16 var2) {
    Word16 result = mac_r(L_var3, var1, var2);

    py_V3W32_V1W16_V2W16_ResultW32("mac_r", L_var3, var1, var2, result);
}

void test_msu_r() {
    printf("print(\"Testing msu_r\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            for (int k=0; k<LENGTH_WORD16_TEST_NUMBERS; k++) {
                test_msu_r_Helper(
                    stdWord32_TestNumbers[i],
                    stdWord16_TestNumbers[j],
                    stdWord16_TestNumbers[k]
                );
            }
        }
    }
}

void test_msu_r_Helper(Word32 L_var3, Word16 var1, Word16 var2) {
    Word16 result = msu_r(L_var3, var1, var2);

    py_V3W32_V1W16_V2W16_ResultW32("msu_r", L_var3, var1, var2, result);
}

void test_mult_r() {
    printf("print(\"Testing mult_r\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            test_mult_r_Helper(
                stdWord16_TestNumbers[i],
                stdWord16_TestNumbers[j]
            );
        }
    }
}

void test_mult_r_Helper(Word16 var1, Word16 var2) {
    Word16 result = mult_r(var1, var2);

    py_V1W16_V2W16_ResultW16("mult_r", var1, var2, result);

    // Clear flags    
    clearFlags();
}

void test_mult() {
    printf("print(\"Testing mult\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            test_mult_Helper(
                stdWord16_TestNumbers[i],
                stdWord16_TestNumbers[j]
            );
        }
    }
}

void test_mult_Helper(Word16 var1, Word16 var2) {
    Word16 result = mult(var1, var2);

    py_V1W16_V2W16_ResultW16("mult", var1, var2, result);

    // Clear flags    
    clearFlags();
}

void test_negate() {
    printf("print(\"Testing negate\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        test_negate_Helper(stdWord16_TestNumbers[i]);
    }

    printLineBreak(); 
}

void test_negate_Helper(Word16 var) {
    Word16 result = negate(var);

    py_V1W16_ResultW16("negate", var, result);
}

void test_norm_l() {
    printf("print(\"Testing norm_l\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        test_norm_l_Helper(
            stdWord32_TestNumbers[i]
        );
    }
}

void test_norm_l_Helper(Word32 L_var1) {
    Word16 result = norm_l(L_var1);

    py_V1W32_ResultW16("norm_l", L_var1, result);
}

void test_norm_s() {
    printf("print(\"Testing norm_s\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        test_norm_s_Helper(stdWord16_TestNumbers[i]);
    }
}

void test_norm_s_Helper(Word16 var1) {
    Word16 result = norm_s(var1);

    py_V1W16_ResultW16("norm_s", var1, result);
}

void test_round() {
    printf("print(\"Testing round\")\n");

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        test_round_Helper(
            stdWord32_TestNumbers[i]
        );
    }
}

void test_round_Helper(Word32 L_var1) {
    Word16 result = round(L_var1);

    py_V1W32_ResultW16("round", L_var1, result);
}

void test_sature() {
    printf("print(\"Testing sature\")\n");

    // Clear flags    
    clearFlags();

    for (int i=0; i<LENGTH_WORD32_TEST_NUMBERS; i++) {
        test_sature_Helper(
            stdWord32_TestNumbers[i]
        );
    }
}

void test_sature_Helper(Word32 L_var1) {
    Word16 result = sature(L_var1);

    py_V1W32_ResultW16_Flags("sature", "", L_var1, result);

    // Clear flags    
    clearFlags();
}

void test_shl() {
    printf("print(\"Testing shl\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            test_shl_Helper(
                stdWord16_TestNumbers[i],
                stdWord16_TestNumbers[j]
            );
        }
    }
}

void test_shl_Helper(Word16 var1, Word16 var2) {
    Word16 result = shl(var1, var2);

    py_V1W16_V2W16_ResultW16("shl", var1, var2, result);
}

void test_shr() {
    printf("print(\"Testing shr\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            test_shr_Helper(
                stdWord16_TestNumbers[i],
                stdWord16_TestNumbers[j]
            );
        }
    }
}

void test_shr_Helper(Word16 var1, Word16 var2) {
    Word16 result = shr(var1, var2);

    py_V1W16_V2W16_ResultW16("shr", var1, var2, result);
}

void test_shr_r() {
    printf("print(\"Testing shr_r\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            test_shr_r_Helper(
                stdWord16_TestNumbers[i],
                stdWord16_TestNumbers[j]
            );
        }
    }
}

void test_shr_r_Helper(Word16 var1, Word16 var2) {
    Word16 result = shr_r(var1, var2);

    py_V1W16_V2W16_ResultW16("shr_r", var1, var2, result);
}

void test_sub() {
    printf("print(\"Testing sub\")\n");

    for (int i=0; i<LENGTH_WORD16_TEST_NUMBERS; i++) {
        for (int j=0; j<LENGTH_WORD16_TEST_NUMBERS; j++) {
            test_sub_Helper(
                stdWord16_TestNumbers[i],
                stdWord16_TestNumbers[j]
            );
        }
    }
}

void test_sub_Helper(Word16 var1, Word16 var2) {
    Word16 result = sub(var1, var2);

    py_V1W16_V2W16_ResultW16("sub", var1, var2, result);
}

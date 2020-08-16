#include <stdio.h>
#include <stdlib.h>

#include "typedef.h"
#include "basic_op.h"

Word16 MAX_14 = (Word16) 0x00004000;
Word32 MAX_30 = (Word32) 0x3fffffffL;

extern Flag Overflow;
extern Flag Carry;

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

    // Check methods
    test_abs_s();
    test_add();
    test_div_s();
    test_extract_h();
    test_extract_l();
    test_L_abs();
    test_L_add_c();
    test_L_add();
}

void clearFlagsHelper() {
    // Clear Python flags
    printf("setOverflow(0)");
    printf("\n");
    printf("setCarry(0)");
    printf("\n");

    // Clear C flags
    Overflow = 0;
    Carry = 0;
}

void printLineBreak() {
    printf("print(\"\\n\")");
    printf("\n");
}


void testConstants() {
    // Maxes
    printf("print(f\"{MAX_INT_14 == %d} - MAX_INT_14 matches %d\")", MAX_14, MAX_14);
    printf("\n"); 

    printf("print(f\"{MAX_INT_16 == %d} - MAX_INT_16 matches %d\")", MAX_16, MAX_16);
    printf("\n"); 

    printf("print(f\"{MAX_INT_30 == %d} - MAX_INT_30 matches %d\")", MAX_30, MAX_30);
    printf("\n"); 

    printf("print(f\"{MAX_INT_32 == %d} - MAX_INT_32 matches %d\")", MAX_32, MAX_32);
    printf("\n"); 

    // Mins
    printf("print(f\"{MIN_INT_16 == %d} - MIN_INT_16 matches %d\")", MIN_16, MIN_16);
    printf("\n"); 

    printf("print(f\"{MIN_INT_32 == %d} - MIN_INT_32 matches %d\")", MIN_32, MIN_32);
    printf("\n");

    printLineBreak(); 
}

void test_abs_s() {
    test_abs_s_Helper(MIN_16);
    test_abs_s_Helper((Word16)-1);
    test_abs_s_Helper((Word16)0);
    test_abs_s_Helper((Word16)1);
    test_abs_s_Helper(MAX_16);

    printLineBreak(); 
}

void test_abs_s_Helper(Word16 var) {
    Word16 result = abs_s(var);

    printf("print(f\"{abs_s(%d) == %d} - abs_s(%d) = %d\")", var, result, var, result);
    printf("\n");
}

void test_add() {
    test_add_Helper(MIN_16, (Word16)-1);
    test_add_Helper(MIN_16, (Word16)0);
    test_add_Helper(MIN_16, (Word16)1);
    test_add_Helper((Word16)0, (Word16)-1);
    test_add_Helper((Word16)0, (Word16)0);
    test_add_Helper((Word16)0, (Word16)1);
    test_add_Helper(MAX_16, (Word16)-1);
    test_add_Helper(MAX_16, (Word16)0);
    test_add_Helper(MAX_16, (Word16)1);

    printLineBreak(); 
}

void test_add_Helper(Word16 var1, Word16 var2) {
    Word16 result = add(var1, var2);

    printf("print(f\"{add(%d,%d) == %d} - add(%d,%d) = %d\")", var1, var2, result, var1, var2, result);
    printf("\n"); 
}

void test_div_s() {
    int i, j;

    test_div_s_Helper((Word16)0, (Word16)245);
    test_div_s_Helper((Word16)357, (Word16)357);
    test_div_s_Helper((Word16)1325, MAX_16);

    printLineBreak(); 
}

void test_div_s_Helper(Word16 var1, Word16 var2) {
    Word16 result = div_s(var1, var2);

    printf("print(f\"{div_s(%d,%d) == %d} - div_s(%d,%d) = %d\")", var1, var2, result, var1, var2, result);
    printf("\n"); 
}

void test_extract_h() {
    test_extract_h_Helper(MIN_32);
    test_extract_h_Helper((Word32)(MIN_16 - (Word32)1));
    test_extract_h_Helper(MIN_16);
    test_extract_h_Helper(MIN_16 + (Word16)1);
    test_extract_h_Helper((Word16)-1);
    test_extract_h_Helper((Word16)0);
    test_extract_h_Helper((Word16)1);
    test_extract_h_Helper(MAX_16);
    test_extract_h_Helper((Word32)(MAX_16 + (Word32)1));
    test_extract_h_Helper(MAX_32);

    printLineBreak(); 
}

void test_extract_h_Helper(Word32 var) {
    Word16 result = extract_h(var);

    printf("print(f\"{extract_h(%d) == %d} - extract_h(%d) = %d\")", var, result, var, result);
    printf("\n"); 
}

void test_extract_l() {
    test_extract_l_Helper(MIN_32);
    test_extract_l_Helper((Word32)(MIN_16 - (Word32)1));
    test_extract_l_Helper(MIN_16);
    test_extract_l_Helper(MIN_16 + (Word16)1);
    test_extract_l_Helper((Word16)-1);
    test_extract_l_Helper((Word16)0);
    test_extract_l_Helper((Word16)1);
    test_extract_l_Helper(MAX_16);
    test_extract_l_Helper((Word32)(MAX_16 + (Word32)1));
    test_extract_l_Helper(MAX_32);

    printLineBreak(); 
}

void test_extract_l_Helper(Word32 var) {
    Word16 result = extract_l(var);

    printf("print(f\"{extract_l(%d) == %d} - extract_l(%d) = %d\")", var, result, var, result);
    printf("\n"); 
}

void test_L_abs() {
    test_extract_l_Helper(MIN_32);
    test_extract_l_Helper((Word32)-1);
    test_extract_l_Helper((Word32)0);
    test_extract_l_Helper((Word32)1);
    test_extract_l_Helper(MAX_32);

    printLineBreak(); 
}

void test_L_abs_Helper(Word32 var) {
    Word32 result = L_abs(var);

    printf("print(f\"{L_abs(%d) == %d} - L_abs(%d) = %d\")", var, result, var, result);
    printf("\n");
}

void test_L_add_c() {
    // Clear Flags
    clearFlagsHelper();

    // Test
    test_L_add_c_Helper(MIN_32, MIN_32);
    test_L_add_c_Helper(MIN_32, (Word32)-10123);
    test_L_add_c_Helper(MIN_32, (Word32)-1);
    test_L_add_c_Helper(MIN_32 - 1, (Word32)1);
    test_L_add_c_Helper(MIN_32 + 1, (Word32)-1);

    test_L_add_c_Helper(-1, 0);
    test_L_add_c_Helper(0, 0);
    test_L_add_c_Helper(0, 1);
    
    test_L_add_c_Helper(MAX_32 - 1, (Word32)1);
    test_L_add_c_Helper(MAX_32 + 1, (Word32)-1);
    test_L_add_c_Helper(MAX_32, (Word32)1);
    test_L_add_c_Helper(MAX_32, (Word32)10123);
    test_L_add_c_Helper(MAX_32, MAX_32);

    printLineBreak(); 
}

void test_L_add_c_Helper(Word32 L_var1, Word32 L_var2) {
    // Run all 4 variations
    test_L_add_c_Helper_No_Flag(L_var1, L_var2);
    test_L_add_c_Helper_with_Overflow(L_var1, L_var2);
    test_L_add_c_Helper_with_Carry(L_var1, L_var2);
    test_L_add_c_Helper_with_OverflowAndCarry(L_var1, L_var2);
    printLineBreak(); 
}

void test_L_add_c_Helper_No_Flag(Word32 L_var1, Word32 L_var2) {
    printf("setOverflow(0)\n");
    printf("setCarry(0)\n");
    Overflow = 0;
    Carry = 0;

    // Run test
    printf("print(f\"Flags __: testing var1=%d var2=%d\")", L_var1, L_var2);
    printf("\n");
    test_L_add_c_Helper_Worker(L_var1, L_var2);

    // Clear flags    
    clearFlagsHelper();
}

void test_L_add_c_Helper_with_Overflow(Word32 L_var1, Word32 L_var2) {
    printf("setOverflow(1)\n");
    printf("setCarry(0)\n");
    Overflow = 1;
    Carry = 0;

    // Run test
    printf("print(f\"Flags O_: testing var1=%d var2=%d\")", L_var1, L_var2);
    printf("\n");
    test_L_add_c_Helper_Worker(L_var1, L_var2);

    // Clear flags    
    clearFlagsHelper();
}

void test_L_add_c_Helper_with_Carry(Word32 L_var1, Word32 L_var2) {
    printf("setOverflow(0)\n");
    printf("setCarry(1)\n");
    Overflow = 0;
    Carry = 1;

    // Run test
    printf("print(f\"Flags _C: testing var1=%d var2=%d\")", L_var1, L_var2);
    printf("\n");
    test_L_add_c_Helper_Worker(L_var1, L_var2);

    // Clear flags    
    clearFlagsHelper();
}

void test_L_add_c_Helper_with_OverflowAndCarry(Word32 L_var1, Word32 L_var2) {
    printf("setOverflow(1)\n");
    printf("setCarry(1)\n");
    Overflow = 1;
    Carry = 1;

    // Run test
    printf("print(f\"Flags OC: testing var1=%d var2=%d\")", L_var1, L_var2);
    printf("\n");
    test_L_add_c_Helper_Worker(L_var1, L_var2);

    // Clear flags    
    clearFlagsHelper();
}

void test_L_add_c_Helper_Worker(Word32 L_var1, Word32 L_var2) {
    Word32 result = L_add_c(L_var1, L_var2);

    // Check Comp
    printf("print(f\"\t{L_add_c(%d,%d) == %d} - L_add_c(%d,%d) = %d\")", L_var1, L_var2, result, L_var1, L_var2, result);
    printf("\n");

    // Check Flags
    printf("print(f\"\t{getOverflow() == %d} - Overflow = %d\")", Overflow, Overflow);
    printf("\n");

    printf("print(f\"\t{getCarry() == %d} - Carry = %d\")", Carry, Carry);
    printf("\n");
}

void test_L_add() {
    // Clear flags    
    clearFlagsHelper();

    test_L_add_Helper(MIN_32, MIN_32);
    test_L_add_Helper(MIN_32, MIN_32 + (Word32)1);
    test_L_add_Helper(MIN_32, (Word32)-1);
    test_L_add_Helper(MIN_32, (Word32)0);
    test_L_add_Helper(MIN_32, (Word32)1);
    test_L_add_Helper((Word32)0, (Word32)-1);
    test_L_add_Helper((Word32)0, (Word32)0);
    test_L_add_Helper((Word32)0, (Word32)1);
    test_L_add_Helper(MAX_32, (Word32)-1);
    test_L_add_Helper(MAX_32, (Word32)0);
    test_L_add_Helper(MAX_32, (Word32)1);
    test_L_add_Helper(MAX_32, MAX_32 - (Word32)1);
    test_L_add_Helper(MAX_32, MAX_32);

    printLineBreak();
}

void test_L_add_Helper(Word32 var1, Word32 var2) {
    Word32 result = L_add(var1, var2);

    // Check Comp
    printf("print(f\"{L_add(%d,%d) == %d} - L_add(%d,%d) = %d\")", var1, var2, result, var1, var2, result);
    printf("\n"); 

    // Check Flags
    printf("print(f\"{getOverflow() == %d} - Overflow = %d\")", Overflow, Overflow);
    printf("\n");

    // Clear flags    
    clearFlagsHelper();
}

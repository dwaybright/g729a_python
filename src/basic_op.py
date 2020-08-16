import ctypes

from typing import Tuple

# Flags
OVERFLOW = 0
CARRY = 0

# Max
MAX_INT_14 = 16384          # 0x00004000
MAX_INT_16 = 32767          # 0x7fff
MAX_INT_30 = 1073741823     # 0x3fffffff
MAX_INT_32 = 2147483647     # 0x7fffffff

# Min
MIN_INT_16 = -32768         # 0x8000
MIN_INT_30 = -1073741824    # 0xc0000000
MIN_INT_32 = -2147483648    # 0x80000000


def getOverflow() -> int:
    return OVERFLOW

def setOverflow(value: int) -> None:
    global OVERFLOW
    OVERFLOW = value

def getCarry() -> int:
    return CARRY

def setCarry(value: int) -> None:
    global CARRY
    CARRY = value

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L69
def sature(L_var1: int, useOverflow = True) -> int:
    result = L_var1

    if L_var1 > MAX_INT_16:
        if useOverflow:
            setOverflow(1)
        
        result = MAX_INT_16
    elif L_var1 < MIN_INT_16:
        if useOverflow:
            setOverflow(1)
        
        result = MIN_INT_16
    
    return result

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L490
def negate(var1: int) -> int:
    if var1 == MIN_INT_16:
        return MAX_INT_16
    
    return (-1) * var1

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L126
def add(var1: int, var2: int) -> int:
    return sature(var1 + var2)

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L170
def sub(var1: int, var2: int) -> int:
    return sature(var1 - var2)

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L208
def abs_s(var1: int) -> int:
    if var1 >= 0:
        return var1

    return negate(var1)

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L265
def shl(var1: int, var2: int) -> int:
    # negative shifts mean shift other way
    if var2 < 0:
        return shr(var1, negate(var2))
    
    return sature(var1 * (1 << var2), useOverflow=True)

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L325
def shr(var1: int, var2: int) -> int:
    # negative shifts mean shift other way
    if var2 < 0:
        return shl(var1, negate(var2))
    
    # 16 bits, can only shift so many times
    if var2 >= 15:
        if var1 < 0:
            return -1
        else:
            return 0
    
    # actually perform a shift
    if var1 < 0:
        return ~( (~var1) >> var2 )
    else:
        return var1 >> var2

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L390
def mult(var1: int, var2: int) -> int:
    product = var1 * var2
    #print(f"\t\tvar1: {var1}  var2: {var2}  product_1: {product}")

    product = (product & -32768) >> 15
    #print(f"\t\tvar1: {var1}  var2: {var2}  product_2: {product}")

    if (product & 65536):
        product = product | -65536
    #print(f"\t\tvar1: {var1}  var2: {var2}  product_3: {product}")

    var_out = sature(product)
    return var_out


def L_sature(L_var1: int, useOverflow = True) -> int:
    result = L_var1

    if L_var1 > MAX_INT_32:
        if useOverflow:
            setOverflow(1)
        
        result = MAX_INT_32
    elif L_var1 < MIN_INT_32:
        if useOverflow:
            setOverflow(1)
        
        result = MIN_INT_32
    
    return result

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L442
def L_mult(var1: int, var2: int) -> int:
    L_var_out = var1 * var2
    
    if L_var_out != 1073741824:
        L_var_out = L_var_out * 2
    else:
        setOverflow(1)
        L_var_out = MAX_INT_32

    return L_var_out

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1138
def L_negate(L_var1: int) -> int:
    return L_sature(-1 * L_var1)

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L527
def extract_h(L_var1: int) -> int:
    return sature(L_var1 >> 16, useOverflow=False)

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L563
def extract_l(L_var1: int) -> int:
    return ctypes.c_short(L_var1).value

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L603
def round(L_var1: int) -> int:
    L_arrondi = L_add(L_var1, 32768)

    return extract_h(L_arrondi)

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L651
def L_mac(L_var3: int, var1: int, var2: int) -> int:
    product = L_mult(var1, var2)
    result = L_add(L_var3, product)

    result = L_sature(result)
    return result

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L699
def L_msu(L_var3: int, var1: int, var2: int) -> int:
    product = L_mult(var1, var2)
    result = L_sub(L_var3, product)

    return L_sature(result)

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L753
def L_macNs(L_var3: int, var1: int, var2: int) -> int:
    product = L_mult(var1, var2)
    result = L_add_c(L_var3, product)

    return result

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L805
def L_msuNs(L_var3: int, var1: int, var2: int) -> int:
    product = L_mult(var1, var2)
    result = L_sub_c(L_var3, product)

    return result

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L846
def L_add(L_var1, L_var2) -> int:
    L_var_out = L_var1 + L_var2
    
    if (L_var1 ^ L_var2) & MIN_INT_32 == 0:
        if (L_var_out ^ L_var1) & MIN_INT_32 != 0:
            setOverflow(1)

            if L_var1 < 0:
                L_var_out = MIN_INT_32
            else:
                L_var_out = MAX_INT_32
            
    return L_var_out

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L895
def L_sub(L_var1, L_var2) -> int:
    return L_sature(L_var1 - L_var2)

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L949
def L_add_c(L_var1, L_var2) -> int:
    carry_int = 0

    L_var_out = L_var1 + L_var2 + getCarry()
    L_test = L_var1 + L_var2

    # Boundary cleanups
    if L_var_out <= MIN_INT_32:
        L_var_out = (-2 * MIN_INT_32) + L_var_out
        L_test = (-2 * MIN_INT_32) + L_test

        if L_var_out > MAX_INT_32:
            L_var_out = MIN_INT_32
    elif L_var_out > MAX_INT_32:
        L_var_out = (2 * MIN_INT_32) + L_var_out
    
    
    if L_test > MAX_INT_32:
        L_test = MIN_INT_32
    
    # print(f"\t\tPython: L_var1: {L_var1}    L_var2: {L_var2}")
    # print(f"\t\tPython: L_var_out: {L_var_out}    L_test: {L_test}")

    if L_var1 > 0 and L_var2 > 0 and L_test < 0:
        setOverflow(1)
        carry_int = 0
    else:
        if L_var1 < 0 and L_var2 < 0 and L_test > 0:
            setOverflow(1)
            carry_int = 1
        else:
            if (L_var1 ^ L_var2) < 0 and L_test > 0:
                setOverflow(0)
                carry_int = 1
            else:
                setOverflow(0)
                carry_int = 0

    if getCarry() != 0:
        if L_test == MAX_INT_32:
            setOverflow(1)
            setCarry(carry_int)
        else:
            if L_test == -1:
                setCarry(1)
            else:
                setCarry(carry_int)
    else:
        setCarry (carry_int)

    return L_var_out


# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1051
def L_sub_c(L_var1, L_var2) -> Tuple[int, int, int]:
    carry_int = 0

    if getCarry() > 0:
        setCarry(0)

        if L_var2 != MIN_INT_32:
            L_var_out = L_add_c(L_var1, -L_var2)
        else:
            L_var_out = L_var1 - L_var2

            if L_var1 > 0:
                setOverflow(1)
                setCarry(0)
    else:
        L_var_out = L_var1 - L_var2 - 1
        L_test = L_var1 - L_var2

        if (L_test < 0) and (L_var1 > 0) and (L_var2 < 0):
            setOverflow(1)
            carry_int = 0
        elif (L_test > 0) and (L_var1 < 0) and (L_var2 > 0):
            setOverflow(1)
            carry_int = 1
        elif (L_test > 0) and ((L_var1 ^ L_var2) > 0):
            setOverflow(0)
            carry_int = 1

        if L_test == MIN_INT_32:
            setOverflow(1)
            setCarry(carry_int)
        else:
            setCarry(carry_int)

    return L_var_out


# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1180
def mult_r(var1: int, var2: int) -> int:
    result = var1 * var2            # product
    result = result + MAX_INT_14    # round
    result = result & -32768        # mask
    result = result >> 15           # shifted

    # sign extend when necessary
    if (result & 65536) != 0:
        result = result | -65536

    return sature(result)

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1233
def L_shl(L_var1: int, var2: int) -> int:
    if var2 <= 0:
        return L_shr(L_var1, -1 * var2)
    
    # for step in range(0, var2):
    while var2 > 0:
        if L_var1 > MAX_INT_30:
            setOverflow(1)
            return MAX_INT_32
        elif L_var1 < MIN_INT_30:
            setOverflow(1)
            return MIN_INT_32
        
        L_var1 = L_var1 * 2
        result = L_var1

        var2 = var2 - 1
    
    return result

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1305
def L_shr(L_var1: int, var2: int) -> int:
    if var2 < 0:
        return L_shl(L_var1, -1 * var2)
    
    if var2 >= 31:
        if L_var1 < 0:
            return -1
        else:
            return 0
    else:
        if L_var1 < 0:
            return ~( (~L_var1) >> var2)
        else:
            return L_var1 >> var2

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1433
def mac_r(L_var3: int, var1: int, var2: int) -> int:
    result = L_mac(L_var3, var1, var2)
    result = L_add(result, 32768)
    result = extract_h(result)

    return result

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1483
def msu_r(L_var3: int, var1: int, var2: int) -> int:
    result = L_msu(L_var3, var1, var2)
    result = L_add(result, 32768)
    result = extract_h(result)

    return result

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1524
def L_deposit_h(var1: int) -> int:
    return L_sature(var1 << 16)

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1561
def L_deposit_l(var1: int) -> int:
    return sature(var1)

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1606
def L_shr_r(L_var1: int, var2: int) -> int:
    if var2 > 31:
        return 0
    
    result = L_shr(L_var1, var2)
    if var2 > 0:
        test = 1 << (var2 - 1)

        if L_var1 & test != 0:
            result = result + 1
    
    return result


def shr_r(var1: int, var2: int) -> int:

    if var2 > 15:
        var_out = 0
    else:
        var_out = shr(var1, var2)

        if var2 > 0:
            if ((var1 & (1 << (var2 - 1))) != 0):
                var_out = var_out + 1

    return var_out


# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1657
def L_abs(L_var1: int) -> int:
    if L_var1 >= 0:
        return L_var1

    return L_negate(L_var1)

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1711
def L_sat(L_var1: int) -> int:
    result = L_var1

    if getOverflow() != 0:
        if getCarry() != 0:
            result = MIN_INT_32
        else:
            result = MAX_INT_32
        
        setCarry(0)
        setOverflow(0)
    
    return result

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1771
def norm_s(var1: int) -> int:

    if var1 == 0:
        return 0
    elif var1 == -1:
        return 15 

    result = 0
    test = var1
    if test < 0:
        test = ~test
    
    while test < MAX_INT_14:
        test = test << 1
        result = result + 1

    return result

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1840
def div_s(var1: int, var2: int) -> int:

    if var1 > var2 or var1 < 0 or var2 < 0:
        print(f"Division Error var1={var1} var2={var2}")
        exit()

    if var2 == 0:
        print("Division by 0, Fatal error")
        exit()

    if var1 == 0:
        return 0
    
    if var1 == var2:
        return MAX_INT_16
    
    result = 0
    L_num = L_deposit_l(var1)
    L_denom = L_deposit_l(var2)

    for step in range(0, 15):
        result = result << 1
        L_num = L_num << 1

        if L_num >= L_denom:
            L_num = L_sub(L_num, L_denom)
            result = add(result, 1)
    
    return result

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/BASIC_OP.C#L1925
def norm_l(L_var1: int) -> int:
    if L_var1 == 0:
        return 0
    elif L_var1 == -1:
        return 31
    
    result = 0
    test = L_var1
    if test < 0:
        test = ~test
    
    while test < 1073741824:
        test = test << 1
        result = result + 1
    
    return result

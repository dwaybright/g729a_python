import basic_op

from typing import Tuple


def L_Extract(L_32: int) -> Tuple[int, int]:
    hi = basic_op.extract_h(L_32)
    lo = basic_op.extract_l(basic_op.L_msu(basic_op.L_shr(L_32, 1), hi, 16384))

    return (hi, lo)


def L_Comp(hi: int, lo: int) -> int:
    L_32 = basic_op.L_deposit_h(hi)

    return basic_op.L_mac(L_32, lo, 1)


def Mpy_32(hi1: int, lo1: int, hi2: int, lo2: int) -> int:
    L_32 = basic_op.L_mult(hi1, hi2)
    L_32 = basic_op.L_mac(L_32, basic_op.mult(hi1, lo2), 1)
    L_32 = basic_op.L_mac(L_32, basic_op.mult(lo1, hi2), 1)

    return L_32

def Mpy_32_16(hi: int, lo: int, n: int) -> int:
    L_32 = basic_op.L_mult(hi, n)
    L_32 = basic_op.L_mac(basic_op.L_32, mult(lo, n) , 1)

    return L_32

def Div_32(L_num: int, denom_hi: int, denom_lo: int) -> int:

    # First approximation: 1 / L_denom = 1/denom_hi
    constOne = 16383                    # (Word16)0x3fff
    approx = div_s( 16383, denom_hi)    # result in Q14 
                                        # Note: 3fff = 0.5 in Q15 

    # 1/L_denom = approx * (2.0 - L_denom * approx) 

    L_32 = Mpy_32_16(denom_hi, denom_lo, approx) # result in Q30 

    L_32 = L_sub(basic_op.MAX_INT_32, L_32)      # result in Q30 

    hi, lo = L_Extract(L_32, hi, lo)

    L_32 = Mpy_32_16(hi, lo, approx)             # = 1/L_denom in Q29 

    # L_num * (1/L_denom) 

    hi, lo = L_Extract(L_32, hi, lo)
    n_hi, n_lo = L_Extract(L_num, n_hi, n_lo)
    L_32 = Mpy_32(n_hi, n_lo, hi, lo)            # result in Q29   
    L_32 = basic_op.L_shl(L_32, 2)               # From Q29 to Q31 

    return L_32

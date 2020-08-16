import basic_op
import ld8a
import tab_ld8a

from typing import Tuple

def Pow2(exponent: int, fraction: int) -> int:
    """
    # (o) Q0  : result       (range: 0<=val<=0x7fffffff)
    # (i) Q0  : Integer part.      (range: 0<=val<=30)
    # (i) Q15 : Fractional part.   (range: 0.0<=val<1.0)
    """

    L_x = basic_op.L_mult(fraction, 32)         # L_x = fraction<<6
    i   = basic_op.extract_h(L_x)               # Extract b10-b15 of fraction 
    L_x = basic_op.L_shr(L_x, 1)
    a   = basic_op.extract_l(L_x)               # Extract b0-b9   of fraction 
    a   = a & 0x7fff

    L_x = basic_op.L_deposit_h(tab_ld8a.tabpow[i])       # tabpow[i] << 16        
    tmp = basic_op.sub(tab_ld8a.tabpow[i], tab_ld8a.tabpow[i+1])  # tabpow[i] - tabpow[i+1] 
    L_x = basic_op.L_msu(L_x, tmp, a)           # L_x -= tmp*a*2        

    exp = basic_op.sub(30, exponent)
    L_x = basic_op.L_shr_r(L_x, exp)

    return L_x

def Log2(L_x: int, exponent: int, fraction: int) -> Tuple[int, int]:
    """
    # (i) Q0 : input value 
    # (o) Q0 : Integer part of Log2.   (range: 0<=val<=30)
    # (o) Q15: Fractional  part of Log2. (range: 0<=val<1)
    """

    if  L_x <= 0:
        return (0, 0)

    exp = basic_op.norm_l(L_x)
    L_x = basic_op.L_shl(L_x, exp )               # L_x is normalized 

    exponent = basic_op.sub(30, exp)

    L_x = basic_op.L_shr(L_x, 9)
    i   = basic_op.extract_h(L_x)                 # Extract b25-b31 
    L_x = basic_op.L_shr(L_x, 1)
    a   = basic_op.extract_l(L_x)                 # Extract b10-b24 of fraction 
    a   = a & 0x7fff

    i   = basic_op.sub(i, 32)

    L_y = basic_op.L_deposit_h(tab_ld8a.tablog[i])         # tablog[i] << 16        
    tmp = basic_op.sub(tab_ld8a.tablog[i], tab_ld8a.tablog[i+1])    # tablog[i] - tablog[i+1] 
    L_y = basic_op.L_msu(L_y, tmp, a)             # L_y -= tmp*a*2        

    fraction = basic_op.extract_h( L_y)

    return (exponent, fraction)

def Inv_sqrt(L_x) -> int:
    """
    # (o) Q30 : output value   (range: 0<=val<1)
    # (i) Q0  : input value    (range: 0<=val<=7fffffff)
    """

    if L_x <= 0: 
        return basic_op.MAX_INT_30

    exp = basic_op.norm_l(L_x)
    L_x = basic_op.L_shl(L_x, exp )               # L_x is normalize 

    exp = basic_op.sub(30, exp)
    if (exp & 1) == 0:                  # If exponent even -> shift right 
        L_x = basic_op.L_shr(L_x, 1)

    exp = basic_op.shr(exp, 1)
    exp = basic_op.add(exp, 1)

    L_x = basic_op.L_shr(L_x, 9)
    i   = basic_op.extract_h(L_x)                 # Extract b25-b31 
    L_x = basic_op.L_shr(L_x, 1)
    a   = basic_op.extract_l(L_x)                 # Extract b10-b24 
    a   = a & 0x7fff

    i   = basic_op.sub(i, 16)

    L_y = basic_op.L_deposit_h(tab_ld8a.tabsqr[i])         # tabsqr[i] << 16          
    tmp = basic_op.sub(tab_ld8a.tabsqr[i], tab_ld8a.tabsqr[i+1])    # tabsqr[i] - tabsqr[i+1])  
    L_y = basic_op.L_msu(L_y, tmp, a)             # L_y -=  tmp*a*2         

    L_y = basic_op.L_shr(L_y, exp)                # denormalization 

    return L_y

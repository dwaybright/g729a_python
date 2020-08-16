from basic_op import L_add, L_mac, L_shl, round
from oper_32b import L_Extract, Mpy_32_16
from tab_ld8a import a140, b140

from typing import List

y2_hi = 0
y2_lo = 0 
y1_hi = 0 
y1_lo = 0 
x0 = 0
x1 = 0

def Init_Pre_Process() -> None:
    global y2_hi
    global y2_lo
    global y1_hi
    global y1_lo
    global x0
    global x1

    y2_hi = 0
    y2_lo = 0
    y1_hi = 0
    y1_lo = 0
    x0   = 0
    x1   = 0


def Pre_Process(signal: List[int], lg: int) -> None:
    """
    # input/output signal
    # length of signal
    """

    global y2_hi
    global y2_lo
    global y1_hi
    global y1_lo
    global x0
    global x1

    for i in range(0, lg):
        x2 = x1
        x1 = x0
        x0 = signal[i]

        #  y[i] = b[0]*x[i]/2 + b[1]*x[i-1]/2 + b140[2]*x[i-2]/2  
        #                     + a[1]*y[i-1] + a[2] * y[i-2]      

        L_tmp     = Mpy_32_16(y1_hi, y1_lo, a140[1])
        L_tmp     = L_add(L_tmp, Mpy_32_16(y2_hi, y2_lo, a140[2]))
        L_tmp     = L_mac(L_tmp, x0, b140[0])
        L_tmp     = L_mac(L_tmp, x1, b140[1])
        L_tmp     = L_mac(L_tmp, x2, b140[2])
        L_tmp     = L_shl(L_tmp, 3)                     # Q28 --> Q31 (Q12 --> Q15) 
        signal[i] = round(L_tmp)

        y2_hi = y1_hi
        y2_lo = y1_lo
        y1_hi, y1_lo = L_Extract(L_tmp)

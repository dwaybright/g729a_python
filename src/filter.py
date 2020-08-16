import basic_op
import ld8a

from typing import List

def Convolve(x: List[int], h: List[int], y: List[int], L: int) -> None:
    """
    # (i)     : input vector
    # (i) Q12 : impulse response
    # (o)     : output vector
    # (i)     : vector size
    """

    for n in range(0, L):
        s = 0
        for i in range(0, n + 1):
            s = basic_op.L_mac(s, x[i], h[n-i])

        s    = basic_op.L_shl(s, 3)                   # h is in Q12 and saturation
        y[n] = basic_op.extract_h(s)

def Syn_filt(a: List[int], x: List[int], y: List[int], lg: int, mem: List[int], update: int) -> None:
    """
    # (i) Q12 : a[m+1] prediction coefficients   (m=10)
    # (i)     : input signal
    # (o)     : output signal
    # (i)     : size of filtering
    # (i/o)   : memory associated with this filtering.
    # (i)     : 0=no update, 1=update of memory.
    """

    #Word16 i, j
    #Word32 s
    #Word16 tmp[100]     # This is usually done by memory allocation (lg+M) 
    #Word16 *yy

    tmp = [0] * 100

    # Copy mem[] to yy[] (yy points to tmp)
    for i in range(0, ld8a.M):
        tmp[i] = mem[i]

    # Do the filtering. 
    for i in range(0, lg):
        s = basic_op.L_mult(x[i], a[0])

        for j in range(1, ld8a.M + 1):
            # this negative index needs tested
            s = basic_op.L_msu(s, a[j], tmp[-j])

        s = basic_op.L_shl(s, 3)
        tmp[i] = basic_op.round(s)
    
    for i in range (0, lg):
        y[i] = tmp[i+M]

    # Update of memory if update==1 

    if update != 0:
        for i in range(0, ld8a.M):
            mem[i] = y[lg-M+i]


def Residu(a: List[int], x: List[int], y: List[int], lg: int) -> None:
    """
    # (i) Q12 : prediction coefficients 
    # (i)     : speech (values x[-m..-1] are needed
    # (o)     : residual signal 
    # (i)     : size of filtering
    """

    for i in range(0, lg):
        s = basic_op.L_mult(x[i], a[0])
        
        for j in range(1, ld8a.M + 1):
            s = basic_op.L_mac(s, a[j], x[i-j])

        s = basic_op.L_shl(s, 3)
        y[i] = basic_op.round(s)

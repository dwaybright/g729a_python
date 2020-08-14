from basic_op import *
from oper_32b import *
from ld8a import *
from tab_ld8a import *
from core_func import *

from typing import List, Tuple


def Pitch_ol_fast(signal: List[int], pit_max: int, L_frame: int) -> int:
    # output: open loop pitch lag
    # input : signal used to compute the open loop pitch
    # signal[-pit_max] to signal[-1] should be known
    # input : maximum pitch lag
    # input : length of frame to compute pitch

    # Scaled signal

    scaled_signal = [0] * (L_FRAME + PIT_MAX)

    scal_sig = pit_max      # index to scaled_signal[]

    #########
    # Verification for risk of overflow.
    #########

    setOverflow(0)
    sum = 0

    for i in range(-pit_max, L_frame, 2):
        sum = L_mac(sum, signal[i], signal[i])

    #########
    # Scaling of input signal.
    #
    # if Overflow        -> scal_sig[i] = signal[i]>>3
    # else if sum < 1^20 -> scal_sig[i] = signal[i]<<3
    # else               -> scal_sig[i] = signal[i]
    #########

    if getOverflow() == 1:
        for i in range(-pit_max, L_frame):
            scaled_signal[scal_sig + i] = shr(signal[i], 3)
    else:
        L_temp = L_sub(sum, 1048576)

        if L_temp < 0:                          # if (sum < 2^20)
            for i in range(-pit_max, L_frame):
                scaled_signal[scal_sig + i] = shl(signal[i], 3)
        else:
            for i in range(-pit_max, L_frame):
                scaled_signal[scal_sig + i] = signal[i]

    #########
    # The pitch lag search is divided in three sections.
    # Each section cannot have a pitch multiple.
    # We find a maximum for each section.
    # We compare the maxima of each section by favoring small lag.
    #
    #  First section:  lag delay = 20 to 39
    #  Second section: lag delay = 40 to 79
    #  Third section:  lag delay = 80 to 143
    #########

    # First section

    max = MIN_INT_32
    T1 = 20                     # Only to remove warning from some compilers

    for i in range(20, 40):
        p = scal_sig        # index to scaled_signal[]
        p1 = scal_sig - i   # index to scaled_signal[]
        sum = 0

        for j in range(0, L_frame, 2):
            sum = L_mac(sum, scaled_signal[p], scaled_signal[p1])

            p = p + 2
            p1 = p1 + 2

        L_temp = L_sub(sum, max)

        if L_temp > 0:
            max = sum
            T1 = i

    # compute energy of maximum

    sum = 1         # to avoid division by zero
    p = scal_sig - T1

    for i in range(0, L_frame, 2):
        sum = L_mac(sum, scaled_signal[p], scaled_signal[p])

        p = p + 2

    # max1 = max/sqrt(energy)
    # This result will always be on 16 bits !!

    sum = Inv_sqrt(sum)  # 1/sqrt(energy),    result in Q30
    max_h, max_l = L_Extract(max)
    ener_h, ener_l = L_Extract(sum)
    sum = Mpy_32(max_h, max_l, ener_h, ener_l)
    max1 = extract_l(sum)

    # Second section

    max = MIN_INT_32
    T2 = 40                # Only to remove warning from some compilers
    for i in range(40, 80):
        p = scal_sig
        p1 = scal_sig - i
        sum = 0

        for j in range(0, L_frame, 2):
            sum = L_mac(sum, scaled_signal[p], scaled_signal[p1])

            p = p + 2
            p1 = p1 + 2

        L_temp = L_sub(sum, max)

        if L_temp > 0:
            max = sum
            T2 = i

    # compute energy of maximum

    sum = 1            # to avoid division by zero
    p = scal_sig - T2

    for i in range(0, L_frame, 2):
        sum = L_mac(sum, scaled_signal[p], scaled_signal[p])

        p = p + 2

    # max2 = max/sqrt(energy)
    # This result will always be on 16 bits !!

    sum = Inv_sqrt(sum)                     # 1/sqrt(energy),    result in Q30
    max_h, max_l = L_Extract(max)
    ener_h, ener_l = L_Extract(sum)
    sum = Mpy_32(max_h, max_l, ener_h, ener_l)
    max2 = extract_l(sum)

    # Third section

    max = MIN_INT_32
    T3 = 80                         # Only to remove warning from some compilers

    for i in range(80, 143, 2):
        p = scal_sig
        p1 = scal_sig - i
        sum = 0

        for j in range(0, L_frame, 2):
            sum = L_mac(sum, scaled_signal[p], scaled_signal[p1])

            p = p + 2
            p1 = p1 + 2

        L_temp = L_sub(sum, max)

        if L_temp > 0:
            max = sum
            T3 = i

    # Test around max3

    i = T3
    p = scal_sig
    p1 = scal_sig - (i + 1)
    sum = 0

    for j in range(0, L_frame, 2):
        sum = L_mac(sum, scaled_signal[p], scaled_signal[p1])

        p = p + 2
        p1 = p1 + 2

    L_temp = L_sub(sum, max)

    if L_temp > 0:
        max = sum
        T3 = i + 1

    p = scal_sig
    p1 = scal_sig - (i - 1)
    sum = 0

    for j in range(0, L_frame, 2):
        sum = L_mac(sum, scaled_signal[p], scaled_signal[p1])

        p = p + 2
        p1 = p1 + 2

    L_temp = L_sub(sum, max)

    if L_temp > 0:
        max = sum
        T3 = i - 1

    # compute energy of maximum

    sum = 1             # to avoid division by zero
    p = scal_sig - T3

    for i in range(0, L_frame, 2):
        sum = L_mac(sum, scaled_signal[p], scaled_signal[p])

        p = p + 2

    # max1 = max/sqrt(energy)
    # This result will always be on 16 bits !!

    sum = Inv_sqrt(sum)                # 1/sqrt(energy),    result in Q30
    max_h, max_l = L_Extract(max)
    ener_h, ener_l = L_Extract(sum)
    sum = Mpy_32(max_h, max_l, ener_h, ener_l)
    max3 = extract_l(sum)

    #########
    # Test for multiple.
    #########

    # if( abs(T2*2 - T3) < 5)
    #    max2 += max3 * 0.25

    i = sub(shl(T2, 1), T3)
    j = sub(abs_s(i), 5)
    if j < 0:
        max2 = add(max2, shr(max3, 2))

    # if( abs(T2*3 - T3) < 7)
    #    max2 += max3 * 0.25

    i = add(i, T2)
    j = sub(abs_s(i), 7)
    if j < 0:
        max2 = add(max2, shr(max3, 2))

    # if( abs(T1*2 - T2) < 5)
    #    max1 += max2 * 0.20

    i = sub(shl(T1, 1), T2)
    j = sub(abs_s(i), 5)
    if j < 0:
        max1 = add(max1, mult(max2, 6554))

    # if( abs(T1*3 - T2) < 7)
    #    max1 += max2 * 0.20

    i = add(i, T1)
    j = sub(abs_s(i), 7)
    if j < 0:
        max1 = add(max1, mult(max2, 6554))

    #########
    # Compare the 3 sections maxima.                                     *
    #########

    if sub(max1, max2) < 0:
        max1 = max2
        T1 = T2

    if sub(max1, max3) < 0:
        T1 = T3

    return T1


def Dot_Product(x: List[int], y: List[int], lg: int) -> int:
    # (o)   :Result of scalar product.
    # (i)   :First vector.
    # (i)   :Second vector.
    # (i)   :Number of point.

    sum = 0

    for i in range(0, lg):
        sum = L_mac(sum, x[i], y[i])

    return sum


def Pitch_fr3_fast(
    exc: List[int], excIndex: int, xn: List[int], h: List[int], L_subfr: int, 
    t0_min: int, t0_max: int, i_subfr: int, pit_frac: List[int]
) -> Tuple[int, int]:
    # (o)     : pitch period.
    # (i)     : excitation buffer
    # (i)     : target vector
    # (i) Q12 : impulse response of filters.
    # (i)     : Length of subframe
    # (i)     : minimum value in the searched range.
    # (i)     : maximum value in the searched range.
    # (i)     : indicator for first subframe.
    # (o)     : chosen fraction.

    Dn = [0] * L_SUBFR
    exc_tmp = [0] * L_SUBFR
    aliasExc = exc[excIndex:]

    #########
    # Compute correlation of target vector with impulse response.     
    #########

    Cor_h_X(h, xn, Dn)

    #########
    # Find maximum integer delay.                                     
    #########

    max = MIN_INT_32
    t0 = t0_min        # Only to remove warning from some compilers 

    for t in range(t0_min, t0_max + 1):
        oddExcSlice = exc[(excIndex - t):]      # guessing this will do it

        corr = Dot_Product(Dn, oddExcSlice, L_subfr)
        L_temp = L_sub(corr, max)

        if L_temp > 0:
            max = corr
            t0 = t

    #########
    # Test fractions.                                                 
    #########

    # Fraction 0 

    Pred_lt_3(aliasExc, t0, 0, L_subfr)
    max = Dot_Product(Dn, aliasExc, L_subfr)
    pit_frac = 0

    # If first subframe and lag > 84 do not search fractional pitch 

    if i_subfr == 0 and sub(t0, 84) > 0:
        return t0

    Copy(aliasExc, exc_tmp, L_subfr)

    # Fraction -1/3 

    Pred_lt_3(exc, t0, -1, L_subfr)
    corr = Dot_Product(Dn, aliasExc, L_subfr)
    L_temp = L_sub(corr, max)

    if L_temp > 0:
        max = corr
        pit_frac = -1
        Copy(aliasExc, exc_tmp, L_subfr)

    # Fraction +1/3 

    Pred_lt_3(aliasExc, t0, 1, L_subfr)
    corr = Dot_Product(Dn, aliasExc, L_subfr)
    L_temp = L_sub(corr, max)

    if L_temp > 0:
        max = corr
        pit_frac = 1
    else:
        Copy(exc_tmp, aliasExc, L_subfr)

    return (t0, pit_frac)


def G_pitch(xn: List[int], y1: List[int], g_coeff: List[int], L_subfr:int):
    # (o) Q14 : Gain of pitch lag saturated to 1.2
    # (i)     : Pitch target.
    # (i)     : Filtered adaptive codebook.
    # (i)     : Correlations need for gain quantization.
    # (i)     : Length of subframe.

    scaled_y1 = [0] * L_SUBFR

    # divide "y1[]" by 4 to avoid overflow 

    for i in range(0, L_subfr):
        scaled_y1[i] = shr(y1[i], 2)

    # Compute scalar product <y1[],y1[]> 

    setOverflow(0)
    s = 1                           # Avoid case of all zeros
    for i in range(0, L_subfr):
        s = L_mac(s, y1[i], y1[i])

    if getOverflow() == 0:
        exp_yy = norm_l(s)
        yy = round(L_shl(s, exp_yy))
    else:
        s = 1               # Avoid case of all zeros

        for i in range(0, L_subfr):
            s = L_mac(s, scaled_y1[i], scaled_y1[i])
        
        exp_yy = norm_l(s)
        yy = round(L_shl(s, exp_yy))
        exp_yy = sub(exp_yy, 4)

    # Compute scalar product <xn[],y1[]> 

    setOverflow(0)
    s = 0
    for i in range(0, L_subfr):
        s = L_mac(s, xn[i], y1[i])

    if getOverflow() == 0:
        exp_xy = norm_l(s)
        xy = round(L_shl(s, exp_xy))
    else:
        s = 0

        for i in range(0, L_subfr):
            s = L_mac(s, xn[i], scaled_y1[i])
        
        exp_xy = norm_l(s)
        xy = round(L_shl(s, exp_xy))
        exp_xy = sub(exp_xy, 2)

    g_coeff[0] = yy
    g_coeff[1] = sub(15, exp_yy)
    g_coeff[2] = xy
    g_coeff[3] = sub(15, exp_xy)

    # If (xy <= 0) gain = 0 

    if xy <= 0:
        g_coeff[3] = -15        # Force exp_xy to -15 = (15-30) 
        return 0

    # compute gain = xy/yy 

    xy = shr(xy, 1)             # Be sure xy < yy 
    gain = div_s(xy, yy)

    i = sub(exp_xy, exp_yy)
    gain = shr(gain, i) # saturation if > 1.99 in Q14 

    # if(gain >1.2) gain = 1.2  in Q14 

    if sub(gain, 19661) > 0:
        gain = 19661

    return gain


def Enc_lag3(T0, T0_frac, T0_min, T0_max, pit_min, pit_max, pit_flag) -> Tuple[int, int, int]:
    # output: Return index of encoding
    # input : Pitch delay
    # input : Fractional pitch delay
    # in/out: Minimum search delay
    # in/out: Maximum search delay
    # input : Minimum pitch delay
    # input : Maximum pitch delay
    # input : Flag for 1st subframe

    if pit_flag == 0:           # if 1st subframe 
        # encode pitch delay (with fraction) 

        if sub(T0, 85) <= 0:
            # index = t0*3 - 58 + t0_frac   
            i = add(add(T0, T0), T0)
            index = add(sub(i, 58), T0_frac)
        else:
            index = add(T0, 112)

        # find T0_min and T0_max for second subframe 

        T0_min = sub(T0, 5)
        if sub(T0_min, pit_min) < 0:
            T0_min = pit_min

        T0_max = add(*T0_min, 9)
        if sub(T0_max, pit_max) > 0:
            T0_max = pit_max
            T0_min = sub(T0_max, 9)
    else:       # if second subframe 
        # i = t0 - t0_min               
        # index = i*3 + 2 + t0_frac     
        i = sub(T0, T0_min)
        i = add(add(i, i), i)
        index = add(add(i, 2), T0_frac)

    return (index, T0_min, T0_max)

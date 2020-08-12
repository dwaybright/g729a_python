import ld8a
import basic_op
import core_func

from typing import List, Tuple


def increment(value: int) -> int:
    return value + 1


def decrement(value: int) -> int:
    return value - 1


def ACELP_Code_A(
    x: List[int],           # (i)     :Target vector
    h: List[int],           # (i) Q12 :Inpulse response of filters
    T0: int,                # (i)     :Pitch lag
    pitch_sharp: int,       # (i) Q14 :Last quantized pitch gain
    code: List[int],        # (o) Q13 :Innovative codebook
    y: List[int],           # (o) Q12 :Filtered innovative codebook
    sign: int               # (o)     :Signs of 4 pulses
):
    # https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/ACELP_CA.C#L47

    Dn = [0] * ld8a.L_SUBFR
    rr = [0] * ld8a.DIM_RR

    #########################
    # Include fixed-gain pitch contribution into impulse resp. h[]
    # Find correlations of h[] needed for the codebook search.
    #########################

    sharp = basic_op.shl(pitch_sharp, 1)            # From Q14 to Q15
    if T0 < ld8a.L_SUBFR:
        # h[i] += pitch_sharp*h[i-T0]
        for i in range(T0, ld8a.L_SUBFR):
            product = basic_op.mult(h[i-T0], sharp)
            h[i] = basic_op.add(h[i], product)

    Cor_h(h, rr)

    #########################
    # Compute correlation of target vector with impulse response.
    #########################

    core_func.Cor_h_X(h, x, Dn)

    #########################
    # Find innovative codebook.
    #########################

    index = D4i40_17_fast(Dn, rr, h, code, y, sign)

    #########################
    # Compute innovation vector gain.
    # Include fixed-gain pitch contribution into code[].
    #########################

    if T0 < ld8a.L_SUBFR:
        for i in range(0, ld8a.L_SUBFR):
            code[i] = basic_op.add(code[i], basic_op.mult(code[i-T0], sharp))

    return index


def Cor_h(H: List[int], rr: List[int]) -> None:
    # https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/ACELP_CA.C#L105

    h = [0] * ld8a.L_SUBFR

    # Scaling h[] for maximum precision
    cor = 0
    for i in range(0, ld8a.L_SUBFR):
        cor = basic_op.L_mac(cor, H[i], H[i])

    if basic_op.sub(basic_op.extract_h(cor), 32000) > 0:
        for i in range(0, ld8a.L_SUBFR):
            h[i] = basic_op.shr(H[i], 1)
    else:
        k = basic_op.norm_l(cor)
        k = shr(k, 1)

        for i in range(0, ld8a.L_SUBFR):
            h[i] = shl(H[i], k)

    ############
    # Compute rri0i0[], rri1i1[], rri2i2[], rri3i3 and rri4i4[]
    ############

    rri0i0 = 0                  # index to variable rr
    rri1i1 = rri0i0 + ld8a.NB_POS
    rri2i2 = rri1i1 + ld8a.NB_POS
    rri3i3 = rri2i2 + ld8a.NB_POS
    rri4i4 = rri3i3 + ld8a.NB_POS

    rri0i2 = rri0i1 + ld8a.MSIZE
    rri0i3 = rri0i2 + ld8a.MSIZE
    rri0i4 = rri0i3 + ld8a.MSIZE
    rri1i2 = rri0i4 + ld8a.MSIZE
    rri1i3 = rri1i2 + ld8a.MSIZE
    rri1i4 = rri1i3 + ld8a.MSIZE
    rri2i3 = rri1i4 + ld8a.MSIZE
    rri2i4 = rri2i3 + ld8a.MSIZE

    # Init pointers to last position of rrixix[]
    p0 = rri0i0 + ld8a.NB_POS-1
    p1 = rri1i1 + ld8a.NB_POS-1
    p2 = rri2i2 + ld8a.NB_POS-1
    p3 = rri3i3 + ld8a.NB_POS-1
    p4 = rri4i4 + ld8a.NB_POS-1

    ptr_h1 = 0                  # index to variable h
    cor = 0
    for i in range(0, ld8a.NB_POS):
        cor = basic_op.L_mac(cor, rr[ptr_h1], rr[ptr_h1])
        ptr_h1 = increment(ptr_h1)
        rr[p4] = basic_op.extract_h(cor)
        p4 = decrement(p4)

        cor = basic_op.L_mac(cor, rr[ptr_h1], rr[ptr_h1])
        ptr_h1 = increment(ptr_h1)
        rr[p3] = basic_op.extract_h(cor)
        p3 = decrement(p3)

        cor = basic_op.L_mac(cor, rr[ptr_h1], rr[ptr_h1])
        ptr_h1 = increment(ptr_h1)
        rr[p2] = basic_op.extract_h(cor)
        p2 = decrement(p2)

        cor = basic_op.L_mac(cor, rr[ptr_h1], rr[ptr_h1])
        ptr_h1 = increment(ptr_h1)
        rr[p1] = basic_op.extract_h(cor)
        p1 = decrement(p1)

        cor = basic_op.L_mac(cor, rr[ptr_h1], rr[ptr_h1])
        ptr_h1 = increment(ptr_h1)
        rr[p0] = basic_op.extract_h(cor)
        p0 = decrement(p0)

    ############
    # Compute elements of: rri2i3[], rri1i2[], rri0i1[] and rri0i4[]
    ############

    l_fin_sup = ld8a.MSIZE - 1
    l_fin_inf = l_fin_sup - 1
    ldec = ld8a.NB_POS + 1

    ptr_hd = 0                  # index to variable h
    ptr_hf = ptr_hd + 1

    for k in range(0, ld8a.NB_POS):
        p3 = rri2i3 + l_fin_sup
        p2 = rri1i2 + l_fin_sup
        p1 = rri0i1 + l_fin_sup
        p0 = rri0i4 + l_fin_inf

        cor = 0
        ptr_h1 = ptr_hd
        ptr_h2 = ptr_hf

        for i in range(k + 1, ld8a.NB_POS):
            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p3] = basic_op.extract_h(cor)

            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p2] = basic_op.extract_h(cor)

            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p1] = basic_op.extract_h(cor)

            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p0] = basic_op.extract_h(cor)

            p3 = p3 - ldec
            p2 = p2 - ldec
            p1 = p1 - ldec
            p0 = p0 - ldec

        cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
        ptr_h1 = increment(ptr_h1)
        ptr_h2 = increment(ptr_h2)
        cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
        ptr_h1 = increment(ptr_h1)
        ptr_h2 = increment(ptr_h2)
        rr[p3] = basic_op.extract_h(cor)

        cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
        ptr_h1 = increment(ptr_h1)
        ptr_h2 = increment(ptr_h2)
        rr[p2] = basic_op.extract_h(cor)

        cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
        ptr_h1 = increment(ptr_h1)
        ptr_h2 = increment(ptr_h2)
        rr[p1] = basic_op.extract_h(cor)

        l_fin_sup = l_fin_sup - ld8a.NB_POS
        l_fin_inf = decrement(l_fin_sup)
        ptr_hf = ptr_hf + ld8a.STEP

    ############
    # Compute elements of: rri2i4[], rri1i3[], rri0i2[], rri1i4[], rri0i3
    ############

    ptr_hd = 0                  # index to variable h
    ptr_hf = ptr_hd + 2
    l_fin_sup = ld8a.MSIZE - 1
    l_fin_inf = l_fin_sup - 1

    for k in range(0, ld8a.NB_POS):
        p4 = rri2i4 + l_fin_sup
        p3 = rri1i3 + l_fin_sup
        p2 = rri0i2 + l_fin_sup
        p1 = rri1i4 + l_fin_inf
        p0 = rri0i3 + l_fin_inf

        cor = 0
        ptr_h1 = ptr_hd
        ptr_h2 = ptr_hf
        for i in range(k + 1, i < ld8a.NB_POS):
            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p4] = basic_op.extract_h(cor)

            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p3] = basic_op.extract_h(cor)

            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p2] = basic_op.extract_h(cor)

            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p1] = basic_op.extract_h(cor)

            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p0] = basic_op.extract_h(cor)

            p4 = p4 - ldec
            p3 = p3 - ldec
            p2 = p2 - ldec
            p1 = p1 - ldec
            p0 = p0 - ldec

        cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
        ptr_h1 = increment(ptr_h1)
        ptr_h2 = increment(ptr_h2)
        rr[p4] = basic_op.extract_h(cor)

        cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
        ptr_h1 = increment(ptr_h1)
        ptr_h2 = increment(ptr_h2)
        rr[p3] = basic_op.extract_h(cor)

        cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
        ptr_h1 = increment(ptr_h1)
        ptr_h2 = increment(ptr_h2)
        rr[p2] = basic_op.extract_h(cor)

        l_fin_sup = l_fin_sup - ld8a.NB_POS
        l_fin_inf = decrement(l_fin_inf)
        ptr_hf = ptr_hf + ld8a.STEP

    ############
    # Compute elements of: rri1i4[], rri0i3[], rri2i4[], rri1i3[], rri0i2
    ############

    ptr_hd = 0                  # index to variable h
    ptr_hf = ptr_hd + 3
    l_fin_sup = ld8a.MSIZE - 1
    l_fin_inf = l_fin_sup - 1

    for k in range(0, ld8a.NB_POS):
        p4 = rri1i4 + l_fin_sup
        p3 = rri0i3 + l_fin_sup
        p2 = rri2i4 + l_fin_inf
        p1 = rri1i3 + l_fin_inf
        p0 = rri0i2 + l_fin_inf

        ptr_h1 = ptr_hd
        ptr_h2 = ptr_hf
        cor = 0

        for i in range(k+1, ld8a.NB_POS):
            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p4] = basic_op.extract_h(cor)

            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p3] = basic_op.extract_h(cor)

            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p2] = basic_op.extract_h(cor)

            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p1] = basic_op.extract_h(cor)

            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p0] = basic_op.extract_h(cor)

            p4 = p4 - ldec
            p3 = p3 - ldec
            p2 = p2 - ldec
            p1 = p1 - ldec
            p0 = p0 - ldec

        cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
        ptr_h1 = increment(ptr_h1)
        ptr_h2 = increment(ptr_h2)
        rr[p4] = basic_op.extract_h(cor)

        cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
        ptr_h1 = increment(ptr_h1)
        ptr_h2 = increment(ptr_h2)
        rr[p3] = basic_op.extract_h(cor)

        l_fin_sup = l_fin_sup - NB_POS
        l_fin_inf = decrement(l_fin_inf)
        ptr_hf = ptr_hf + STEP

    ############
    # Compute elements of: rri0i4[], rri2i3[], rri1i2[], rri0i1[]
    ############

    ptr_hd = 0
    ptr_hf = ptr_hd + 4
    l_fin_sup = ld8a.MSIZE - 1
    l_fin_inf = l_fin_sup - 1

    for k in range(0, ld8a.NB_POS):
        p3 = rri0i4 + l_fin_sup
        p2 = rri2i3 + l_fin_inf
        p1 = rri1i2 + l_fin_inf
        p0 = rri0i1 + l_fin_inf

        ptr_h1 = ptr_hd
        ptr_h2 = ptr_hf
        cor = 0

        for i in range(k + 1, ld8a.NB_POS):
            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p3] = basic_op.extract_h(cor)

            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p2] = basic_op.extract_h(cor)

            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p1] = basic_op.extract_h(cor)

            cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
            ptr_h1 = increment(ptr_h1)
            ptr_h2 = increment(ptr_h2)
            rr[p0] = basic_op.extract_h(cor)

            p3 = p3 - ldec
            p2 = p2 - ldec
            p1 = p1 - ldec
            p0 = p0 - ldec

        cor = basic_op.L_mac(cor, h[ptr_h1], h[ptr_h2])
        ptr_h1 = increment(ptr_h1)
        ptr_h2 = increment(ptr_h2)
        rr[p3] = basic_op.extract_h(cor)

        l_fin_sup = l_fin_sup - NB_POS
        l_fin_inf = decrement(l_fin_inf)
        ptr_hf = ptr_hf + STEP


def D4i40_17_fast(
    dn: List[int],          # (i)    : Correlations between h[] and Xn[].
    rr: List[int],          # (i)    : Correlations of impulse response h[].
    h: List[int],           # (i) Q12: Impulse response of filters.
    cod: List[int],         # (o) Q13: Selected algebraic codeword.
    y: List[int],           # (o) Q12: Filtered algebraic codeword.
    sign: int               # (o): Signs of 4 pulses.
):
    # (o) : Index of pulses positions.

    return 1

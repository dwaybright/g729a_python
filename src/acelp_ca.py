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
) -> None:
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
) -> int:
    # https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/ACELP_CA.C#L425

    sign_dn = [0] * ld8a.L_SUBFR
    sign_dn_inv = [0] * ld8a.L_SUBFR
    tmp_vect = [0] * ld8a.NB_POS

    # Init pointers to variable rr
    rri0i0 = 0
    rri1i1 = rri0i0 + ld8a.NB_POS
    rri2i2 = rri1i1 + ld8a.NB_POS
    rri3i3 = rri2i2 + ld8a.NB_POS
    rri4i4 = rri3i3 + ld8a.NB_POS
    rri0i1 = rri4i4 + ld8a.NB_POS
    rri0i2 = rri0i1 + ld8a.MSIZE
    rri0i3 = rri0i2 + ld8a.MSIZE
    rri0i4 = rri0i3 + ld8a.MSIZE
    rri1i2 = rri0i4 + ld8a.MSIZE
    rri1i3 = rri1i2 + ld8a.MSIZE
    rri1i4 = rri1i3 + ld8a.MSIZE
    rri2i3 = rri1i4 + ld8a.MSIZE
    rri2i4 = rri2i3 + ld8a.MSIZE

    ############
    # Chose the sign of the impulse.
    ############

    for i in range(0, ld8a.L_SUBFR):
        if dn[i] >= 0:
            sign_dn[i] = basic_op.MAX_INT_16
            sign_dn_inv[i] = basic_op.MIN_INT_16
        else:
            sign_dn[i] = basic_op.MIN_INT_16
            sign_dn_inv[i] = basic_op.MAX_INT_16
            dn[i] = basic_op.negate(dn[i])

    ############
    # Modification of rrixiy[] to take signs into account.
    ############

    p0 = rri0i1
    p1 = rri0i2
    p2 = rri0i3
    p3 = rri0i4

    for i0 in range(0, ld8a.L_SUBFR, ld8a.STEP):
        psign = 0
        target = sign_dn

        if sign_dn[psign + i0] < 0:
            target = sign_dn_inv       # index to sign_dn_inv

        for i1 in range(1, ld8a.L_SUBFR, ld8a.STEP):
            rr[p0] = basic_op.mult(rr[p0], target[psign + i1])
            p0 = increment(p0)

            rr[p1] = basic_op.mult(rr[p1], target[psign + i1 + 1])
            p1 = increment(p1)

            rr[p2] = basic_op.mult(rr[p2], target[psign + i1 + 2])
            p2 = increment(p2)

            rr[p3] = basic_op.mult(rr[p3], target[psign + i1 + 3])
            p3 = increment(p3)

    p0 = rri1i2
    p1 = rri1i3
    p2 = rri1i4

    for i1 in range(1, ld8a.L_SUBFR, ld8a.STEP):
        psign = 0
        target = sign_dn

        if sign_dn[psign + i1] < 0:
            target = sign_dn_inv       # index to sign_dn_inv

        for i2 in range(2, ld8a.L_SUBFR, ld8a.STEP):
            rr[p0] = basic_op.mult(rr[p0], target[psign + i2])
            p0 = increment(p0)

            rr[p1] = basic_op.mult(rr[p1], target[psign + i2 + 1])
            p1 = increment(p1)

            rr[p2] = basic_op.mult(rr[p2], target[psign + i2 + 2])
            p2 = increment(p2)

    p0 = rri2i3
    p1 = rri2i4

    for i2 in range(2, ld8a.L_SUBFR, ld8a.STEP):
        psign = 0
        target = sign_dn

        if sign_dn[psign + i2] < 0:
            target = sign_dn_inv       # index to sign_dn_inv

        for i3 in range(3, ld8a.L_SUBFR, ld8a.STEP):
            rr[p0] = basic_op.mult(rr[p0], target[psign + i3])
            p0 = increment(p0)

            rr[p1] = basic_op.mult(rr[p1], target[psign + i3 + 1])
            p1 = increment(p1)

    ############
    # Search the optimum positions of the four pulses which maximize 'square(correlation) / energy'
    ############

    psk = -1
    alpk = 1

    ptr_rri0i3_i4 = rri0i3
    ptr_rri1i3_i4 = rri1i3
    ptr_rri2i3_i4 = rri2i3
    ptr_rri3i3_i4 = rri3i3

    ip0 = 0
    ip1 = 1
    ip2 = 2
    ip3 = 3
    ix = 0
    iy = 0
    ps = 0

    trk = 0
    for track in range(3, 5):
        sq = -1
        alp = 1

        # i0 loop: 2 positions in track 2
        prev_i0 = -1

        for i in range(0, 2):
            max = -1

            # search "dn[]" maximum position in track 2
            for j in range(2, ld8a.L_SUBFR, ld8a.STEP):
                arg1 = basic_op.sub(dn[j], max)
                arg2 = basic_op.sub(prev_i0, j)

                if arg1 > 0 and arg2 != 0:
                    max = dn[j]
                    i0 = j
            prev_i0 = i0

            j = basic_op.mult(i0, 6554)
            p0 = rri2i2 + j

            ps1 = dn[i0]
            alp1 = basic_op.L_mult(rr[p0], _1_4)

            # i1 loop: 8 positions in track 2
            p0 = ptr_rri2i3_i4 + basic_op.shl(j, 3)
            p1 = ptr_rri3i3_i4

            for i1 in range(track, ld8a.L_SUBFR, ld8a.STEP):
                ps2 = basic_op.add(ps1, dn[i1])

                alp2 = basic_op.L_mac(alp1, rr[p0], _1_2)
                increment(p0)
                alp2 = basic_op.L_mac(alp2, rr[p1], _1_4)
                increment(p1)

                sq2 = basic_op.mult(ps2, ps2)
                alp_16 = basic_op.round(alp2)

                s = basic_op.L_msu(basic_op.L_mult(alp, sq2), sq, alp_16)
                if s > 0:
                    sq = sq2
                    ps = ps2
                    alp = alp_16
                    ix = i0
                    iy = i1

        i0 = ix
        i1 = iy
        i1_offset = basic_op.shl(basic_op.mult(i1, 6554), 3)

        ############
        # depth first search 3, phase B: track 0 and 1 (line 628)
        ############

        ps0 = ps
        alp0 = basic_op.L_mult(alp, _1_4)

        sq = -1
        alp = -1

        # build vector for next loop to decrease complexity
        p0 = rri1i2 + basic_op.mult(i0, 6554)
        p1 = ptr_rri1i3_i4 + basic_op.mult(i1, 6554)
        p2 = rri1i1
        p3 = 0  # index for tmp_vect

        for i3 in range(1, ld8a.L_SUBFR, ld8a.STEP):
            # rrv[i3] = rr[i3][i3] + rr[i0][i3] + rr[i1][i3]
            s = basic_op.L_mult(rr[p0], _1_4)
            p0 = p0 + ld8a.NB_POS
            s = basic_op.L_mac(s, rr[p1], _1_4)
            p1 = p1 + ld8a.NB_POS
            s = basic_op.L_mac(s, rr[p2], _1_8)
            p2 = increment(p2)
            tmp_vect[p3] = basic_op.round(s)
            p3 = increment(p3)

        # i2 loop: 8 positions in track 0

        p0 = rri0i2 + basic_op.mult(i0, 6554)
        p1 = ptr_rri0i3_i4 + basic_op.mult(i1, 6554)
        p2 = rri0i0
        p3 = rri0i1

        for i2 in range(0, ld8a.L_SUBFR, ld8a.STEP):
            ps1 = basic_op.add(ps0, dn[i2])

            # alp1 = alp0 + rr[i0][i2] + rr[i1][i2] + 1/2*rr[i2][i2]
            alp1 = basic_op.L_mac(alp0, rr[p0], _1_8)
            p0 = p0 + ld8a.NB_POS
            alp1 = basic_op.L_mac(alp1, rr[p1], _1_8)
            p1 = p1 + ld8a.NB_POS
            alp1 = basic_op.L_mac(alp1, rr[p2], _1_16)
            p2 = increment(p2)

            # i3 loop: 8 positions in track 1

            p4 = 0  # index to tmp_vect

            for i3 in range(1, ld8a.L_SUBFR, ld8a.STEP):
                ps2 = basic_op.add(ps1, dn[i3])

                # alp1 = alp0 + rr[i0][i3] + rr[i1][i3] + rr[i2][i3] + 1/2*rr[i3][i3]
                alp2 = basic_op.L_mac(alp1, rr[p3], _1_8)
                p3 = increment(p3)
                alp2 = basic_op.L_mac(alp2, tmp_vect[p4], _1_2)

                sq2 = basic_op.mult(ps2, ps2)
                alp_16 = basic_op.round(alp2)

                s = basic_op.L_msu(basic_op.L_mult(alp, sq2), sq, alp_16)

                if s > 0:
                    sq = sq2
                    alp = alp_16
                    ix = i2
                    i7 = i3

        ############
        # depth first search 3: compare codevector with the best case. (line 696)
        ############

        s = basic_op.L_msu(basic_op.L_mult(alpk, sq), psk, alp)

        if s > 0:
            psk = sq
            alpk = slp
            ip2 = i0
            ip3 = i1
            ip0 = ix
            ip1 = iy

        ############
        # depth first search 4, phase A: track 3 and 0. (line 711)
        ############

        sq = -1
        alp = 1

        # i0 loop: 2 positions in track 3/4

        prev_i0 = -1

        for i in range(0, 2):
            max = -1

            # search "dn[]" maximum position in track 3/4

            for j in range(track, ld8a.L_SUBFR, ld81.STEP):
                arg1 = basic_op.sub(dn[j], max)
                arg2 = basic_op.sub(prev_i0, j)

                if arg1 > 0 and arg2 != 0:
                    max = dn[j]
                    i0 = j

            prev_i0 = i0

            j = basic_op.mult(i0, 6554)  # j = i0/5
            p0 = ptr_rri3i3_i4 + j

            ps1 = dn[i0]
            alp1 = basic_op.L_mult(rr[p0], _1_4)

            # i1 loop: 8 positions in track 0

            p0 = ptr_rri0i3_i4 + j
            p1 = rri0i0

            for i1 in range(0, ld8a.L_SUBFR, ld8a.STEP):
                ps2 = basic_op.add(ps1, dn[i1])

                # alp1 = alp0 + rr[i0][i1] + 1/2*rr[i1][i1]
                alp2 = basic_op.L_mac(alp1, rr[p0], _1_2)
                p0 = p0 + ld8a.NB_POS
                alp2 = basic_op.L_mac(alp2, rr[p1], _1_4)
                p1 = increment(p1)

                sq2 = basic_op.mult(ps2, ps2)
                alp_16 = basic_op.round(alp2)

                s = basic_op.L_msu(basic_op.L_mult(alp, sq2), sq, alp_16)

                if s > 0:
                    sq = sq2
                    ps = ps2
                    alp = alp_16
                    ix = i0
                    iy = i1

        i0 = ix
        i1 = iy
        i1_offset = basic_op.shl(basic_op.mult(i1, 6554), 3)

        ############
        # depth first search 4, phase B: track 1 and 2.
        ############

        ps0 = ps
        alp0 = basic_op.L_mult(alp, _1_4)

        sq = -1
        alp = 1

        p0 = ptr_rri2i3_i4 + basic_op.mult(i0, 6554)
        p1 = rri0i2 + i1_offset
        p2 = rri2i2
        p3 = 0   # index for tmp_vect

        for i3 in range(2, ld8a.L_SUBFR, ld8a.STEP):
            # rrv[i3] = rr[i3][i3] + rr[i0][i3] + rr[i1][i3]
            s = basic_op.L_mult(rr[p0], _1_4)
            p0 = p0 + ld8a.NB_POS
            s = basic_op.L_mac(s, rr[p1], _1_4)
            p1 = increment(p1)
            s = basic_op.L_mac(s, rr[p2], _1_8)
            p2 = increment(p2)
            tmp_vect[p3] = basic_op.round(s)
            p3 = increment(p3)

        p0 = ptr_rri1i3_i4 + basic_op.mult(i0, 6554)
        p1 = rri0i1 + i1_offset
        p2 = rri1i1
        p3 = rri1i2

        for i2 in range(1, ld8a.L_SUBFR, ld8a.STEP):
            ps1 = basic_op.add(ps0, dn[i2])

            alp1 = basic_op.L_mac(alp0, rr[p0], _1_8)
            p0 = p0 + ld8a.NB_POS
            alp1 = basic_op.L_mac(alp1, rr[p1], _1_8)
            p1 = increment(p1)
            alp1 = basic_op.L_mac(alp1, rr[p2], _1_16)
            p2 = increment(p2)

            p4 = 0      # index to tmp_vect

            for i3 in range(2, ld8a.L_SUBFR, ld8a.STEP):
                ps2 = basic_op.add(ps2, dn[i3])

                # alp1 = alp0 + rr[i0][i3] + rr[i1][i3] + rr[i2][i3] + 1/2*rr[i3][i3]
                alp2 = basic_op.L_mac(alp1, rr[p3], _1_8)
                p3 = increment(p3)
                alp2 = basic_op.L_mac(alp2, tmp_vect[p4], _1_2)
                p4 = increment(p4)

                sq2 = basic_op.mult(ps2, ps2)
                alp_16 = basic_op.round(alp2)

                s = basic_op.L_msu(basic_op.L_mult(alp, sq2), sq, alp_16)
                if s > 0:
                    sq = sq2
                    alp = alp_16
                    ix = i2
                    iy = i3

        # depth first search 1: compare codevector with the best case

        s = basic_op.L_msu(basic_op.L_mult(alpk, sq), psk, alp)
        if s > 0:
            psk = sq
            alpk = alp
            ip3 = i0
            ip0 = i1
            ip1 = ix
            ip2 = iy

        ptr_rri0i3_i4 = rri0i4
        ptr_rri1i3_i4 = rri1i4
        ptr_rri2i3_i4 = rri2i4
        ptr_rri3i3_i4 = rri4i4

        trk = increment(trk)

    # Set the sign of impulses
    i0 = sign_dn[ip0]
    i1 = sign_dn[ip1]
    i2 = sign_dn[ip2]
    i3 = sign_dn[ip3]

    # Find the codeword corresponding to the selected positions
    for i in range(0, ld8a.L_SUBFR):
        cod[i] = 0

    cod[ip0] = basic_op.shr(i0, 2)   # From Q15 to Q13
    cod[ip1] = basic_op.shr(i1, 2)
    cod[ip2] = basic_op.shr(i2, 2)
    cod[ip3] = basic_op.shr(i3, 2)

    # find the filtered codeword
    for i in range(0, ip0):
        y[i] = 0

    if i0 > 0:
        j = 0
        for i in range(ip0, ld8a.L_SUBFR):
            y[i] = h[j]
            j = j + 1
    else:
        j = 0
        for i in range(ip0, ld8a.L_SUBFR):
            y[i] = basic_op.negate(h[j])
            j = j + 1

    if i1 > 0:
        j = 0
        for i in range(ip1, ld8a.L_SUBFR):
            y[i] = basic_op.add(y[i], h[j])
            j = j + 1
    else:
        j = 0
        for i in range(ip1, ld8a.L_SUBFR):
            y[i] = basic_op.sub(y[i], h[j])
            j = j + 1

    if i2 > 0:
        j = 0
        for i in range(ip2, ld8a.L_SUBFR):
            y[i] = basic_op.add(y[i], h[j])
            j = j + 1
    else:
        j = 0
        for i in range(ip2, ld8a.L_SUBFR):
            y[i] = basic_op.sub(y[i], h[j])
            j = j + 1

    if i3 > 0:
        j = 0
        for i in range(ip3, ld8a.L_SUBFR):
            y[i] = basic_op.add(y[i], h[j])
            j = j + 1
    else:
        j = 0
        for i in range(ip3, ld8a.L_SUBFR):
            y[i] = basic_op.sub(y[i], h[j])
            j = j + 1

    # find codebook index  17-bit address
    i = 0
    if i0 > 0:
        i = basic_op.add(i, 1)
    if i1 > 0:
        i = basic_op.add(i, 2)
    if i2 > 0:
        i = basic_op.add(i, 4)
    if i3 > 0:
        i = basic_op.add(i, 8)
    # *sign = i

    ip0 = basic_op.mult(ip0, 6554)              # ip0/5
    ip1 = basic_op.mult(ip1, 6554)              # ip1/5
    ip2 = basic_op.mult(ip2, 6554)              # ip2/5
    i = basic_op.mult(ip3, 6554)                # ip3/5
    j = basic_op.add(i, basic_op.shl(i, 2))     # j = i*5
    j = basic_op.sub(ip3, basic_op.add(j, 3))   # j= ip3%5 -3
    ip3 = basic_op.add(basic_op.shl(i, 1), j)

    i = basic_op.add(ip0, basic_op.shl(ip1, 3))
    i = basic_op.add(i, basic_op.shl(ip2, 6))
    i = basic_op.add(i, basic_op.shl(ip3, 9))

    return i

import basic_op
import ld8a
import tab_ld8a

L_exc_err = [0] * 4


def test_err(T0: int, T0_frac: int) -> int:
    #  (o) flag set to 1 if taming is necessary
    #  (i) T0 - integer part of pitch delay
    #  (i) T0_frac - fractional part of pitch delay

    if T0_frac > 0:
        t1 = basic_op.add(T0, 1)
    else:
        t1 = T0

    i = basic_op.sub(t1, (ld8a.L_SUBFR + ld8a.L_INTER10))
    if i < 0:
        i = 0

    zone1 = tab_ld8a.tab_zone[i]

    i = basic_op.add(t1, (ld8a.L_INTER10 - 2))
    zone2 = tab_ld8a.tab_zone[i]

    L_maxloc = -1
    flag = 0
    for i in range(zone, zone1 + 1, -1):
        L_acc = basic_op.L_sub(L_exc_err[i], L_maxloc)

        if L_acc > 0:
            L_maxloc = L_exc_err[i]

    L_acc = L_sub(L_maxloc, L_THRESH_ERR)
    if L_acc > 0:
        flag = 1

    return flag


def update_exc_err(gain_pit: int, T0: int) -> None:
    #  (i) pitch gain
    #  (i) integer part of pitch delay

    L_worst = -1
    n = basic_op.sub(T0, ld8a.L_SUBFR)

    if n < 0:
        hi, lo = L_Extract(L_exc_err[0], hi, lo)
        L_temp = Mpy_32_16(hi, lo, gain_pit)
        L_temp = basic_op.L_shl(L_temp, 1)
        L_temp = basic_op.L_add(basic_op.MAX_INT_14, L_temp)
        L_acc = basic_op.L_sub(L_temp, L_worst)
        if L_acc > 0:
            L_worst = L_temp

        hi, lo = L_Extract(L_temp, hi, lo)
        L_temp = Mpy_32_16(hi, lo, gain_pit)
        L_temp = basic_op.L_shl(L_temp, 1)
        L_temp = basic_op.L_add(basic_op.MAX_INT_14, L_temp)
        L_acc = basic_op.L_sub(L_temp, L_worst)
        if L_acc > 0:
            L_worst = L_temp

    else:
        zone1 = tab_ld8a.tab_zone[n]

        i = basic_op.sub(T0, 1)
        zone2 = tab_ld8a.tab_zone[i]

        for i in range(zone1, zone2 + 1):
            hi, lo = L_Extract(L_exc_err[i], hi, lo)
            L_temp = Mpy_32_16(hi, lo, gain_pit)
            L_temp = basic_op.L_shl(L_temp, 1)
            L_temp = basic_op.L_add(basic_op.MAX_INT_14, L_temp)
            L_acc = basic_op.L_sub(L_temp, L_worst)
            if L_acc > 0:
                L_worst = L_temp

    for i in range(3, 0, -1):
        L_exc_err[i] = L_exc_err[i-1]

    L_exc_err[0] = L_worst

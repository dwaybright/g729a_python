from basic_op import *
from ld8a import *
from tab_ld8a import *


L_exc_err = [0] * 4


def Init_exc_err() -> None:
    global L_exc_err

    for i in range(0, 4):
        L_exc_err[i] = MAX_INT_14       # Q14


def test_err(T0: int, T0_frac: int) -> int:
    """
    #  (o) flag set to 1 if taming is necessary
    #  (i) T0 - integer part of pitch delay
    #  (i) T0_frac - fractional part of pitch delay
    """

    if T0_frac > 0:
        t1 = add(T0, 1)
    else:
        t1 = T0

    i = sub(t1, (L_SUBFR + L_INTER10))
    if i < 0:
        i = 0

    zone1 = tab_tab_zone[i]

    i = add(t1, (L_INTER10 - 2))
    zone2 = tab_tab_zone[i]

    L_maxloc = -1
    flag = 0
    for i in range(zone, zone1 + 1, -1):
        L_acc = L_sub(L_exc_err[i], L_maxloc)

        if L_acc > 0:
            L_maxloc = L_exc_err[i]

    L_acc = L_sub(L_maxloc, L_THRESH_ERR)
    if L_acc > 0:
        flag = 1

    return flag


def update_exc_err(gain_pit: int, T0: int) -> None:
    """
    #  (i) pitch gain
    #  (i) integer part of pitch delay
    """

    L_worst = -1
    n = sub(T0, L_SUBFR)

    if n < 0:
        hi, lo = L_Extract(L_exc_err[0])
        L_temp = Mpy_32_16(hi, lo, gain_pit)
        L_temp = L_shl(L_temp, 1)
        L_temp = L_add(MAX_INT_14, L_temp)
        L_acc = L_sub(L_temp, L_worst)
        if L_acc > 0:
            L_worst = L_temp

        hi, lo = L_Extract(L_temp)
        L_temp = Mpy_32_16(hi, lo, gain_pit)
        L_temp = L_shl(L_temp, 1)
        L_temp = L_add(MAX_INT_14, L_temp)
        L_acc = L_sub(L_temp, L_worst)
        if L_acc > 0:
            L_worst = L_temp

    else:
        zone1 = tab_tab_zone[n]

        i = sub(T0, 1)
        zone2 = tab_tab_zone[i]

        for i in range(zone1, zone2 + 1):
            hi, lo = L_Extract(L_exc_err[i])
            L_temp = Mpy_32_16(hi, lo, gain_pit)
            L_temp = L_shl(L_temp, 1)
            L_temp = L_add(MAX_INT_14, L_temp)
            L_acc = L_sub(L_temp, L_worst)
            if L_acc > 0:
                L_worst = L_temp

    for i in range(3, 0, -1):
        L_exc_err[i] = L_exc_err[i-1]

    L_exc_err[0] = L_worst

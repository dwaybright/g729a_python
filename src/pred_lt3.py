import basic_op
import tab_ld8a

from typing import List

def Pred_lt_3(exc: List[int], T0: int, frac: int, L_subfr: int) -> None:
    
    x0 = exc[-T0]
    
    frac = basic_op.negate(frac)
    if frac < 0:
        frac = basic_op.add(frac, UP_SAMP)
        x0 = x0 - 1

    for j in range(0, L_subfr):
        x1 = x0
        x0 = x0 + 1
        x2 = x0
        
        c1 = tab_ld8a.inter_31[frac]
        c2 = tab_ld8a.inter_31[basic_op.sub(UP_SAMP, frac)]

        s = 0
        k = 0
        for i in range(0, L_INTER10):
            s = basic_op.L_mac(s, x1[-i], c1[k])
            s = basic_op.L_mac(s, x2[i], c2[k])

            k = k + UP_SAMP
        
        exc[j] = basic_op.round(s)

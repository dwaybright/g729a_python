from basic_op import add, sub, mult, L_add, L_sub, shr, L_shr, L_shr_r, round, shl, L_shl, extract_l, L_mult, L_msu
from oper_32b import L_Extract, Mpy_32_16
from tab_ld8a import table, slope, slope_cos, slope_acos
from ld8a import M, MP1

from typing import List


def Lsp_Az(lsp: List[int], a: List[int], aOffset: int) -> None:
    # (i) Q15 : line spectral frequencies
    # (o) Q12 : predictor coefficients (order = 10)

    f1 = [0] * 6
    f2 = [0] * 6

    Get_lsp_pol(lsp, 0 + lspIndexOffset, f1)
    Get_lsp_pol(lsp, 1 + lspIndexOffset, f2)

    for i in range(5, 0, -1):
        f1[i] = L_add(f1[i], f1[i - 1])     # f1[i] += f1[i-1]
        f2[i] = L_sub(f2[i], f2[i - 1])     # f2[i] -= f2[i-1]

    a[0 + aOffset] = 4096
    j = 10
    for i in range(1, 6):
        t0 = L_add(f1[i], f2[i])                        # f1[i] + f2[i]
        a[i] = extract_l(L_shr_r(t0, 13))               # from Q24 to Q12 and * 0.5

        t0 = L_sub(f1[i], f2[i])                        # f1[i] - f2[i]
        a[j + aOffset] = extract_l(L_shr_r(t0, 13))     # from Q24 to Q12 and * 0.5

        j = j - 1


def Get_lsp_pol(lsp: List[int], lspIndexOffset: int, f: List[int]) -> None:

    lspIndex = 0 + lspIndexOffset
    fIndex = 0

    # All computation in Q24

    f[fIndex] = L_mult(4096, 2048)              # f[0] = 1.0             in Q24
    fIndex = fIndex + 1
    f[fIndex] = L_msu(0, lsp[lspIndex], 512)    # f[1] =  -2.0 * lsp[0]  in Q24
    fIndex = fIndex + 1

    lspIndex = lspIndex + 2         # Advance lsp pointer

    for i in range(2, 6):
        f[fIndex] = f[fIndex-2]

        for j in range(1, i):
            hi, lo = L_Extract(f[fIndex-1])
            t0 = Mpy_32_16(hi, lo, lsp[lspIndex])  # t0 = f[-1] * lsp
            t0 = L_shl(t0, 1)
            f[fIndex] = L_add(*f, f[-2])           # *f += f[-2]
            f[fIndex] = L_sub(*f, t0)              # *f -= t0

            fIndex = fIndex - 1

        f[fIndex] = L_msu(f[fIndex], lsp[lspIndex], 512)   # *f -= lsp<<9
        fIndex = fIndex + i                                         # Advance f pointer
        lspIndex = lspIndex + 2                                     # Advance lsp pointer


def Lsf_lsp(lsf: List[int], lsp: List[int], m: int) -> None:
    # (i) Q15 : lsf[m] normalized (range: 0.0<=val<=0.5)
    # (o) Q15 : lsp[m] (range: -1<=val<1)
    # (i)     : LPC order

    for i in range(0, m):
        ind = shr(lsf[i], 8)       # ind    = b8-b15 of lsf[i] 
        offset = lsf[i] & 0x00ff            # offset = b0-b7  of lsf[i] 

        # lsp[i] = table[ind]+ ((table[ind+1]-table[ind])*offset) / 256 

        L_tmp = L_mult(sub(table[ind + 1], table[ind]), offset)
        lsp[i] = add(table[ind], extract_l(L_shr(L_tmp, 9)))

def Lsp_lsf(lsp: List[int], lsf: List[int], m: int) -> None:
    # (i) Q15 : lsp[m] (range: -1<=val<1)
    # (o) Q15 : lsf[m] normalized (range: 0.0<=val<=0.5)
    # (i)     : LPC order

    ind = 63 # begin at end of table -1 

    for i in range(m - 1, -1, -1):
        # find value in table that is just greater than lsp[i] 
        while sub(table[ind], lsp[i]) < 0:
            ind = sub(ind, 1)

        # acos(lsp[i])= ind*256 + ( ( lsp[i]-table[ind] ) * slope[ind] )/4096 

        L_tmp = L_mult(sub(lsp[i], table[ind]), slope[ind])
        tmp = round(L_shl(L_tmp, 3))                  #(lsp[i]-table[ind])*slope[ind])>>12
        lsf[i] = add(tmp, shl(ind, 8))


def Lsf_lsp2(lsf: List[int], lsp: List[int], m: int) -> None:
    # (i) Q13 : lsf[m] (range: 0.0<=val<PI)
    # (o) Q15 : lsp[m] (range: -1<=val<1)
    # (i)     : LPC order

    for i in range(0, m):
        #    freq = abs_s(freq)
        freq = mult(lsf[i], 20861)         # 20861: 1.0/(2.0*PI) in Q17 
        ind = shr(freq, 8)                 # ind    = b8-b15 of freq 
        offset = freq & 0x00ff                      # offset = b0-b7  of freq 

        if sub(ind, 63) > 0:
            ind = 63                                # 0 <= ind <= 63

        # lsp[i] = table2[ind]+ (slope_cos[ind]*offset >> 12) 

        L_tmp = L_mult(slope_cos[ind], offset) # L_tmp in Q28 
        lsp[i] = add(table2[ind], extract_l(L_shr(L_tmp, 13)))

def Lsp_lsf2(lsp: List[int], lsf: List[int], m: int) -> None:
    # (i) Q15 : lsp[m] (range: -1<=val<1)
    # (o) Q13 : lsf[m] (range: 0.0<=val<PI)
    # (i)     : LPC order

    ind = 63 # begin at end of table2 -1 

    for i in range(m - 1, -1, -1):
        # find value in table2 that is just greater than lsp[i] 
        while sub(table2[ind], lsp[i]) < 0:
            ind = sub(ind, 1)
            
            if ind <= 0:
                break

        offset = sub(lsp[i], table2[ind])

        # acos(lsp[i])= ind*512 + (slope_acos[ind]*offset >> 11) 

        L_tmp = L_mult(slope_acos[ind], offset) # L_tmp in Q28 
        freq = add(shl(ind, 9), extract_l(L_shr(L_tmp, 12)))
        lsf[i] = mult(freq, 25736) # 25736: 2.0*PI in Q12 


def Int_qlpc(lsp_old: List[int], lsp_new: List[int], Az: List[int]) -> None:
    # input : LSP vector of past frame
    # input : LSP vector of present frame
    # output: interpolated Az() for the 2 subframes

    lsp = [0] * M

    #  lsp[i] = lsp_new[i] * 0.5 + lsp_old[i] * 0.5 

    for i in range(0, M):
        lsp[i] = add(shr(lsp_new[i], 1), shr(lsp_old[i], 1))

    Lsp_Az(lsp, Az, 0)              # Subframe 1 

    Lsp_Az(lsp_new, Az, MP1)        # Subframe 2 

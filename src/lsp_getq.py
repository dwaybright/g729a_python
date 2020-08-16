from basic_op import add, sub, shr, L_mult, L_mac, L_msu, extract_h, L_deposit_l, L_sub
from tab_ld8a import lspcb1, lspcb2
from ld8a import M, NC, GAP1, GAP2, GAP3, MA_NP, M_LIMIT, L_LIMIT
from util import Copy

from typing import List


def Lsp_get_quant(
    lspcb1: List[List[int]], lspcb2: List[List[int]], code0, code1, code2, 
    fg: List[List[int]], freq_prev: List[List[int]], lspq: List[int], fg_sum: List[int]
) -> None:
    """
    # (i) Q13 : first stage LSP codebook
    # (i) Q13 : Second stage LSP codebook
    # (i)     : selected code of first stage
    # (i)     : selected code of second stage
    # (i)     : selected code of second stage
    # (i) Q15 : MA prediction coef.
    # (i) Q13 : previous LSP vector
    # (o) Q13 : quantized LSP parameters
    # (i) Q15 : present MA prediction coef.
    """

    buf = [0] * M           # Q13

    for j in range(0, NC):
        buf[j] = add( lspcb1[code0][j], lspcb2[code1][j] )

    for j in range(NC, M):
        buf[j] = add( lspcb1[code0][j], lspcb2[code2][j] )

    Lsp_expand_1_2(buf, GAP1)
    Lsp_expand_1_2(buf, GAP2)

    Lsp_prev_compose(buf, lspq, fg, freq_prev, fg_sum)

    Lsp_prev_update(buf, freq_prev)

    Lsp_stability( lspq )


def Lsp_expand_1(buf: List[int], gap) -> None:
    """
    # (i/o) Q13 : LSP vectors
    # (i)   Q13 : gap
    """

    for j in range(1, NC):
        diff = sub( buf[j-1], buf[j] )
        tmp = shr( add( diff, gap), 1 )

        if tmp >  0:
            buf[j-1] = sub( buf[j-1], tmp )
            buf[j]   = add( buf[j], tmp )


def Lsp_expand_2(buf: List[int], gap) -> None:
    """
    # (i/o) Q13 : LSP vectors
    # (i)   Q13 : gap
    """

    for j in range(NC, M):
        diff = sub(buf[j - 1], buf[j])
        tmp = shr(add(diff, gap), 1)

        if tmp > 0:
            buf[j - 1] = sub(buf[j - 1], tmp)
            buf[j] = add(buf[j], tmp)


def Lsp_expand_1_2(buf: List[int], gap) -> None:
    """
    # (i/o) Q13 : LSP vectors
    # (i)   Q13 : gap
    """

    for j in range(1, M):
        diff = sub(buf[j - 1], buf[j])
        tmp = shr(add(diff, gap), 1)

        if tmp > 0:
            buf[j - 1] = sub(buf[j - 1], tmp)
            buf[j] = add(buf[j], tmp)

def Lsp_prev_compose(
    lsp_ele: List[int], lsp: List[int], fg: List[List[int]], 
    freq_prev: List[List[int]], fg_sum: List[int]
) -> None:
    """
    # (i) Q13 : LSP vectors
    # (o) Q13 : quantized LSP parameters
    # (i) Q15 : MA prediction coef.
    # (i) Q13 : previous LSP vector
    # (i) Q15 : present MA prediction coef.
    """

    for j in range(0, M):
        L_acc = L_mult(lsp_ele[j], fg_sum[j])

        for k in range(0, MA_NP):
            L_acc = L_mac(L_acc, freq_prev[k][j], fg[k][j])

        lsp[j] = extract_h(L_acc)

def Lsp_prev_extract(
    lsp: List[int], lsp_ele: List[int], fg: List[List[int]], 
    freq_prev: List[List[int]], fg_sum_inv: List[int]
) -> None:
    """
    # (i) Q13 : unquantized LSP parameters
    # (o) Q13 : target vector
    # (i) Q15 : MA prediction coef.
    # (i) Q13 : previous LSP vector
    # (i) Q12 : inverse previous LSP vector
    """

    for j in range(0, M):
        L_temp = L_deposit_h(lsp[j])

        for k in range(0, MA_NP):
            L_temp = L_msu(L_temp, freq_prev[k][j], fg[k][j])

        temp = extract_h(L_temp)
        L_temp = L_mult(temp, fg_sum_inv[j])
        lsp_ele[j] = extract_h(L_shl(L_temp, 3))

def Lsp_prev_update(lsp_ele: List[int], freq_prev: List[List[int]]) -> None:
    """
    # (i)   Q13 : LSP vectors
    # (i/o) Q13 : previous LSP vectors
    """

    for k in range(MA_NP - 1, 0, -1):
        Copy(freq_prev[k - 1], freq_prev[k])

    Copy(lsp_ele, freq_prev[0])

def Lsp_stability(buf: List[int]) -> None:
    """
    # (i/o) Q13 : quantized LSP parameters
    """

    for j in range(0, M - 1):
        L_acc = L_deposit_l(buf[j + 1])
        L_accb = L_deposit_l(buf[j])
        L_diff = L_sub(L_acc, L_accb)

        if L_diff < 0:
            # exchange buf[j]<->buf[j+1]
            tmp = buf[j + 1]
            buf[j + 1] = buf[j]
            buf[j] = tmp


    if sub(buf[0], L_LIMIT) < 0:
        buf[0] = L_LIMIT
        # printf("lsp_stability warning Low \n")

    for j in range(j, M - 1):
        L_acc = L_deposit_l(buf[j + 1])
        L_accb = L_deposit_l(buf[j])
        L_diff = L_sub(L_acc, L_accb)

        if L_sub(L_diff, GAP3) < 0:
            buf[j + 1] = add(buf[j], GAP3)

    if sub(buf[M - 1], M_LIMIT) > 0:
        buf[M - 1] = M_LIMIT
        # printf("lsp_stability warning High \n")

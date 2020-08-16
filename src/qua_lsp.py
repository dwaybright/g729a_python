from basic_op import *
from ld8a import *
from tab_ld8a import *
from util import *
from lsp_getq import Lsp_prev_extract, Lsp_expand_1, Lsp_expand_2, Lsp_expand_1_2, Lsp_get_quant

from typing import List

# static memory

# Q13:previous LSP vector
freq_prev = []  # [MA_NP][M]
for i in range(ld8a.MA_NP):
    freq_prev.append([0] * ld8a.M)

# Q13:previous LSP vector(init)
freq_prev_reset = [2339, 4679, 7018, 9358, 11698, 14037,
                   16377, 18717, 21056, 23396]  # PI*(float)(j+1)/(float)(M+1)


def Qua_lsp(lsp: List[int], lsp_q: List[int], ana: List[int]) -> None:
    """
    (i) Q15 : Unquantized LSP
    (o) Q15 : Quantized LSP
    (o)     : indexes
    """

    lsf = [0] * ld8a.M
    lsf_q = [0] * ld8a.M

    # Convert LSPs to LSFs
    Lsp_lsf2(lsp, lsf, M)

    Lsp_qua_cs(lsf, lsf_q, ana)

    # Convert LSFs to LSPs
    Lsf_lsp2(lsf_q, lsp_q, M)


def Lsp_encw_reset() -> None:
    for i in range(0, ld8a.MA_NP):
        util.Copy(freq_prev_reset, freq_prev[i])


def Lsp_qua_cs(flsp_in: List[int], lspq_out: List[int], code: List[int]) -> None:
    """
    (i) flsp_in[M]  - Q13 : Original LSP parameters
    (o) lspq_out[M] - Q13 : Quantized LSP parameters
    (o) *code       -     : codes of the selected LSP
    """

    wegt = [0] * M      # Q11->normalized : weighting coefficients

    Get_wegt(flsp_in, wegt)

    Relspwed(flsp_in, wegt, lspq_out, lspcb1, lspcb2, fg,
             freq_prev, fg_sum, fg_sum_inv, code)


def Relspwed(
    lsp: List[int], wegt: List[int], lspq: List[int], lspcb1: List[[int]], lspcb2: List[[int]],
    fg: List[[[int]]], freq_prev: List[[int]], fg_sum: List[[int]], fg_sum_inv: List[[int]],
    code_ana: List[int]
) -> None:
    """
    Word16 lsp[],               # (i) Q13 : unquantized LSP parameters 
    Word16 wegt[],              # (i) norm: weighting coefficients     
    Word16 lspq[],              # (o) Q13 : quantized LSP parameters   
    Word16 lspcb1[][M],         # (i) Q13 : first stage LSP codebook   
    Word16 lspcb2[][M],         # (i) Q13 : Second stage LSP codebook  
    Word16 fg[MODE][MA_NP][M],  # (i) Q15 : MA prediction coefficients 
    Word16 freq_prev[MA_NP][M], # (i) Q13 : previous LSP vector        
    Word16 fg_sum[MODE][M],     # (i) Q15 : present MA prediction coef.
    Word16 fg_sum_inv[MODE][M], # (i) Q12 : inverse coef.              
    Word16 code_ana[]           # (o)     : codes of the selected LSP  
    """

    cand = [0] * MODE
    tindex1 = [0] * MODE
    tindex2 = [0] * MODE
    L_tdist = [0] * MODE    # Q26
    rbuf = [0] * M          # Q13
    buf = [0] * M           # Q13

    for mode in range(0, MODE):

        Lsp_prev_extract(lsp, rbuf, fg[mode], freq_prev, fg_sum_inv[mode])

        cand[mode] = Lsp_pre_select(rbuf, lspcb1)

        index = Lsp_select_1(rbuf, lspcb1[cand_cur], wegt, lspcb2)

        tindex1[mode] = index

        for j in range(0, NC):
            buf[j] = add(lspcb1[cand_cur][j], lspcb2[index][j])

        Lsp_expand_1(buf, GAP1)

        index = Lsp_select_2(rbuf, lspcb1[cand_cur], wegt, lspcb2, index)

        tindex2[mode] = index

        for j in range(NC, M):
            buf[j] = add(lspcb1[cand_cur][j], lspcb2[index][j])

        Lsp_expand_2(buf, GAP1)

        Lsp_expand_1_2(buf, GAP2)

        Lsp_get_tdist(wegt, buf, L_tdist, mode, rbuf, fg_sum[mode])

    mode_index = Lsp_last_select(L_tdist)

    code_ana[0] = shl(mode_index, NC0_B) | cand[mode_index]
    code_ana[1] = shl(tindex1[mode_index], NC1_B) | tindex2[mode_index]

    Lsp_get_quant(lspcb1, lspcb2, cand[mode_index],
                  tindex1[mode_index], tindex2[mode_index],
                  fg[mode_index], freq_prev, lspq, fg_sum[mode_index])


def Lsp_pre_select(rbuf: List[int], lspcb1: List[[int]]) -> int:
    """
    Word16 rbuf[],      # (i) Q13 : target vetor             
    Word16 lspcb1[][M], # (i) Q13 : first stage LSP codebook 
    Word16 *cand        # (o)     : selected code            
    """

    # avoid the worst case. (all over flow)

    candIndex = 0
    L_dmin = MAX_INT_32

    for i in range(0, NC0):
        L_tmp = 0

        for j in range(0, M):
            tmp = sub(rbuf[j], lspcb1[i][j])
            L_tmp = L_mac(L_tmp, tmp, tmp)

        L_temp = L_sub(L_tmp, L_dmin)

        if L_temp < 0:
            L_dmin = L_tmp
            candIndex = i

    return candIndex


def Lsp_select_1(rbuf: List[int], lspcb1: List[int], wegt: List[int], lspcb2: List[[int]]) -> int:
    """
    Word16 rbuf[],      # (i) Q13 : target vector             
    Word16 lspcb1[],    # (i) Q13 : first stage lsp codebook  
    Word16 wegt[],      # (i) norm: weighting coefficients    
    Word16 lspcb2[][M], # (i) Q13 : second stage lsp codebook 
    Word16 *index       # (o)     : selected codebook index   
    """

    buf = [0] * M

    for j in range(0, NC):
        buf[j] = sub(rbuf[j], lspcb1[j])

    # avoid the worst case. (all over flow)

    index = 0
    L_dmin = MAX_INT_32

    for k1 in range(0, NC1):
        L_dist = 0

        for j in range(0, NC):
            tmp = sub(buf[j], lspcb2[k1][j])
            tmp2 = mult(wegt[j], tmp)
            L_dist = L_mac(L_dist, tmp2, tmp)

        L_temp = L_sub(L_dist, L_dmin)

        if L_temp < 0:
            L_dmin = L_dist
            index = k1

    return index


def Lsp_select_2(rbuf: List[int], lspcb1: List[int], wegt: List[int], lspcb2: List[[int]]) -> int:
    """
    Word16 rbuf[],      # (i) Q13 : target vector             
    Word16 lspcb1[],    # (i) Q13 : first stage lsp codebook  
    Word16 wegt[],      # (i) norm: weighting coef.           
    Word16 lspcb2[][M], # (i) Q13 : second stage lsp codebook 
    Word16 *index       # (o)     : selected codebook index   
    """

    buf = [0] * M

    for j in range(NC, M):
        buf[j] = sub(rbuf[j], lspcb1[j])

    # avoid the worst case. (all over flow)
    index = 0
    L_dmin = MAX_INT_32

    for k1 in range(0, NC1):
        L_dist = 0

        for j in range(NC, M):
            tmp = sub(buf[j], lspcb2[k1][j])
            tmp2 = mult(wegt[j], tmp)
            L_dist = L_mac(L_dist, tmp2, tmp)

        L_temp = L_sub(L_dist, L_dmin)

        if L_temp < 0:
            L_dmin = L_dist
            index = k1

    return index


def Lsp_get_tdist(
    wegt: List[int], buf: List[int], L_tdist: List[int], L_tdist_index: int,
    rbuf: List[int], fg_sum: List[int]
) -> None:
    """
    Word16 wegt[],   # (i) norm: weight coef.                
    Word16 buf[],    # (i) Q13 : candidate LSP vector        
    Word32 *L_tdist, # (o) Q27 : distortion                  
    Word16 rbuf[],   # (i) Q13 : target vector               
    Word16 fg_sum[]  # (i) Q15 : present MA prediction coef. 
    """

    L_tdist[L_tdist_index] = 0

    for j in range(0, M):
        # tmp = (buf - rbuf)*fg_sum

        tmp = sub(buf[j], rbuf[j])
        tmp = mult(tmp, fg_sum[j])

        # *L_tdist += wegt * tmp * tmp

        L_acc = L_mult(wegt[j], tmp)
        tmp2 = extract_h(L_shl(L_acc, 4))
        L_tdist[L_tdist_index] = L_mac(L_tdist[L_tdist_index], tmp2, tmp)


def Lsp_last_select(L_tdist: List[int]) -> int:
    """
    Word32 L_tdist[],  # (i) Q27 : distortion         
    Word16 *mode_index # (o)     : the selected mode  
    """

    L_temp = L_sub(L_tdist[1], L_tdist[0])

    if L_temp < 0:
        return 1

    return 0


def Get_wegt(flsp: List[int], wegt: List[int]):
    """
    Word16 flsp[], # (i) Q13 : M LSP parameters  
    Word16 wegt[]  # (o) Q11->norm : M weighting coefficients 
    """

    buf = [0] * M

    buf[0] = sub(flsp[1], (PI04 + 8192))  # 8192:1.0(Q13)

    for i in range(1, M - 1):
        tmp = sub(flsp[i + 1], flsp[i - 1])
        buf[i] = sub(tmp, 8192)

    buf[M - 1] = sub((PI92 - 8192), flsp[M - 2])

    for i in range(0, M):
        if buf[i] > 0:
            wegt[i] = 2048  # 2048:1.0(Q11)
        else:
            L_acc = L_mult(buf[i], buf[i])      # L_acc in Q27
            tmp = extract_h(L_shl(L_acc, 2))    # tmp in Q13

            L_acc = L_mult(tmp, CONST10)        # L_acc in Q25
            tmp = extract_h(L_shl(L_acc, 2))    # tmp in Q11

            wegt[i] = add(tmp, 2048)            # wegt in Q11

    L_acc = L_mult(wegt[4], CONST12)            # L_acc in Q26
    wegt[4] = extract_h(L_shl(L_acc, 1))        # wegt in Q11

    L_acc = L_mult(wegt[5], CONST12)            # L_acc in Q26
    wegt[5] = extract_h(L_shl(L_acc, 1))        # wegt in Q11

    # wegt: Q11 -> normalized
    tmp = 0
    for i in range(0, M):
        if sub(wegt[i], tmp) > 0:
            tmp = wegt[i]

    sft = norm_s(tmp)
    for i in range(0, M):
        wegt[i] = shl(wegt[i], sft)             # wegt in Q(11+sft)

    return

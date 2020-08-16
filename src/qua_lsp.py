import ld8a
import tab_ld8a
import basic_op
import util

from typing import List

## static memory

# Q13:previous LSP vector
freq_prev = []  #[MA_NP][M]
for i in range(ld8a.MA_NP):
    freq_prev.append([0] * ld8a.M)

# Q13:previous LSP vector(init)
freq_prev_reset = [2339, 4679, 7018, 9358, 11698, 14037, 16377, 18717, 21056, 23396]  # PI*(float)(j+1)/(float)(M+1)


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

    Lsp_qua_cs(lsf, lsf_q, ana )

    # Convert LSFs to LSPs 
    Lsf_lsp2(lsf_q, lsp_q, M)


def Lsp_encw_reset() -> None:
    for i in range(0, ld8a.MA_NP):
        util.Copy(freq_prev_reset, freq_prev[i])


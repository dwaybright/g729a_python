import basic_op

from typing import List

def Corr_xy2(
    xn: List[int], y1: List[int], y2: List[int],           
    g_coeff: List[int], exp_g_coeff: List[int]   
) -> None:
    """
    # (i) Q0  :Target vector.
    # (i) Q0  :Adaptive codebook.# 
    # (i) Q12 :Filtered innovative vector.
    # (o) Q[exp]:Correlations between xn,y1,y2
    # (o)       :Q-format of g_coeff[]
    """

    return 1


def Cor_h_X(h: List[int], X: List[int], D: List[int]) -> None:
    """
    # (i) Q12 :Impulse response of filters
    # (i)     :Target vector
    # (o)     :Correlations between h[] and D[] 
    #          Normalized to 13 bits
    """

    return 1

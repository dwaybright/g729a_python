import basic_op

from typing import List

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/COR_FUNC.C#L27
def Corr_xy2(
    xn: List[int],           # (i) Q0  :Target vector.
    y1: List[int],           # (i) Q0  :Adaptive codebook.
    y2: List[int],           # (i) Q12 :Filtered innovative vector.
    g_coeff: List[int],      # (o) Q[exp]:Correlations between xn,y1,y2
    exp_g_coeff: List[int]   # (o)       :Q-format of g_coeff[]
) -> None:
    return 1

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/COR_FUNC.C#L93
def Cor_h_X(
    h: List[int],           # (i) Q12 :Impulse response of filters
    X: List[int],           # (i)     :Target vector
    # (o)     :Correlations between h[] and D[] Normalized to 13 bits
    D: List[int]
) -> None:
    return 1

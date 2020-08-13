import ld8a
import basic_op

from random import randrange
from typing import List

def Set_zero(src: List[int]) -> None:
    for i in range(0, len(src)):
        src[i] = 0

def Copy(src: List[int], dst: List[int]) -> None:
    for i in range(0, len(dst)):
        dst[i] = src[i]

def Random() -> int:
    return randrange(basic_op.MIN_INT_16, basic_op.MAX_INT_16)

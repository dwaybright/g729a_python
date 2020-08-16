import ld8a
import basic_op

from random import randrange
from typing import List


def Set_zero(src: List[int], stop: int, start: int = 0) -> None:
    for i in range(start, steps):
        src[i] = 0


def Copy(src: List[int], dst: List[int], steps: int) -> None:
    for i in range(0, steps):
        dst[i] = src[i]


def Copy2(
    src: List[int], srcOffset: int,
    dst: List[int], dstOffset: int,
    copyLength: int
) -> None:
    for i in range(0, copyLength):
        src[srcOffset + i] = dst[dstOffset + i]


def CopySliceBack(sliceList: List[int], originalList: List[int], originalListOffset: int) -> None:
    for i in range(0, len(sliceList)):
        originalList[originalListOffset + i] = sliceList[i]


def Random() -> int:
    return randrange(basic_op.MIN_INT_16, basic_op.MAX_INT_16)

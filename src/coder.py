from basic_op import *
from ld8a import *
from cod_ld8a import Init_Coder_ld8a, Coder_ld8a
from pre_proc import Init_Pre_Process, Pre_Process

from typing import Tuple


prm  = [0] * PRM_SIZE
serial = [0] * SERIAL_SIZE


def initialize() -> None:
    Init_Pre_Process()
    Init_Coder_ld8a()


def extractPCMToList(pcm16data: bytearray) -> List[int]:
    """
    (i) pcm16data: bytearray - PCM 16-bit data as bytearray
    (o) pcmIntData: List[int] - PCM integer data as list
    """
    pcmIntData = []
    
    for i in range(0, len(pcm16data), 2):
        word16ByteChunk = pcm16data[i:i+1]
        word16AsInt = int.from_bytes(word16ByteChunk, "little", signed=True)
        pcmIntData.append(word16AsInt)

    return pcmIntData


def convertPCMToG729a(pcm16data: bytearray) -> Tuple[bytearray, int]:
    '''
    (i)     pcm16data: bytearray - PCM 16-bit data
    (o)     Tuple[bytearray, int] - Output G729a data and frame count
    '''

    outputG729aFrameCount = len(pcm16data) / (L_FRAME * 2)
    outputG729a = []

    for i in range(0, outputG729aFrameCount):
        new_speech = extractPCMToIntList(pcm16data)

        Pre_Process(new_speech, L_FRAME)

        Coder_ld8a(prm)

        # prm2bits_ld8k( prm, serial) -> sends prm to serial

        outputG729a.extend(serial)

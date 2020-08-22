from typing import List


def convertWord16ToIntegerList(word16data: bytearray) -> List[int]:
    """
    (i) word16data: bytearray - Word16 binary data as Python bytearray
    (o) intListData: List[int] - list of Word16 values as Python integers
    """
    intListData = []
    
    for i in range(0, len(word16data), 2):
        word16ByteChunk = word16data[i:i+1]
        word16AsInt = int.from_bytes(word16ByteChunk, "little", signed=True)
        intListData.append(word16AsInt)

    return intListData


def convertIntegerListToWord16(intListData: List[int]) -> bytearray:
    """
    (i) intListData: List[int] - list of Word16 values as Python integers
    (o) word16data: bytearray - Word16 binary data as Python bytearray
    """
    word16data = bytearray()

    for i in range(0, len(intListData)):
        bytesValue = intListData[i].to_bytes(2, byteorder="little", signed=True)
        word16data.extend(bytesValue)

    return word16data

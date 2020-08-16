import basic_op

def Parity_Pitch(pitch_index: int) -> int:
    """
    #  output: parity bit (XOR of 6 MSB bits)    
    #  input : index for which parity to compute 
    """

    temp = basic_op.shr(pitch_index, 1)

    result = 1
    for i in range(0, 6):
        temp = basic_op.shr(temp, 1)
        bit = temp & 1
        result = basic_op.add(result, bit)
    
    result = result & 1

    return result

def Check_Parity_Pitch(pitch_index: int, parity: int) -> int:
    """
    #  output: 0 = no error, 1= error 
    #  input : index of parameter     
    #  input : parity bit  
    """           

    temp = basic_op.shr(pitch_index, 1)

    sum = 1
    for i in range(0, 6):
        temp = basic_op.shr(temp, 1)
        bit = temp & 1
        sum = basic_op.add(sum, bit)
    
    sum = basic_op.add(sum, parity)
    sum = sum & 1

    return sum

import basic_op
import ld8a
import tab_ld8a
import oper_32b
import dsp_func

from typing import List, Tuple

def Gain_predict(past_qua_en: List[int], code: List[int], L_subfr: int) -> Tuple[int, int]:
    """
    # (i) Q10 :Past quantized energies
    # (i) Q13 :Innovative vector.
    # (i)     :Subframe length.
    # (o) Qxx :Predicted codebook gain      - omitted param
    # (o)     :Q-Format(gcode0)             - omitted param
    """

    #Word16  i, exp, frac
    #Word32  L_tmp

    ##########
    # Energy coming from code       
    ##########

    L_tmp = 0
    for i in range (0, L_subfr):
        L_tmp = basic_op.L_mac(L_tmp, code[i], code[i])

    ##########
    #  Compute: means_ener - 10log10(ener_code/ L_sufr)               
    #  Note: mean_ener change from 36 dB to 30 dB because input/2     
    #                                                                 
    # = 30.0 - 10 log10( ener_code / lcode)  + 10log10(2^27)          
    #                                          !!ener_code in Q27!!   
    # = 30.0 - 3.0103  log2(ener_code) + 10log10(40) + 10log10(2^27) 
    # = 30.0 - 3.0103  log2(ener_code) + 16.02  + 81.278             
    # = 127.298 - 3.0103  log2(ener_code)                            
    ##########

    exp, frac = dsp_func.Log2(L_tmp, exp, frac)             # Q27->Q0 ^Q0 ^Q15       
    L_tmp = oper_32b.Mpy_32_16(exp, frac, -24660)           # Q0 Q15 Q13 -> ^Q14     
                                                            # hi:Q0+Q13+1            
                                                            # lo:Q15+Q13-15+1        
                                                            # -24660[Q13]=-3.0103    
    L_tmp = basic_op.L_mac(basic_op.L_tmp, 32588, 32)       # 32588*32[Q14]=127.298  

    ##########
    # Compute gcode0.                                                 *
    #  = Sum(i=0,3) pred[i]*past_qua_en[i] - ener_code + mean_ener    *
    ##########

    L_tmp = basic_op.L_shl(L_tmp, 10)                              # From Q14 to Q24
    for i in range(0, 4):
        L_tmp = basic_op.L_mac(L_tmp, pred[i], past_qua_en[i])     # Q13*Q10 ->Q24 

    gcode0 = basic_op.extract_h(L_tmp)                             # From Q24 to Q8  

    ##########
    # gcode0 = pow(10.0, gcode0/20)                                   *
    #        = pow(2, 3.3219*gcode0/20)                               *
    #        = pow(2, 0.166*gcode0)                                   *
    ##########

    L_tmp = basic_op.L_mult(gcode0, 5439)                   # *0.166 in Q15, result in Q24
    L_tmp = basic_op.L_shr(L_tmp, 8)                        # From Q24 to Q16             
    exp, frac = oper_32b.L_Extract(L_tmp, exp, frac)        # Extract exponent of gcode0  

    gcode0 = basic_op.extract_l(dsp_func.Pow2(14, frac))    # Put 14 as exponent so that  
                                                            # output of Pow2() will be:   
                                                            # 16768 < Pow2() <= 32767     
    exp_gcode0 = basic_op.sub(14,exp)

    return (gcode0, exp_gcode0)


def Gain_update(past_qua_en: List[int], L_gbk12: int) -> None:
    """
    # (io) Q10 :Past quantized energies
    # (i) Q13 : gbk1[indice1][1]+gbk2[indice2][1]
    """

    for i in range(3, 0, -1):
        past_qua_en[i] = past_qua_en[i-1]         # Q10
    
    ##########
    # -- past_qua_en[0] = 20*log10(gbk1[index1][1]+gbk2[index2][1]) --    
    #    2 * 10 log10( gbk1[index1][1]+gbk2[index2][1] )                  
    #  = 2 * 3.0103 log2( gbk1[index1][1]+gbk2[index2][1] )                
    #  = 2 * 3.0103 log2( gbk1[index1][1]+gbk2[index2][1] )                
    #                                                 24660:Q12(6.0205)    
    ##########

    exp, frac = dsp_func.Log2( L_gbk12, exp, frac )             # L_gbk12:Q13       
    L_acc = oper_32b.L_Comp( basic_op.sub(exp,13), frac)        # L_acc:Q16           
    tmp = basic_op.extract_h( basic_op.L_shl( L_acc,13 ) )      # tmp:Q13           
    past_qua_en[0] = basic_op.mult( tmp, 24660 )                # past_qua_en[]:Q10 


def Gain_update_erasure(past_qua_en: List[int]) -> None:
    # (i) Q10 :Past quantized energies

    L_tmp = 0                                                     # Q10
    for i in range (0, 4):
        L_tmp = basic_op.L_add( L_tmp, basic_op.L_deposit_l( past_qua_en[i] ) )
    
    av_pred_en = basic_op.extract_l( basic_op.L_shr( L_tmp, 2 ) )
    av_pred_en = basic_op.sub( av_pred_en, 4096 )                          # Q10 

    if basic_op.sub(av_pred_en, -14336) < 0:
        av_pred_en = -14336                              # 14336:14[Q10] 
    
    for i in range(3, 0, -1):
        past_qua_en[i] = past_qua_en[i-1]
    
    past_qua_en[0] = av_pred_en

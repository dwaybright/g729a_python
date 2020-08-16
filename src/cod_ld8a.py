
from basic_op import *
from util import *
from ld8a import *
from acelp_ca import ACELP_Code_A
from core_func import Corr_xy2
from filter import Syn_filt, Residu
from lpc import Autocorr, Lag_window, Levinson, Az_lsp
from lpcfunc import Weight_Az, Weight_Az_2
from pitch_a import Pitch_fr3_fast, Enc_lag3, G_pitch
from qua_gain import Qua_gain
from qua_lsp import Qua_lsp, Lsp_encw_reset
from taming import Init_exc_err, test_err, update_exc_err

from typing import List

# Speech vector
old_speech = [0] * ld8a.L_TOTAL
speech = 0          # index to old_speech
p_window = 0        # index to old_speech
new_speech = 0      # index to old_speech   # Global variable

# Weighted speech vector
old_wsp = [0] * (ld8a.L_FRAME + ld8a.PIT_MAX)
wsp = 0             # index to old_wsp

# Excitation vector
old_exc = [0] * (ld8a.L_FRAME + ld8a.PIT_MAX + ld8a.L_INTERPOL)
exc = 0             # index to old_exc

# Lsp (Line spectral pairs)
lsp_old = [30000, 26000, 21000, 15000, 8000, 0, -8000, -15000, -21000, -26000]
lsp_old_q = [0] * M

# Filter's memory
mem_w0 = [0] * M
mem_w = [0] * M
mem_zero = [0] * M
sharp = 0

def Init_Coder_ld8a() -> None:
    # https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/COD_LD8A.C#L101
    
    # Initialize indexes to old_speech list
    global new_speech
    global speech
    global p_window

    new_speech = old_speech + ld8a.L_TOTAL - ld8a.L_FRAME         # New speech     
    speech     = new_speech - ld8a.L_NEXT                         # Present frame  
    p_window   = old_speech + ld8a.L_TOTAL - ld8a.L_WINDOW        # For LPC window 

    # Initialize static pointers
    global wsp
    global exc

    wsp    = old_wsp + PIT_MAX
    exc    = old_exc + PIT_MAX + L_INTERPOL

    # Static vectors to zero
    Set_zero(old_speech, L_TOTAL)
    Set_zero(old_exc, PIT_MAX + L_INTERPOL)
    Set_zero(old_wsp, PIT_MAX)
    Set_zero(mem_w,   M)
    Set_zero(mem_w0,  M)
    Set_zero(mem_zero, M)
    sharp = ld8a.SHARPMIN

    # Initialize lsp_old_q[] 

    Copy(lsp_old, lsp_old_q)
    Lsp_encw_reset()
    Init_exc_err()


def Coder_ld8a(ana: List[int]) -> None:
    # output  : Analysis parameters

    anaIndex = 0

    # LPC analysis 

    Aq_t = [0] * (MP1 * 2)      # A(z)   quantized for the 2 subframes 
    Ap_t = [0] * (MP1 * 2)      # A(z/gamma)       for the 2 subframes     

    # Other vectors 

    h1 = [0] * L_SUBFR          # Impulse response h1[]              
    xn = [0] * L_SUBFR          # Target vector for pitch search     
    xn2 = [0] * L_SUBFR         # Target vector for codebook search  
    code = [0] * L_SUBFR        # Fixed codebook excitation          
    y1 = [0] * L_SUBFR          # Filtered adaptive excitation       
    y2 = [0] * L_SUBFR          # Filtered fixed codebook excitation 
    g_coeff = [0] * 4           # Correlations between xn & y1       

    g_coeff_cs = [0] * 5
    exp_g_coeff_cs = [0] * 5    # Correlations between xn, y1, & y2
                                #   <y1,y1>, -2<xn,y1>,
                                #       <y2,y2>, -2<xn,y2>, 2<y1,y2> 

    #------------------------------------------------------------------------*
    #  - Perform LPC analysis:                                               *
    #       * autocorrelation + lag windowing                                *
    #       * Levinson-durbin algorithm to find a[]                          *
    #       * convert a[] to lsp[]                                           *
    #       * quantize and code the LSPs                                     *
    #       * find the interpolated LSPs and convert to a[] for the 2        *
    #         subframes (both quantized and unquantized)                     *
    #------------------------------------------------------------------------

    # Temporary vectors 
    r_l = [0] * MP1         # Autocorrelations low and hi 
    r_h = [0] * MP1        
    rc = [0] * M            # Reflection coefficients.             
    lsp_new = [0] * M       # LSPs at 2th subframe      
    lsp_new_q = [0] * M           

    # LP analysis 

    Autocorr(p_window, M, r_h, r_l)        # Autocorrelations 
    Lag_window(M, r_h, r_l)                # Lag windowing    
    Levinson(r_h, r_l, Ap_t, rc)           # Levinson Durbin  
    Az_lsp(Ap_t, lsp_new, lsp_old)         # From A(z) to lsp 

    # LSP quantization 

    Qua_lsp(lsp_new, lsp_new_q, ana)
    anaIndex = anaIndex + 2                 # Advance analysis parameters pointer 

    #--------------------------------------------------------------------
    # Find interpolated LPC parameters in all subframes                  
    # The interpolated parameters are in array Aq_t[].                   
    #--------------------------------------------------------------------

    Int_qlpc(lsp_old_q, lsp_new_q, Aq_t)

    # Compute A(z/gamma) 

    result = Weight_Az_2(Aq_t, GAMMA1, M)
    CopySliceBack(result, Ap_t, 0)

    result = Weight_Az_2(Aq_t[MP1:], GAMMA1, M)
    CopySliceBack(result, Ap_t, MP1)

    # update the LSPs for the next frame 

    Copy(lsp_new,   lsp_old,   M)
    Copy(lsp_new_q, lsp_old_q, M)

    #----------------------------------------------------------------------
    # - Find the weighted input speech w_sp[] for the whole speech frame   
    # - Find the open-loop pitch delay                                     
    #----------------------------------------------------------------------

    Residu(Aq_t[0], speech[0], exc[0], L_SUBFR)

    # Residu(&Aq_t[MP1], &speech[L_SUBFR], &exc[L_SUBFR], L_SUBFR)
    slice_Aq_t = Aq_t[MP1:]                                 # Slice it
    slice_speech = speech[L_SUBFR:]
    slice_exc = exc[L_SUBFR:]
    Residu(slice_Aq_t, slice_speech, slice_exc, L_SUBFR)    # operate it
    CopySliceBack(slice_Aq_t, Aq_t, MP1)                    # recover values
    CopySliceBack(slice_speech, speech, L_SUBFR)
    CopySliceBack(slice_exc, exc, L_SUBFR)

    Ap1 = [0] * MP1
    Ap = 0          # index to Ap_t
    Ap1[0] = 4096

    for i in range(1, M + 1):       
        # Ap1[i] = Ap[i] - 0.7 * Ap[i-1]
        Ap1[i] = sub(Ap_t[Ap+i], mult(Ap_t[Ap+i-1], 22938))
    
    Syn_filt(Ap1, exc, wsp, L_SUBFR, mem_w, 1)

    Ap = Ap + MP1

    for i in range (1, M + 1):      
        # Ap1[i] = Ap[i] - 0.7 * Ap[i-1]
        Ap1[i] = sub(Ap_t[Ap+i], mult(Ap_t[Ap+i-1], 22938))
    
    slice_wsp = wsp[L_SUBFR:]
    Syn_filt(Ap1, exc[L_SUBFR:], slice_wsp, L_SUBFR, mem_w, 1)
    CopySliceBack(slice_wsp, wsp, L_SUBFR)

    # Find open loop pitch lag 

    T_op = Pitch_ol_fast(wsp, PIT_MAX, L_FRAME)

    # Range for closed loop pitch search in 1st subframe 

    T0_min = sub(T_op, 3)
    if sub(T0_min,PIT_MIN) < 0:
        T0_min = PIT_MIN

    T0_max = add(T0_min, 6)
    if sub(T0_max, PIT_MAX) > 0:
        T0_max = PIT_MAX
        T0_min = sub(T0_max, 6)

    #------------------------------------------------------------------------
    #          Loop for every subframe in the analysis frame                 
    #------------------------------------------------------------------------
    #  To find the pitch and innovation parameters. The subframe size is     
    #  L_SUBFR and the loop is repeated 2 times.                             
    #     - find the weighted LPC coefficients                               
    #     - find the LPC residual signal res[]                               
    #     - compute the target signal for pitch search                       
    #     - compute impulse response of weighted synthesis filter (h1[])     
    #     - find the closed-loop pitch parameters                            
    #     - encode the pitch delay                                           
    #     - find target vector for codebook search                           
    #     - codebook search                                                  
    #     - VQ of pitch and codebook gains                                   
    #     - update states of weighting filter                                
    #------------------------------------------------------------------------

    Aq = 0 # index to Aq_t    # pointer to interpolated quantized LPC parameters 
    Ap = 0 # index to Ap_t    # pointer to weighted LPC coefficients             

    for i_subfr in range (0, L_FRAME, L_SUBFR):
        #---------------------------------------------------------------
        # Compute impulse response, h1[], of weighted synthesis filter  
        #---------------------------------------------------------------

        h1[0] = 4096
        Set_zero(h1, L_SUBFR, start = 1)        # Set_zero(&h1[1], L_SUBFR - 1)
        slice_h1 = h1[1:]
        Syn_filt(Ap, h1, h1, L_SUBFR, slice_h1, 0)
        CopySliceBack(slice_h1, h1, 1)

        #----------------------------------------------------------------------
        #  Find the target vector for pitch search:                            
        #----------------------------------------------------------------------

        Syn_filt(Ap, exc[i_subfr:], xn, L_SUBFR, mem_w0, 0)

        #---------------------------------------------------------------------
        #                 Closed-loop fractional pitch search                 
        #---------------------------------------------------------------------

        slice_exc = exc[i_subfr:]
        T0 = Pitch_fr3_fast(
            slice_exc, xn, h1, L_SUBFR, 
            T0_min, T0_max, i_subfr, T0_frac
        )
        CopySliceBack(slice_exc, exc, i_subfr)

        index, T0_min, T0_max = Enc_lag3(T0, T0_frac, T0_min, T0_max, PIT_MIN, PIT_MAX, i_subfr)

        ana[anaIndex] = index
        anaIndex = anaIndex + 1

        if i_subfr == 0:
            ana[anaIndex] = Parity_Pitch(index)
            anaIndex = anaIndex + 1

        #-----------------------------------------------------------------
        #   - find filtered pitch exc                                     
        #   - compute pitch gain and limit between 0 and 1.2              
        #   - update target vector for codebook search                    
        #-----------------------------------------------------------------

        Syn_filt(Ap, exc[i_subfr:], y1, L_SUBFR, mem_zero, 0)

        gain_pit = G_pitch(xn, y1, g_coeff, L_SUBFR)

        # clip pitch gain if taming is necessary 

        taming = test_err(T0, T0_frac)

        if taming == 1:
            if sub(gain_pit, GPCLIP) > 0:
                gain_pit = GPCLIP

        # xn2[i]   = xn[i] - y1[i] * gain_pit  

        for i in range(0, L_SUBFR):
            L_temp = L_mult(y1[i], gain_pit)
            L_temp = L_shl(L_temp, 1)                  # gain_pit in Q14 
            xn2[i] = sub(xn[i], extract_h(L_temp))

        #-----------------------------------------------------
        # - Innovative codebook search.                       
        #-----------------------------------------------------

        index, sign = ACELP_Code_A(xn2, h1, T0, sharp, code, y2, 0)

        ana[anaIndex] = index        # Positions index
        anaIndex = anaIndex + 1
        ana[anaIndex] = i            # Signs index     
        anaIndex = anaIndex + 1

        #-----------------------------------------------------
        # - Quantization of gains.                            
        #-----------------------------------------------------

        g_coeff_cs[0]     = g_coeff[0]            # <y1,y1> 
        exp_g_coeff_cs[0] = negate(g_coeff[1])    # Q-Format:XXX -> JPN 
        g_coeff_cs[1]     = negate(g_coeff[2])    # (xn,y1) -> -2<xn,y1> 
        exp_g_coeff_cs[1] = negate(add(g_coeff[3], 1)) # Q-Format:XXX -> JPN 

        Corr_xy2( xn, y1, y2, g_coeff_cs, exp_g_coeff_cs )     # Q0 Q0 Q12 ^Qx ^Q0 
                            # g_coeff_cs[3]:exp_g_coeff_cs[3] = <y2,y2>   
                            # g_coeff_cs[4]:exp_g_coeff_cs[4] = -2<xn,y2> 
                            # g_coeff_cs[5]:exp_g_coeff_cs[5] = 2<y1,y2>  

        ana[anaIndex], gain_pit, gain_code = Qua_gain(
            code, g_coeff_cs, exp_g_coeff_cs,
            L_SUBFR, gain_pit, gain_code, taming
        )
        anaIndex = anaIndex + 1

        #------------------------------------------------------------
        # - Update pitch sharpening "sharp" with quantized gain_pit  
        #------------------------------------------------------------

        sharp = gain_pit
        if sub(sharp, SHARPMAX) > 0:
            sharp = SHARPMAX     

        if sub(sharp, SHARPMIN) < 0:
            sharp = SHARPMIN         

        #------------------------------------------------------
        # - Find the total excitation                          
        # - update filters memories for finding the target     
        #   vector in the next subframe                        
        #------------------------------------------------------

        for i in range(0, L_SUBFR):
            # exc[i] = gain_pit*exc[i] + gain_code*code[i] 
            # exc[i]  in Q0   gain_pit in Q14               
            # code[i] in Q13  gain_cod in Q1                

            L_temp = L_mult(exc[i+i_subfr], gain_pit)
            L_temp = L_mac(L_temp, code[i], gain_code)
            L_temp = L_shl(L_temp, 1)
            exc[i+i_subfr] = round(L_temp)

        update_exc_err(gain_pit, T0)

        j = 0
        for i in range(L_SUBFR-M, L_SUBFR):
            temp       = extract_h(L_shl( L_mult(y1[i], gain_pit),  1) )
            k          = extract_h(L_shl( L_mult(y2[i], gain_code), 2) )
            mem_w0[j]  = sub(xn[i], add(temp, k))
        
            j = j + 1

        Aq = Aq + MP1           # interpolated LPC parameters for next subframe 
        Ap = Ap + MP1

    #--------------------------------------------------
    # Update signal for next frame.                    
    # -> shift to the left by L_FRAME:                 
    #     speech[], wsp[] and  exc[]                   
    #--------------------------------------------------

    Copy2(old_speech, L_FRAME, old_speech, 0, (L_TOTAL-L_FRAME))    # Copy(&old_speech[L_FRAME], &old_speech[0], L_TOTAL-L_FRAME)
    Copy2(old_wsp, L_FRAME, old_wsp, 0, PIT_MAX)                    # Copy(&old_wsp[L_FRAME], &old_wsp[0], PIT_MAX)
    Copy2(old_exc, L_FRAME, old_exc, 0, (PIT_MAX+L_INTERPOL))       # Copy(&old_exc[L_FRAME], &old_exc[0], PIT_MAX+L_INTERPOL)

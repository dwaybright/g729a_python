import ld8a
import basic_op
import util
import qua_lsp
import taming

# Speech vector
old_speech = [0] * ld8a.L_TOTAL
speech = 0
p_window = 0
new_speech = 0                    # Global variable

# Weighted speech vector
old_wsp = [0] * (ld8a.L_FRAME + ld8a.PIT_MAX)
wsp = 0

# Excitation vector
old_exc = [0] * (ld8a.L_FRAME + ld8a.PIT_MAX + ld8a.L_INTERPOL)
exc = 0

# Lsp (Line spectral pairs)
lsp_old = [30000, 26000, 21000, 15000, 8000, 0, -8000, -15000, -21000, -26000]
lsp_old_q = [0] * ld8a.M

# Filter's memory
mem_w0 = [0] * ld8a.M
mem_w = [0] * ld8a.M
mem_zero = [0] * ld8a.M
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
    util.Set_zero(old_speech)
    util.Set_zero(old_exc)
    util.Set_zero(old_wsp, PIT_MAX)
    util.Set_zero(mem_w,   M)
    util.Set_zero(mem_w0,  M)
    util.Set_zero(mem_zero, M)
    sharp = ld8a.SHARPMIN

    # Initialize lsp_old_q[] 

    util.Copy(lsp_old, lsp_old_q)
    qua_lsp.Lsp_encw_reset()
    taming.Init_exc_err()

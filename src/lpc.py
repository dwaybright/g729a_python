import basic_op
import oper_32b
import ld8a
import tab_ld8a

from typing import List

old_A = [4096, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
old_rc = [0, 0]


def Autocorr(x: List[int], m: int, r_h: List[int], r_l: List[int]) -> None:
    """
    # (i)    : Input signal
    # (i)    : LPC order
    # (o)    : Autocorrelations  (msb)
    # (o)    : Autocorrelations  (lsb)
    """

    y = [0] * ld8a.L_WINDOW

    # Windowing of signal

    for i in range(0, ld8a.L_WINDOW):
        y[i] = basic_op.mult_r(x[i], tab_ld8a.hamwindow[i])

    # Compute r[0] and test for overflow
    while(basic_op.getOverflow() != 0):
        basic_op.setOverflow(0)
        sum = 1

        # Avoid case of all zeros

        for i in range(0, ld8a.L_WINDOW):
            sum = basic_op.L_mac(sum, y[i], y[i])

        # If overflow divide y[] by 4

        if basic_op.getOverflow() != 0:
            for i in range(0, ld8a.L_WINDOW):
                y[i] = basic_op.shr(y[i], 2)

    # Normalization of r[0]
    norm = basic_op.norm_l(sum)
    sum = basic_op.L_shl(sum, norm)
    r_h[0], r_l[0] = oper_32b.L_Extract(sum, r_h[0], r_l[0])

    # Put in DPF format(see oper_32b)
    # r[1] to r[m]

    for i in range(1, m + 1):
        sum = 0

        for j in range(0, ld8a.L_WINDOW - i):
            sum = basic_op.L_mac(sum, y[j], y[j + i])

        sum = basic_op.L_shl(sum, norm)
        r_h[i], r_l[i] = oper_32b.L_Extract(sum, r_h[i], r_l[i])


def Lag_window(m: int, r_h: List[int], r_l: List[int]) -> None:
    """
    # (i)     : LPC order
    # (i/o)   : Autocorrelations  (msb)
    # (i/o)   : Autocorrelations  (lsb)
    """

    for i in range(i, m + 1):
        x = oper_32b.Mpy_32(r_h[i], r_l[i], tab_ld8a.lag_h[i - 1], tab_ld8a.lag_l[i - 1])
        r_h[i], r_l[i] = oper_32b.L_Extract(x, r_h[i], r_l[i])


def Levinson(Rh: List[int], Rl: List[int], A: List[int], rc: List[int]) -> None:
    """
    # (i)     : Rh[M+1] Vector of autocorrelations (msb)
    # (i)     : Rl[M+1] Vector of autocorrelations (lsb)
    # (o) Q12 : A[M]    LPC coefficients  (m = 10)
    # (o) Q15 : rc[M]   Reflection coefficients.
    """

    # LPC coef. in double prec. 
    Ah = [0] * (M + 1)
    Al = [0] * (M + 1)

    # LPC coef.for next iteration in double prec.
    Anh = [0] * (M + 1)
    Anl = [0] * (M + 1)

    # K = A[1] = -R[1] / R[0] 

    t1 = oper_32b.L_Comp(Rh[1], Rl[1])          # R[1] in Q31      
    t2 = basic_op.L_abs(t1)                     # abs R[1]         
    t0 = oper_32b.Div_32(t2, Rh[0], Rl[0])      # R[1]/R[0] in Q31

    if t1 > 0:
        t0 = basic_op.L_negate(t0)              # -R[1]/R[0]

    Kh, Kl = oper_32b.L_Extract(t0)             # K in DPF         
    rc[0] = Kh
    t0 = basic_op.L_shr(t0, 4)                  # A[1] in Q27      
    Ah[1], Al[1] = oper_32b.L_Extract(t0)       # A[1] in DPF      

    #  Alpha = R[0] * (1-K**2) 

    t0 = oper_32b.Mpy_32(Kh, Kl, Kh, Kl)            # K*K      in Q31 
    t0 = basic_op.L_abs(t0)                         # Some case <0 !! 
    t0 = basic_op.L_sub(basic_op.MAX_INT_32, t0)    # 1 - K*K  in Q31 
    hi, lo = L_Extract(t0)                          # DPF format      
    t0 = oper_32b.Mpy_32(Rh[0], Rl[0], hi, lo)      # Alpha in Q31    

    # Normalize Alpha 

    alp_exp = basic_op.norm_l(t0)
    t0 = basic_op.L_shl(t0, alp_exp)
    alp_h, alp_l = L_Extract(t0)                    # DPF format    

    ########
    # ITERATIONS  I=2 to M
    ########

    for i in range(2, ld8a.M + 1):
        # t0 = SUM ( R[j]*A[i-j] ,j=1,i-1 ) +  R[i] 

        t0 = 0
        for j in range(1, i):
            t0 = basic_op.L_add(t0, oper_32b.Mpy_32(Rh[j], Rl[j], Ah[i - j], Al[i - j]))

        t0 = basic_op.L_shl(t0, 4)                  # result in Q27 -> convert to Q31 
                                                    # No overflow possible            
        t1 = oper_32b.L_Comp(Rh[i], Rl[i])
        t0 = basic_op.L_add(t0, t1)                 # add R[i] in Q31                 

        # K = -t0 / Alpha

        t1 = basic_op.L_abs(t0)
        t2 = oper_32b.Div_32(t1, alp_h, alp_l)      # abs(t0)/Alpha
        
        if t0 > 0:
            t2 = basic_op.L_negate(t2)              # K =-t0/Alpha                    
        t2 = basic_op.L_shl(t2, alp_exp)            # denormalize compare to Alpha   
        Kh, Kl = L_Extract(t2)                      # K in DPF                        
        rc[i - 1] = Kh

        # Test for unstable filter. If unstable keep old A(z) 

        if basic_op.sub(basic_op.abs_s(Kh), 32750) > 0:
            for j in range(0, ld8a.M + 1):
                A[j] = old_A[j]
            
            rc[0] = old_rc[0]       # only two rc coefficients are needed 
            rc[1] = old_rc[1]
            return
        

        ##########
        # Compute new LPC coeff. -> An[i]         *
        # An[j]= A[j] + K*A[i-j]     , j=1 to i-1 *
        # An[i]= K                                *
        ##########

        for j in range (1, i):
            t0 = oper_32b.Mpy_32(Kh, Kl, Ah[i - j], Al[i - j])
            t0 = basic_op.L_add(t0, oper_32b.L_Comp(Ah[j], Al[j]))
            Anh[j], Anl[j] = L_Extract(t0)
        
        t2 = basic_op.L_shr(t2, 4)              # t2 = K in Q31 ->convert to Q27  
        Anh[i], Anl[i] = L_Extract(t2)          # An[i] in Q27                    

        #  Alpha = Alpha * (1-K**2) 

        t0 = oper_32b.Mpy_32(Kh, Kl, Kh, Kl)            # K*K      in Q31 
        t0 = basic_op.L_abs(t0)                         # Some case <0 !! 
        t0 = basic_op.L_sub(basic_op.MAX_INT_32, t0)    # 1 - K*K  in Q31 
        hi, lo = L_Extract(t0)                          # DPF format      
        t0 = oper_32b.Mpy_32(alp_h, alp_l, hi, lo)      # Alpha in Q31    

        # Normalize Alpha 

        j = basic_op.norm_l(t0)
        t0 = basic_op.L_shl(t0, j)
        alp_h, alp_l = L_Extract(t0)            # DPF format    
        alp_exp = basic_op.add(alp_exp, j)      # Add normalization to alp_exp 

        # A[j] = An[j] 

        for j in range(1, i + 1):
            Ah[j] = Anh[j]
            Al[j] = Anl[j]

    # Truncate A[i] in Q27 to Q12 with rounding 

    A[0] = 4096

    for i in range(1, ld8a.M + 1):
        t0 = oper_32b.L_Comp(Ah[i], Al[i])
        old_A[i] = A[i] = basic_op.round(L_shl(t0, 1))
    
    old_rc[0] = rc[0]
    old_rc[1] = rc[1]


def Az_lsp(a: List[int], lsp: List[int], old_lsp: List[int]) -> None:
    """
    # (i) Q12 : predictor coefficients
    # (o) Q15 : line spectral pairs
    # (i)     : old lsp[] (in case not found 10 roots)
    """

    #Word16 i, j, nf, ip
    #Word16 xlow, ylow, xhigh, yhigh, xmid, ymid, xint
    #Word16 x, y, sign, exp
    #Word16 *coef
    #Word16 f1[M / 2 + 1], f2[M / 2 + 1]
    #Word32 t0, L_temp
    #Flag ovf_coef
    #Word16 (*pChebps)(Word16 x, Word16 f[], Word16 n)

    f1 = [0] * ((ld8a.M / 2) + 1)
    f2 = [0] * ((ld8a.M / 2) + 1)

    #########
    # find the sum and diff. pol. F1(z) and F2(z)                
    # F1(z) <--- F1(z)/(1+z**-1) & F2(z) <--- F2(z)/(1-z**-1)  
    # 
    # f1[0] = 1.0                                                
    # f2[0] = 1.0                                                
    # 
    # for (i = 0 i< NC i++)                                     
    # {                                                           
    #   f1[i+1] = a[i+1] + a[M-i] - f1[i]                       
    #   f2[i+1] = a[i+1] - a[M-i] + f2[i]                        
    # }                                                           
    ########

    ovf_coef = 0
    pChebps = 'Chebps_11'

    f1[0] = 2048        # f1[0] = 1.0 is in Q11 
    f2[0] = 2048        # f2[0] = 1.0 is in Q11

    for i in range(0, ld8a.NC):
        basic_op.setOverflow(0)
        t0 = basic_op.L_mult(a[i + 1], 16384)       # x = (a[i+1] + a[M-i]) >> 1        
        t0 = basic_op.L_mac(t0, a[M - i], 16384)    #    -> From Q12 to Q11             
        x = basic_op.extract_h(t0)

        if basic_op.getOverflow() != 0:
            ovf_coef = 1

        basic_op.setOverflow(0)
        f1[i + 1] = basic_op.sub(x, f1[i])          # f1[i+1] = a[i+1] + a[M-i] - f1[i]

        if basic_op.getOverflow() != 0: 
            ovf_coef = 1

        basic_op.setOverflow(0)
        t0 = basic_op.L_mult(a[i + 1], 16384)       # x = (a[i+1] - a[M-i]) >> 1        
        t0 = basic_op.L_msu(t0, a[M - i], 16384)    #    -> From Q12 to Q11             
        x = basic_op.extract_h(t0)

        if basic_op.getOverflow() != 0: 
            ovf_coef = 1

        basic_op.setOverflow(0)
        f2[i + 1] = basic_op.add(x, f2[i]) # f2[i+1] = a[i+1] - a[M-i] + f2[i] 
        
        if basic_op.getOverflow() != 0: 
            ovf_coef = 1

    if ovf_coef == 1:
        #printf("===== OVF ovf_coef =====\n")

        pChebps = 'Chebps_10'

        f1[0] = 1024                # f1[0] = 1.0 is in Q10 
        f2[0] = 1024                # f2[0] = 1.0 is in Q10 

        for i in range(0, ld8a.NC):
            t0 = basic_op.L_mult(a[i + 1], 8192)        # x = (a[i+1] + a[M-i]) >> 1        
            t0 = basic_op.L_mac(t0, a[M - i], 8192)     #    -> From Q11 to Q10             
            x = basic_op.extract_h(t0)
            f1[i + 1] = basic_op.sub(x, f1[i])          # f1[i+1] = a[i+1] + a[M-i] - f1[i] 

            t0 = basic_op.L_mult(a[i + 1], 8192)        # x = (a[i+1] - a[M-i]) >> 1        
            t0 = basic_op.L_msu(t0, a[M - i], 8192)     #    -> From Q11 to Q10             
            x = basic_op.extract_h(t0)
            f2[i + 1] = basic_op.add(x, f2[i])          # f2[i+1] = a[i+1] - a[M-i] + f2[i] 


    ########
    # find the LSPs using the Chebichev pol. evaluation
    ########

    nf = 0      # number of found frequencies 
    ip = 0      # indicator for f1 or f2      

    coef = f1   # Alias for f1 or f2

    xlow = grid[0]
    if pChebps == 'Chebps_11':
        ylow = Chebps_11(xlow, coef, NC)
    else:
        ylow = Chebps_10(xlow, coef, NC)

    j = 0
    while nf < ld81.M and j < ld8a.GRID_POINTS:
        j = basic_op.add(j, 1)
        xhigh = xlow
        yhigh = ylow
        xlow = grid[j]
        if pChebps == 'Chebps_11':
            ylow = Chebps_11(xlow, coef, ld8a.NC)
        else:
            ylow = Chebps_10(xlow, coef, ld8a.NC)

        L_temp = basic_op.L_mult(ylow, yhigh)

        if L_temp <= 0:
            # divide 2 times the interval

            for i in range(0, 2):
                xmid = basic_op.add(basic_op.shr(xlow, 1), basic_op.shr(xhigh, 1))  # xmid = (xlow + xhigh)/2 

                if pChebps == 'Chebps_11':
                    ymid = Chebps_11(xmid, coef, ld8a.NC)
                else:
                    ymid = Chebps_10(xmid, coef, ld8a.NC)

                L_temp = basic_op.L_mult(ylow, ymid)
                if L_temp <= 0:
                    yhigh = ymid
                    xhigh = xmid
                else:
                    ylow = ymid
                    xlow = xmid

            ########
            # Linear interpolation                    
            #   xint = xlow - ylow*(xhigh-xlow)/(yhigh-ylow) 
            ########

            x = basic_op.sub(xhigh, xlow)
            y = basic_op.sub(yhigh, ylow)

            if y == 0:
                xint = xlow
            else:
                sign = y
                y = basic_op.abs_s(y)
                exp = basic_op.norm_s(y)
                y = basic_op.shl(y, exp)
                y = basic_op.div_s(16383, y)
                t0 = basic_op.L_mult(x, y)
                t0 = basic_op.L_shr(t0, basic_op.sub(20, exp))
                y = basic_op.extract_l(t0)                      # y= (xhigh-xlow)/(yhigh-ylow) in Q11 

                if sign < 0:
                    y = basic_op.negate(y)

                t0 = basic_op.L_mult(ylow, y)                       # result in Q26 
                t0 = basic_op.L_shr(t0, 11)                         # result in Q15 
                xint = basic_op.sub(xlow, basic_op.extract_l(t0))   # xint = xlow - ylow*y 

            lsp[nf] = xint
            xlow = xint
            nf = basic_op.add(nf, 1)

            if ip == 0:
                ip = 1
                coef = f2
            else:
                ip = 0
                coef = f1
            
            if pChebps == 'Chebps_11':
                ylow = Chebps_11(xlow, coef, ld8a.NC)
            else:
                ylow = Chebps_10(xlow, coef, ld8a.NC)

    # Check if M roots found 

    if basic_op.sub(nf, ld8a.M) < 0:
        for i in range (0, ld8a.M):
            lsp[i] = old_lsp[i]

        # printf("\n !!Not 10 roots found in Az_lsp()!!!\n") 


def Chebps_11(x: int, f: List[int], n: int) -> int:
    # Note: All computation are done in Q24.

    b2_h = 256      # b2 = 1.0 in Q24 DPF
    b2_l = 0

    t0 = basic_op.L_mult(x, 512)            # 2*x in Q24          
    t0 = basic_op.L_mac(t0, f[1], 4096)     # + f[1] in Q24       
    b1_h, b1_l = oper_32b.L_Extract(t0)     # b1 = 2*x + f[1]     

    for i in range(2, n):
        t0 = oper_32b.Mpy_32_16(b1_h, b1_l, x)      # t0 = 2.0*x*b1              
        t0 = basic_op.L_shl(t0, 1)
        t0 = basic_op.L_mac(t0, b2_h, -32768)       # t0 = 2.0*x*b1 - b2         
        t0 = basic_op.L_msu(t0, b2_l, 1)
        t0 = basic_op.L_mac(t0, f[i], 4096)         # t0 = 2.0*x*b1 - b2 + f[i] 

        b0_h, b0_l = oper_32b.L_Extract(t0)         # b0 = 2.0*x*b1 - b2 + f[i] 

        b2_l = b1_l         # b2 = b1 
        b2_h = b1_h
        b1_l = b0_l         # b1 = b0 
        b1_h = b0_h

    t0 = oper_32b.Mpy_32_16(b1_h, b1_l, x)          # t0 = x*b1              
    t0 = basic_op.L_mac(t0, b2_h, -32768)           # t0 = x*b1 - b2          
    t0 = basic_op.L_msu(t0, b2_l, 1)
    t0 = basic_op.L_mac(t0, f[i], 2048)             # t0 = x*b1 - b2 + f[i]/2 

    t0 = basic_op.L_shl(t0, 6)                      # Q24 to Q30 with saturation 
    cheb = basic_op.extract_h(t0)                   # Result in Q14

    return cheb

def Chebps_10(x: int, f: List[int], n: int) -> int:
    # Note: All computation are done in Q23.

    b2_h = 128      # b2 = 1.0 in Q23 DPF
    b2_l = 0

    t0 = basic_op.L_mult(x, 256)            # 2*x in Q23          
    t0 = basic_op.L_mac(t0, f[1], 4096)     # + f[1] in Q23       
    b1_h, b1_l = oper_32b.L_Extract(t0)     # b1 = 2*x + f[1]     

    for i in range(2, n):
        t0 = oper_32b.Mpy_32_16(b1_h, b1_l, x)      # t0 = 2.0*x*b1              
        t0 = basic_op.L_shl(t0, 1)
        t0 = basic_op.L_mac(t0, b2_h, -32768)       # t0 = 2.0*x*b1 - b2         
        t0 = basic_op.L_msu(t0, b2_l, 1)
        t0 = basic_op.L_mac(t0, f[i], 4096)         # t0 = 2.0*x*b1 - b2 + f[i] 

        b0_h, b0_l = oper_32b.L_Extract(t0)         # b0 = 2.0*x*b1 - b2 + f[i] 

        b2_l = b1_l     # b2 = b1 
        b2_h = b1_h
        b1_l = b0_l     # b1 = b0 
        b1_h = b0_h

    t0 = oper_32b.Mpy_32_16(b1_h, b1_l, x)          # t0 = x*b1              
    t0 = basic_op.L_mac(t0, b2_h, -32768)           # t0 = x*b1 - b2          
    t0 = basic_op.L_msu(t0, b2_l, 1)
    t0 = basic_op.L_mac(t0, f[i], 2048)             # t0 = x*b1 - b2 + f[i]/2 

    t0 = basic_op.L_shl(t0, 7)                      # Q23 to Q30 with saturation 
    cheb = basic_op.extract_h(t0)

    return cheb

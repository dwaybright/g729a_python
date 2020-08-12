#####################
# Codec constant parameters (coder, decoder, and postfilter)
#####################

BIT_0 = 0x007f          # definition of zero-bit in bit-stream
BIT_1 = 0x0081          # definition of one-bit in bit-stream
SYNC_WORD = 0x6b21      # definition of frame erasure flag
SIZE_WORD = 80          # number of speech bits

#####################
# Codec constant parameters (coder, decoder, and postfilter)
#####################

L_TOTAL = 240           # Total size of speech buffer.
L_WINDOW = 240          # Window size in LP analysis.
L_NEXT = 40             # Lookahead in LP analysis.
L_FRAME = 80            # Frame size.
L_SUBFR = 40            # Subframe size.
M = 10                  # Order of LP filter.
MP1 = (M+1)             # Order of LP filter + 1
PIT_MIN = 20            # Minimum pitch lag.
PIT_MAX = 143           # Maximum pitch lag.
L_INTERPOL = (10+1)     # Length of filter for interpolation.
GAMMA1 = 24576          # Bandwitdh factor = 0.75   in Q15

PRM_SIZE = 11           # Size of vector of analysis parameters.
SERIAL_SIZE = (80+2)    # bfi+ number of speech bits

SHARPMAX = 13017        # Maximum value of pitch sharpening     0.8  Q14
SHARPMIN = 3277         # Minimum value of pitch sharpening     0.2  Q14

#####################
# LTP constant parameters
#####################

UP_SAMP = 3
L_INTER10 = 10
FIR_SIZE_SYN = (UP_SAMP * L_INTER10 + 1)

#####################
# Innovative codebook.
#####################

DIM_RR = 616            # size of correlation matrix
NB_POS = 8              # Number of positions for each pulse
STEP = 5                # Step betweem position of the same pulse.
MSIZE = 64              # Size of vectors for cross-correlation between 2 pulses

#####################
# The following constants are Q15 fractions.
# These fractions is used to keep maximum precision on "alp" sum
#####################

_1_2 = 16384
_1_4 = 8192
_1_8 = 4096
_1_16 = 2048

#####################
# LSP constant parameters
#####################

NC = 5                  # NC = M/2
MA_NP = 4               # MA prediction order for LSP
MODE = 2                # number of modes for MA prediction
NC0_B = 7               # number of first stage bits
NC1_B = 5               # number of second stage bits
NC0 = (1 << NC0_B)
NC1 = (1 << NC1_B)

L_LIMIT = 40            # Q13:0.005
M_LIMIT = 25681         # Q13:3.135

GAP1 = 10               # Q13
GAP2 = 5                # Q13
GAP3 = 321              # Q13
GRID_POINTS = 50

PI04 = 1029             # Q13  pi*0.04
PI92 = 23677            # Q13  pi*0.92
CONST10 = 10*(1 << 11)  # Q11  10.0
CONST12 = 19661         # Q14  1.2

#####################
# gain VQ constants.
#####################

NCODE1_B = 3                # number of Codebook-bit
NCODE2_B = 4                # number of Codebook-bit
NCODE1 = (1 << NCODE1_B)    # Codebook 1 size
NCODE2 = (1 << NCODE2_B)    # Codebook 2 size
NCAN1 = 4                   # Pre-selecting order for #1
NCAN2 = 8                   # Pre-selecting order for #2
INV_COEF = -17103           # Q19

#####################
# Post-filter functions.
#####################

L_H = 22                        # size of truncated impulse response of A(z/g1)/A(z/g2)

GAMMAP = 16384                  # 0.5               (Q15)
INV_GAMMAP = 21845              # 1/(1+GAMMAP)      (Q15)
GAMMAP_2 = 10923                # GAMMAP/(1+GAMMAP) (Q15)

GAMMA2_PST = 18022              # Formant postfilt factor (numerator)   0.55 Q15
GAMMA1_PST = 22938              # Formant postfilt factor (denominator) 0.70 Q15

MU = 26214                      # Factor for tilt compensation filter   0.8  Q15
AGC_FAC = 29491                 # Factor for automatic gain control     0.9  Q15
AGC_FAC1 = (32767 - AGC_FAC)    # 1-AGC_FAC in Q15

#####################
#  Constants and prototypes for taming procedure.
#####################

GPCLIP = 15564                  # Maximum pitch gain if taming is needed Q14
GPCLIP2 = 481                   # Maximum pitch gain if taming is needed Q9
GP0999 = 16383                  # Maximum pitch gain if taming is needed
L_THRESH_ERR = 983040000        # Error threshold taming 16384. * 60000.

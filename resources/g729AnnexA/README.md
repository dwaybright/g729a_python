# Copied From

Copied verbatim from https://github.com/opentelecoms-org/codecs/tree/master/g729/ITU-samples-200701/Soft/g729AnnexA

# Tweaks

1. Used VS Code to format the files

2. basic_op.c => shr(), shl(), L_shr(), L_shl()
    * Added check for var2 == MIN_16, was causing infinite loops

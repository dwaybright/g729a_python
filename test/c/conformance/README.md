# Conformance Testing

This area provides the ability to test parts of the application to see if the python code matches the C code in functionality.

## Testing Idea

The idea for the tests is to build out a python file as output, that then runs the same commands and checks if the two match.

## Build a Test

To build a test, you need to link to required objects.  Basic form is:
    ```gcc -O2 -Wall <test.c> <../path/to/first_component.o> ... <../path/to/last_component.o> -I <../path/to/header/files> -o executable```

As an example, to build the basic_ops_test.c:
    ```gcc -O2 -Wall basic_ops_test.c ../g729a_build/basic_op.o -I ../../../../resources/g729AnnexA/c_code -o test_basic_ops```

## G729AnnexA Build info

Built on Windows 10 using Cygwin
```
$ make -v
GNU Make 4.3
Built for x86_64-pc-cygwin
Copyright (C) 1988-2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

$ gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-pc-cygwin/9.3.0/lto-wrapper.exe
Target: x86_64-pc-cygwin
Configured with: /cygdrive/i/szsz/tmpp/gcc/gcc-9.3.0-2.x86_64/src/gcc-9.3.0/configure --srcdir=/cygdrive/i/szsz/tmpp/gcc/gcc-9.3.0-2.x86_64/src/gcc-9.3.0 --prefix=/usr --exec-prefix=/usr --localstatedir=/var --sysconfdir=/etc --docdir=/usr/share/doc/gcc --htmldir=/usr/share/doc/gcc/html -C --build=x86_64-pc-cygwin --host=x86_64-pc-cygwin --target=x86_64-pc-cygwin --without-libiconv-prefix --without-libintl-prefix --libexecdir=/usr/lib --enable-shared --enable-shared-libgcc --enable-static --enable-version-specific-runtime-libs --enable-bootstrap --enable-__cxa_atexit --with-dwarf2 --with-tune=generic --enable-languages=c,c++,fortran,lto,objc,obj-c++ --enable-graphite --enable-threads=posix --enable-libatomic --enable-libgomp --enable-libquadmath --enable-libquadmath-support --disable-libssp --enable-libada --disable-symvers --with-gnu-ld --with-gnu-as --with-cloog-include=/usr/include/cloog-isl --without-libiconv-prefix --without-libintl-prefix --with-system-zlib --enable-linker-build-id --with-default-libstdcxx-abi=gcc4-compatible --enable-libstdcxx-filesystem-ts
Thread model: posix
gcc version 9.3.0 (GCC)

$ make -f coder.mak
```

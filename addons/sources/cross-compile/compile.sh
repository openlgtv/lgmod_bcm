#!/bin/bash
# OpenLGTV BCM toolchain ver 0.0.6 based on LG open source toolchain
# compile.sh source compilation script
# execute this script by full path (/path/to/toolchain/compile.sh) in the sources dir
# some apps might need different arguments to configure so need to adjust them if one of these is not supported
# you'll see what's wrong in configure.out log file
# when everything compiled correctly then the installed binaries are in mipsel-linux-uclibc/target-apps/ dir
# --
# xeros

source `dirname $0`/env.sh

if [ -f "./configure" ]
then
    #./configure --prefix=${PREFIX} --build=${build_arch}-linux-gnu --host=${build_arch}-linux-gnu --enable-languages=c --with-sysroot=${SYSROOT} --with-install-prefix=${DESTDIR} $* 2>&1 | tee configure.out
    ./configure --prefix=${PREFIX} --build=${build_arch}-linux-gnu --target=${TARGET} --host=mipsel-unknown-linux-gnu --includedir=${SYSROOT}/sys-include $* 2>&1 | tee configure.out
    if [ "${PIPESTATUS[0]}" -eq "0" ]
    then
	make -j${CORES} 2>&1 | tee make.out
	if [ "${PIPESTATUS[0]}" -eq "0" ]
	then
	    echo "Now run: `dirname $0`/env.sh make install_root=${DESTDIR} install 2>&1 | tee make_install.out"
	else
	    echo "Error: compilation failed - check logs in make.out file"
	fi
    else
	echo "Error: configure failed - check logs in configure.out file"
    fi
else
    make -j${CORES} 2>&1 | tee make.out
    if [ "${PIPESTATUS[0]}" -eq "0" ]
    then
	echo "Compilation successful."
	echo "Now run: `dirname $0`/env.sh make install_root=\${DESTDIR} install 2>&1 | tee make_install.out"
	echo "To install app into ${DESTDIR}"
    else
	echo "Error: compilation failed - check logs in make.out file"
    fi
fi

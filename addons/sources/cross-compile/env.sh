#!/bin/bash
# OpenLGTV BCM toolchain scripts ver 0.0.6 based on LG open source toolchain
# env.sh script for setting environment variables, used by compile.sh source compilation script
# --
# xeros

export TARGET=mipsel-linux
export PREFIX=`dirname $0`
export CROSS_DIR=`dirname $0`
export SYSROOT=${PREFIX}/mipsel-linux
export ARCH=mips
export CROSS_COMPILE=${TARGET}-
export PATH=${CROSS_DIR}/bin:$PATH:${CROSS_DIR}/libexec/gcc/mipsel-linux-uclibc/4.2.0:${SYSROOT}/bin
export KERNEL_SRC=${CROSS_DIR}/src/stblinux-2.6.31-1.0
mkdir -p ${PREFIX}/src
export CC=${CROSS_COMPILE}gcc
export CPP="${CROSS_COMPILE}gcc -E"
export CXX=${CROSS_COMPILE}g++
export AR=${CROSS_COMPILE}ar
export RANLIB=${CROSS_COMPILE}ranlib
export AS=${CROSS_COMPILE}as
export LD=${CROSS_COMPILE}ld
export BUILD_CC=gcc
export HOSTCC=gcc
export DESTDIR=`dirname $0`/mipsel-linux-uclibc/target-apps
#export CFLAGS="-I ${CROSS_DIR}/mipsel-linux-uclibc/include -I ${CROSS_DIR}/mipsel-linux-uclibc/target-apps/usr/include -O2"
#export CPPFLAGS="-I ${CROSS_DIR}/mipsel-linux-uclibc/include -I ${CROSS_DIR}/mipsel-linux-uclibc/target-apps/usr/include -O2"
#export LDFLAGS="-L ${CROSS_DIR}/mipsel-linux-uclibc/lib -L ${CROSS_DIR}/mipsel-linux-uclibc/target-apps/lib -L ${CROSS_DIR}/mipsel-linux-uclibc/target-apps/usr/lib"
export CFLAGS="-I${CROSS_DIR}/mipsel-linux-uclibc/include -I${CROSS_DIR}/mipsel-linux-uclibc/target-apps/usr/include -O2"
export CPPFLAGS="-I${CROSS_DIR}/mipsel-linux-uclibc/include -I${CROSS_DIR}/mipsel-linux-uclibc/target-apps/usr/include -O2"
export LDFLAGS="-L${CROSS_DIR}/mipsel-linux-uclibc/lib -L${CROSS_DIR}/mipsel-linux-uclibc/target-apps/lib -L${CROSS_DIR}/mipsel-linux-uclibc/target-apps/usr/lib"
export build_arch=`uname -m`
export cross_compiling=yes
export PLATFORM=BCM
export CORES=$(grep ^processor /proc/cpuinfo | wc -l)
#export PREFIX=/usr

if [ "${1:0:1}" != "-" ]
then
    if [ "${1}" = "CC" ]
    then
	cmdline="$*"
	"$CC" ${cmdline:2}
    else
	$*
    fi
fi

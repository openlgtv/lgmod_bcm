#!/bin/bash
# mtdinfo.sh script by mmm4m5m
# adapted for OpenLGTV BCM by xeros
# Source code released under GPL License

if [ -n "$1" ]
then
    mtdinfo="$1"
else
    mtdinfo="/dev/mtd1"
fi

echo "MTDINFO:"
epkver=`hexdump $mtdinfo -vs4 -n8 -e'"%x"'`
curepkver=${epkver:0:7}
oldepkver=${epkver:7:7}
cev=${curepkver}
oev=${oldepkver}
echo "Current  EPK version: ${cev:0:1}.${cev:1:2}.${cev:3:2}.${cev:5:2}"
echo "Previous EPK version: ${oev:0:1}.${oev:1:2}.${oev:3:2}.${oev:5:2}"
hexdump $mtdinfo -vs240 -e'32 "%_p" " %08x ""%08x " 32 "%_p" " %8d"" %8x " /1 "Uu:%x" /1 " %x " /1 "CIMF:%x" /1 " %x" "\n"' | head -n 60 | grep -v "^\."

#!/bin/sh
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
#hexdump $mtdinfo -vs240 -e'32 "%_p" 2 "%08x "" " 32 "%_p" "%8d " 2 "%8x ""\n"' | head -n 60 | grep -v "^\."
hexdump $mtdinfo -vs240 -e'32 "%_p" " %08x ""%08x " 32 "%_p" " %8d"" %8x " /1 "Uu:%x" /1 " %x " /1 "CIMF:%x" /1 " %x" "\n"' | head -n 60 | grep -v "^\."

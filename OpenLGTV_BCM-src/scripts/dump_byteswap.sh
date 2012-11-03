#!/bin/sh
# dump_byteswap.sh script by xeros
# Source code released under GPL License

# this script is just for testing purpose for partition images creation from nanddump dumps

# DO NOT FLASH SUCH CONVERTED IMAGES

ifile=$1
[ ! -f "$ifile" ] && echo "ERROR: missing input file: $1" && exit 1
ofile=$ifile.byteswapped
ibs=4
size=`wc -c $ifile | cut -d' ' -f1`
nblocks=$(($size/$ibs))
rm -f $ofile
i=0
while [ "$i" -lt "$nblocks" ]
do
    dd if=$ifile ibs=$ibs skip=$i count=1 | tac -r -s '.\| ' >> $ofile
    i=$(($i+1))
done

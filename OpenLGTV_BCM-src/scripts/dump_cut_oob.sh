#!/bin/sh
# dump_cut_oob.sh script by xeros
# Source code released under GPL License

# this script is just for testing purpose for partition images creation from nanddump dumps

# DO NOT FLASH SUCH CONVERTED IMAGES

ifile=$1
ofile=$ifile.without_oob
ibs=2112
obs=2048
size=`wc -c $ifile | awk '{print $1}'`
nblocks=$(($size/$ibs))
rm -f $ofile
for i in `seq 0 $(($nblocks-1))`
do
    dd if=$ifile ibs=$ibs skip=$i count=1 | head -c $obs >> $ofile
done

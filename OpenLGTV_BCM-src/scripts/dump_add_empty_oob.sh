#!/bin/bash
# dump_add_empty_oob.sh script by xeros
# Source code released under GPL License

# this script is just for testing purpose for partition nanddump compatibile images creation from standard partition images

# DO NOT FLASH SUCH CONVERTED IMAGES

data_block_size=2048
oob_block_size=64

ifile=$1
ofile=$ifile.with_empty_oob
[ ! -f "$ifile" ] && echo "ERROR: missing input file: $1" && exit 1
ibs=$data_block_size
obs=$(($data_block_size+$oob_block_size))
size=`wc -c $ifile | cut -d' ' -f1`
nblocks=$(($size/$ibs))
[ -f "$ofile" ] && rm -f $ofile
i=0
while [ "$i" -lt "$nblocks" ]
do
    dd if=$ifile ibs=$ibs skip=$i count=1 >> $ofile
    blocks=$((${oob_block_size}/8))
    for i in `seq $blocks`
    do
	printf '\xff\xff\xff\xff\xff\xff\xff\xff' >> $ofile
    done
    i=$(($i+1))
done

#!/bin/bash
ifile=$1
ofile=$ifile.with_empty_oob
ibs=2048
obs=2112
size=`wc -c $ifile | awk '{print $1}'`
nblocks=$(($size/$ibs))
for i in `seq 0 $(($nblocks-1))`
do
    dd if=$ifile ibs=$ibs skip=$i count=1 >> $ofile
    for i in `seq 8`
    do
	printf '\xff\xff\xff\xff\xff\xff\xff\xff' >> $ofile
    done
done

#!/bin/sh
if [ "$1" != "" ]
then
    back_dir=$1
    cur_dir=`pwd`
    mkdir -p $back_dir
    cd $back_dir
    for i in `cat /proc/mtd | grep -v erasesize | awk '{print $1 "_" $4}' | sed 's/\"//g' | sed 's/://g'`
    do
	echo Making standard backup of $i ...
	cat /dev/`echo $i | sed 's/_.*//g'` > $back_dir/$i
	echo Making nanddump backup of $i ...
	nanddump -a -f $back_dir/$i.nand /dev/`echo $i | sed 's/_.*//g'`
    done
    echo Making NVRAM copy ...    
    cp -f /tmp/nvram $back_dir/
    echo Done.
    cd $cur_dir
fi

#!/bin/sh
if [ "$1" != "" ]
then
    back_dir=$1
else
    back_dir=/mnt/usb1/Drive1
fi

echo "OpenLGTV BCM-INFO: Backup script running with \"$1\" argument..."

cur_dir=`pwd`
mkdir -p $back_dir
cd $back_dir
#cat /proc/mtd | sed 's/mtd\(.\):/mtd0\1:/'
#for i in `cat /proc/mtd | grep -v erasesize | awk "BEGIN {printf \"mtd%02d_%s\", \"$1\", \"$4\"}" | sed 's/\"//g' | sed 's/://g'`
for i in `cat /proc/mtd | grep -v erasesize | awk '{print $1 "_" $4}' | sed 's/\"//g' | sed 's/mtd\(.\):/mtd0\1/'`
do
    echo "Making standard backup of $i ..."
    cat /dev/`echo $i | sed 's/_.*//g' | sed 's/mtd0/mtd/g'` > $back_dir/$i
    echo "Making nanddump backup of $i ..."
    nanddump -f $back_dir/$i.nand /dev/`echo $i | sed 's/_.*//g' | sed 's/mtd0/mtd/g'`
done
echo "Making NVRAM copy ..."
cp -f /tmp/nvram $back_dir/
echo "Backup DONE."
cd $cur_dir

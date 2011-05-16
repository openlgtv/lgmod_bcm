#!/bin/sh
# OpenLGTV BCM backup script by xeros
# Source code released under GPL License
#  $1  - backup dir
# [$2] = writable_only - make backup from writable partitions only

# Make standard dump
make_catdump=1
# Make nanddump dump (with OOB data)
make_nanddump=0
# Pack data from writable partitions to .tar.gz file
make_writable_tgz=1

if [ "$1" != "" ]
then
    back_dir=$1
else
    back_dir=/mnt/usb1/Drive1
fi

echo "OpenLGTV BCM-INFO: Backup script running with \"$1\" and \"$2\" arguments..."

cur_dir=`pwd`
mkdir -p $back_dir
cd $back_dir
if [ "$2" != "writable_only" ]
then
  #cat /proc/mtd | sed 's/mtd\(.\):/mtd0\1:/'
  #for i in `cat /proc/mtd | grep -v erasesize | awk "BEGIN {printf \"mtd%02d_%s\", \"$1\", \"$4\"}" | sed 's/\"//g' | sed 's/://g'`
  for i in `cat /proc/mtd | grep -v erasesize | awk '{print $1 "_" $4}' | sed -e 's/\"//g' -e 's/mtd\(.\):/mtd0\1/'`
  do
    if [ "$make_catdump" = "1" ]
    then
	echo "Making standard backup of $i ..."
	cat /dev/`echo $i | sed -e 's/_.*//g' -e 's/mtd0/mtd/g'` > $back_dir/$i
    fi
    if [ "$make_nanddump" = "1" ]
    then
	echo "Making nanddump backup of $i ..."
	nanddump -f $back_dir/$i.nand /dev/`echo $i | sed -e 's/_.*//g' -e 's/mtd0/mtd/g'`
    fi
  done
fi
echo "Trying to make NVRAM copy if dump exists..."
cp -f /tmp/nvram* $back_dir/ > /dev/null 2>&1
if [ "$make_writable_tgz" = "1" -o "$2" = "writable_only" ]
then
    for mount_path in `cat /proc/mounts | egrep "yaffs|jffs2" | awk '{print $2}'`
    do
	echo "Making tar.gz backup of $mount_path ..."
	tar czvf `echo $mount_path | sed -e 's#^/##g' -e 's#/#_#g'`.tar.gz $mount_path
    done
fi
echo "Backup DONE."
cd $cur_dir

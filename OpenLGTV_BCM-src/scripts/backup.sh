#!/bin/sh
# OpenLGTV BCM backup script by xeros
# Source code released under GPL License
#  $1  - backup dir
# [$2] = writable_only - make backup from writable partitions only

# Default settings:
# Make standard dump
[ -z "$make_catdump"  ] && make_catdump=1
# Make nanddump dump (with OOB data) for all partitions
[ -z "$make_nanddump" ] && make_nanddump=0
# Make nanddump dump (with OOB data) for 'total' partition
[ -z "$make_nanddump_total" ] && make_nanddump_total=1
# Pack data from writable partitions to .tar.gz file
[ -z "$make_writable_tgz"   ] && make_writable_tgz=1

[ -z "$1" ] && back_dir="$1" || back_dir="/mnt/usb1/Drive1"

echo "OpenLGTV BCM-INFO: Backup script running with \"$1\" and \"$2\" arguments..."

cur_dir=`pwd`
mkdir -p "$back_dir"
cd "$back_dir"
if [ "$2" != "writable_only" ]
then
    for i in `cat /proc/mtd | grep -v erasesize | awk '{print $1 "_" $4}' | sed -e 's/\"//g' -e 's/mtd\(.\):/mtd0\1/' -e 's/://g'`
    do
	partname=`echo $i | sed -e 's/^mtd[0-9]*_//g'`
	partno=`echo $i | sed -e 's/_.*//g' -e 's/mtd0/mtd/g'`
	[ "$partname" = "total" -a "$make_nanddump_total" = "1" ] && make_nanddump=1 && make_catdump=0
	if [ "$make_catdump" = "1" ]
	then
	    echo "Making standard backup of $i ..."
	    cat "/dev/$partno" > "$back_dir/$i"
	fi
	if [ "$make_nanddump" = "1" ]
	then
	    echo "Making nanddump backup of $i ..."
	    nanddump -f "$back_dir/$i.nand" "/dev/$partno"
	fi
    done
fi
echo "Trying to make NVRAM copy if dump exists..."
cp -f /tmp/nvram* "$back_dir/" > /dev/null 2>&1
if [ "$make_writable_tgz" = "1" -o "$2" = "writable_only" ]
then
    for mount_path in `cat /proc/mounts | egrep "yaffs|jffs2" | awk '{print $2}'`
    do
	echo "Making tar.gz backup of $mount_path ..."
	tar czvf $back_dir/`echo $mount_path | sed -e 's#^/##g' -e 's#/#_#g'`.tar.gz $mount_path
    done
fi
echo "Backup DONE."
cd "$cur_dir"

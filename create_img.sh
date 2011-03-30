#!/bin/sh
# OpenLGTV BCM rootfs image creation script by xeros
size=3145728
dir=OpenLGTV_BCM-src
ver=`cat $dir/etc/ver2`
perl -pi -e "s/^ver=.*/ver=$ver/g" install.sh
perl -pi -e "s/Welcome to OpenLGTV BCM ver.*/Welcome to OpenLGTV BCM ver\. $ver/g" $dir/etc/motd.org
cp -r $dir squashfs-root
cd squashfs-root
tar xzvf dev.tar.gz
tar xzvf etc_passwd.tar.gz
rm -f dev.tar.gz etc_passwd.tar.gz
find . -name '.svn' | xargs rm -rf
cd ..
ofile=OpenLGTV_BCM-v$ver
rm -f $ofile.sqf $ofile.md5 $ofile.zip
mksquashfs squashfs-root $ofile.sqf
osize=`wc -c $ofile.sqf | awk '{print $1}'`
if [ "$osize" -gt "$size" ]
then
    echo "ERROR: Partition image too big for flashing."
    rm -rf squashfs-root
    exit 1
else
    if [ "$osize" -lt "$size" ]
    then
	echo "Partition image size is small, adding some bytes to fill the partition up to the end."
	for i in `seq $(($size-$osize))`
	do
	    printf "\xff" >> $ofile.sqf
	done
    fi
fi
md5sum $ofile.sqf > $ofile.md5
zip $ofile.zip $ofile.sqf $ofile.md5 install.sh
rm -rf squashfs-root

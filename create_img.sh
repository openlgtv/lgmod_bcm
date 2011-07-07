#!/bin/bash
# OpenLGTV BCM rootfs image creation script by xeros
# Source code released under GPL License
size=3145728
size2011=4194304
dir=OpenLGTV_BCM-src
dir2011=OpenLGTV_BCM-2011-src
ver=`cat $dir/etc/ver2`
ofile=OpenLGTV_BCM-v$ver
ofile2011=OpenLGTV_BCM_2011-v$ver
sed -i -e "s/^ver=.*/ver=$ver/g" install.sh
cp -f install.sh $dir/scripts/
sed -i -e "s/Welcome to OpenLGTV BCM ver.*/Welcome to OpenLGTV BCM ver\. $ver/g" $dir/etc/motd.org
find $dir -type d -exec chmod 775 '{}' \;
chmod -R 755 $dir/bin/* $dir/sbin/* $dir/usr/bin/* $dir/usr/sbin/* $dir/etc/init.d/* $dir/etc/rc.d/* \
	     $dir/scripts/* $dir/var/www/ywe/*.sh \
	     $dir/var/www/*.cgi* $dir/var/www/browser/*.cgi* $dir/var/www/include/*.cgi* \
	     $dir2011/bin/* $dir2011/sbin/* $dir2011/usr/bin/* $dir2011/usr/sbin/*
rm -rf squashfs-root squashfs-root-2011
cp -r $dir squashfs-root
cd squashfs-root
tar xzvf dev.tar.gz
tar xzvf etc_passwd.tar.gz
rm -f dev.tar.gz etc_passwd.tar.gz
find . -name '.svn' | xargs rm -rf
cd ..
rm -f $ofile.sqf $ofile.md5 $ofile.sha1 $ofile.zip
mksquashfs squashfs-root $ofile.sqf
cp -r squashfs-root squashfs-root-2011
cp -r --remove-destination $dir2011/* squashfs-root-2011
cd squashfs-root-2011
tar xzvf dev-add.tar.gz
rm -f dev-add.tar.gz lib/modules/*.ko
find . -name '.svn' | xargs rm -rf
cd ..
# no modules for 2011 models compile yet, so remove the 2010 models modules
rm -f $ofile2011.sqf $ofile2011.md5 $ofile2011.sha1 $ofile2011.zip
mksquashfs squashfs-root-2011 $ofile2011.sqf
osize=`wc -c $ofile.sqf | awk '{print $1}'`
osize2011=`wc -c $ofile2011.sqf | awk '{print $1}'`
if [ "$osize" -gt "$size" ]
then
    echo "ERROR: Partition image for 2010 BCM is too big for flashing."
    #rm -rf squashfs-root
    exit 1
else
    if [ "$osize" -lt "$size" ]
    then
	abytes=$(($size-$osize))
	echo "Partition image size ( $osize ) for 2010 BCM is small, adding $abytes bytes to fill the partition up to the end ( $size )."
	for i in `seq $abytes`
	do
	    printf '\xff' >> $ofile.sqf
	done
    fi
fi
if [ "$osize2011" -gt "$size2011" ]
then
    echo "ERROR: Partition image for 2011 BCM is too big for flashing."
    #rm -rf squashfs-root-2011
    exit 1
else
    if [ "$osize2011" -lt "$size2011" ]
    then
	abytes=$(($size2011-$osize2011))
	echo "Partition image size ( $osize2011 ) for 2011 BCM is small, adding $abytes bytes to fill the partition up to the end ( $size2011 )."
	for i in `seq $abytes`
	do
	    printf '\xff' >> $ofile2011.sqf
	done
    fi
fi
sha1sum $ofile.sqf > $ofile.sha1
sha1sum $ofile2011.sqf > $ofile2011.sha1
zip $ofile.zip $ofile.sqf $ofile.sha1 install.sh
zip $ofile2011.zip $ofile2011.sqf $ofile2011.sha1 install.sh
rm -rf squashfs-root squashfs-root-2011

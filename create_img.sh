#!/bin/bash
# OpenLGTV BCM rootfs image creation script by xeros
# Source code released under GPL License

# TODO: try with bigger block size - multiple of 128KB (131072)
# for 2010 models best results with 512KB block size (256KB not a much bigger than with 512KB)
# for 2011 models best results with 1MB block size
#-rwx------ 1 root root 3125248 2011-08-07 21:50 OpenLGTV_BCM-GP2B-v0.5.0-devel1mb.sqf
#-rwx------ 1 root root 3129344 2011-08-07 21:51 OpenLGTV_BCM-GP2B-v0.5.0-devel256kb.sqf
#-rwx------ 1 root root 3125248 2011-08-07 21:50 OpenLGTV_BCM-GP2B-v0.5.0-devel512kb.sqf
#-rwx------ 1 root root 3145728 2011-08-07 21:36 OpenLGTV_BCM-GP2B-v0.5.0-devel.sqf
#-rwx------ 1 root root 4190208 2011-08-07 21:52 OpenLGTV_BCM-GP3B-v0.5.0-devel1mb.sqf
#-rwx------ 1 root root 4198400 2011-08-07 21:53 OpenLGTV_BCM-GP3B-v0.5.0-devel256kb.sqf
#-rwx------ 1 root root 4194304 2011-08-07 21:52 OpenLGTV_BCM-GP3B-v0.5.0-devel512kb.sqf
#-rwx------ 1 root root 4222976 2011-08-07 21:36 OpenLGTV_BCM-GP3B-v0.5.0-devel.sqf

size=3145728
size2011=4194304
dir=OpenLGTV_BCM-src
dir2011=OpenLGTV_BCM-2011-src
ver=`cat $dir/etc/ver2`
ofile=OpenLGTV_BCM-GP2B-v$ver
ofile2011=OpenLGTV_BCM-GP3B-v$ver
squashfs_opts="-all-root -noappend"
#squashfs_opts="-all-root -noappend -b $((256*1024))"
squashfs2011_opts="-all-root -noappend -always-use-fragments -b 1048576"
sed -i -e "s/^ver=.*/ver=$ver/g" install.sh
cp -f install.sh $dir/scripts/
sed -i -e "s/Welcome to OpenLGTV BCM ver.*/Welcome to OpenLGTV BCM ver\. $ver/g" $dir/etc/motd
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
mksquashfs squashfs-root $ofile.sqf $squashfs_opts
cp -r squashfs-root squashfs-root-2011
cp -r --remove-destination $dir2011/* squashfs-root-2011
cd squashfs-root-2011
tar xzvf dev-add.tar.gz
# no modules for 2011 models compile yet, so remove the 2010 models modules
rm -f dev-add.tar.gz lib/modules/*.ko
find . -name '.svn' | xargs rm -rf
cd ..
rm -f $ofile2011.sqf $ofile2011.md5 $ofile2011.sha1 $ofile2011.zip
mksquashfs squashfs-root-2011 $ofile2011.sqf $squashfs2011_opts
osize=`wc -c $ofile.sqf | awk '{print $1}'`
osize2011=`wc -c $ofile2011.sqf | awk '{print $1}'`
if [ "$osize" -gt "$size" ]
then
    echo "ERROR: Partition image for GP2B is too big for flashing by $(($osize-$size)) bytes."
    #rm -rf squashfs-root
    #exit 1
else
    if [ "$osize" -lt "$size" ]
    then
	abytes=$(($size-$osize))
	echo "Partition image size ( $osize ) for GP2B is small, adding $abytes bytes to fill the partition up to the end ( $size )."
	for i in `seq $abytes`
	do
	    printf '\xff' >> $ofile.sqf
	done
    fi
    echo "OpenLGTV BCM installation package for GP2B is generated"
fi
if [ "$osize2011" -gt "$size2011" ]
then
    echo "ERROR: Partition image for GP3B is too big for flashing by $(($osize2011-$size2011)) bytes."
    #rm -rf squashfs-root-2011
    #exit 1
else
    if [ "$osize2011" -lt "$size2011" ]
    then
	abytes=$(($size2011-$osize2011))
	echo "Partition image size ( $osize2011 ) for GP3B is small, adding $abytes bytes to fill the partition up to the end ( $size2011 )."
	for i in `seq $abytes`
	do
	    printf '\xff' >> $ofile2011.sqf
	done
    fi
    echo "OpenLGTV BCM installation package for GP3B is generated"
fi
sha1sum $ofile.sqf > $ofile.sha1
sha1sum $ofile2011.sqf > $ofile2011.sha1
zip $ofile.zip $ofile.sqf $ofile.sha1 install.sh
zip $ofile2011.zip $ofile2011.sqf $ofile2011.sha1 install.sh
cat extract.sh $ofile.zip > $ofile.sh.zip
cat extract.sh $ofile2011.zip > $ofile2011.sh.zip
chmod a+rx $ofile.sh.zip $ofile2011.sh.zip
rm -rf squashfs-root squashfs-root-2011

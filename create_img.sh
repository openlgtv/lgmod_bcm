#!/bin/bash
# OpenLGTV BCM rootfs image creation script by xeros
# Source code released under GPL License

size=3145728
size2011=4194304
dir=OpenLGTV_BCM-src
dir2011=OpenLGTV_BCM-2011-src
ver=`cat $dir/etc/ver2`
ofile=OpenLGTV_BCM-GP2B-v$ver
ofile2011=OpenLGTV_BCM-GP3B-v$ver
squashfs_opts="-all-root -noappend -b $((1024*1024))"
squashfs2011_opts="-all-root -noappend -always-use-fragments -b $((1024*1024))"

echo "OpenLGTV BCM installation image building script"
echo "Updating version info..."
sed -i -e "s/^ver=.*/ver=$ver/g" -e "s/OpenLGTV BCM .* installation script/OpenLGTV BCM $ver installation script/g" install.sh extract.sh
cp -f install.sh $dir/scripts/
sed -i -e "s/Welcome to OpenLGTV BCM ver.*/Welcome to OpenLGTV BCM ver\. $ver/g" $dir/etc/motd
echo "Updating file permissions..."
find $dir -type d -exec chmod 775 '{}' \;
chmod -R 755 $dir/bin $dir/sbin $dir/usr/bin $dir/usr/sbin $dir/etc/init.d $dir/etc/rc.d \
	     $dir/scripts $dir/var/www/ywe/*.sh \
	     $dir/var/www/*.cgi* $dir/var/www/browser/*.cgi* $dir/var/www/include/*.cgi* \
	     $dir2011/bin $dir2011/sbin $dir2011/usr/bin $dir2011/usr/sbin
echo "Building GP2B image..."
rm -rf squashfs-root squashfs-root-2011
cp -r $dir squashfs-root
cd squashfs-root
tar xzf dev.tar.gz
tar xzf etc_passwd.tar.gz
rm -f dev.tar.gz etc_passwd.tar.gz
find . -name '.svn' | xargs rm -rf
cp etc/openrelease/openrelease.cfg etc/default/openrelease/openrelease.cfg.default
cp etc/openrelease/openrelease_keymap.cfg etc/default/openrelease/openrelease_keymap.cfg.default
cp ../../../lgmod_s7/trunk/rootfs/home/lgmod/info.sh scripts/
cd ..
rm -f $ofile.sqf $ofile.md5 $ofile.sha1 $ofile.zip
mksquashfs squashfs-root $ofile.sqf $squashfs_opts
echo "Building GP3B image..."
cp -r squashfs-root squashfs-root-2011
cp -r --remove-destination $dir2011/* squashfs-root-2011
cd squashfs-root-2011
tar xzf dev-add.tar.gz
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
echo "Preparing extroot.tar.gz"
rm -rf extroot.tar.gz extroot
cp -r addons/extroot .
find extroot -name '.svn' | xargs rm -rf
tar czf extroot.tar.gz extroot
rm -rf extroot

echo "Updating checksums and building installation images..."
sha1sum $ofile.sqf > $ofile.sha1
sha1sum $ofile2011.sqf > $ofile2011.sha1
tar cf $ofile.tar $ofile.sqf $ofile.sha1 install.sh
tar cf $ofile2011.tar $ofile2011.sqf $ofile2011.sha1 install.sh

SKIP_LINES=$((`cat extract.sh | wc -l`+1))
sed -i -e "s/SKIP_LINES=.*/SKIP_LINES=$SKIP_LINES/g" extract.sh

cat extract.sh $ofile.tar > $ofile.tar.sh
cat extract.sh $ofile2011.tar > $ofile2011.tar.sh
chmod a+rx $ofile.tar.sh $ofile2011.tar.sh
rm -rf squashfs-root squashfs-root-2011

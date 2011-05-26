#!/bin/sh
# OpenLGTV BCM installation script v.1.3 by xeros
# Source code released under GPL License

# it needs $file.sqf and $file.sha1 files in the same dir as this script

# if 'confirmations' is set to '1' then it asks for confirmation, if '0' then autoconfirm
# if 'rebooting' is set to '1' then TV is autorebooted after after successful flashing
# if 'make_backup' is set to '1' then installer makes full backup of firmware if OpenLGTV BCM haven't been installed yet

# vars set
#confirmations=1
confirmations=0
#rebooting=0
rebooting=1
make_backup=1

# enforce variables from settings file
if [ -f "/mnt/user/cfg/settings" ]
then
    source /mnt/user/cfg/settings
fi

if [ "$2" = "autoupgrade" ]
then
    confirmations=0
    rebooting=1
    autoupgrade=1
else
    if [ "$2" = "no_backup" -o "$1" = "no_backup" ]
    then
	make_backup=0
    fi
fi

ver=0.4.0-beta3
supported_rootfs_ver="V1.00.51 Mar 01 2010"
development=1

tmp=/tmp
dir=`dirname $0`

if [ "$1" != "" -a "$1" != "no_backup" ]
then
    ver=`basename $1 | sed 's/OpenLGTV_BCM-v//' | sed 's/\.sqf//'`
    dir=`dirname $1`
fi

file=OpenLGTV_BCM-v$ver
size=3145728
mtd=3
magic=hsqs
magic_clean=377377377377
lginit=4
lginit_size=262144


cdir=$dir
#log=$dir/$file.log
log="$dir/$file.log $tmp/$file.log"
tmpout=$tmp/output.log
reqfreemem=20000

backup=pre-backup
lginit_backup=lginit-$backup
rootfs_backup=rootfs-$backup
suffix=flashed
backup2=$suffix-backup
ver_installed=`cat /etc/ver2 2>/dev/null`

mkdir -p /mnt/usb1/Drive1/OpenLGTV_BCM > /dev/null 2>&1
mkdir -p /mnt/usb2/Drive1/OpenLGTV_BCM > /dev/null 2>&1

if [ -d "/mnt/usb2/Drive1/OpenLGTV_BCM" ]
then
    export OpenLGTV_BCM_USB=/mnt/usb2/Drive1/OpenLGTV_BCM
else
    export OpenLGTV_BCM_USB=/mnt/usb1/Drive1/OpenLGTV_BCM
fi

touch $log
if [ "$?" -ne "0" ]
then
    echo "WARNING: Could not create flashing log in $dir, the partition might not be writable."
    echo "Trying to create log in $tmp/ instead..."
    echo "This will be path for current firmware /dev/mtd$mtd partition backup, too."
    dir=$tmp
    log=$dir/$file.log
    touch $log
    if [ "$?" -ne "0" ]
    then
	echo "ERROR: $tmp/ path is not writable, will not continue."
	exit 1
    fi
fi

ntpclient -h pool.ntp.org -s -c 1 > /dev/null 2>&1

echo "" | tee -a $log
date 2>&1 | tee -a $log
echo "OpenLGTV BCM $ver installation script by xeros" | tee -a $log

if [ "$2" = "autoupgrade" ]
then
    echo "Script is run as AUTOUPGRADE, forcing disable confirmations and reboot TV after successful flashing" | tee -a $log
    confirmations=0
    rebooting=1
    autoupgrade=1
fi

backup_error=0
# making current firmware backup if it's first installation
if [ "$make_backup" = "1" -a -d "$OpenLGTV_BCM_USB" -a "$ver_installed" = "" -a ! -f "/mnt/user/lock/backup-first_dump_of_mtd_partitions-done.lock" ]
then
    back_dir="$OpenLGTV_BCM_USB/backup"
    echo "Looks like OpenLGTV BCM installation is being run for the first time - making backup of current firmware to $back_dir" | tee -a $log
    mkdir -p "$back_dir" 2>&1 | tee -a $log
    for i in `cat /proc/mtd | grep -v erasesize | awk '{print $1 "_" $4}' | sed -e 's/\"//g' -e 's/mtd\(.\):/mtd0\1/' -e 's/://g'`
    do
	echo "Making standard backup of $i ..." | tee -a $log
	cat /dev/`echo $i | sed -e 's/_.*//g' -e 's/mtd0/mtd/g'` > $back_dir/$i 2>$log
	if [ "$?" -ne "0" ]
	then
	    echo "ERROR: Problem making backup of /dev/`echo $i | sed -e 's/_.*//g' -e 's/mtd0/mtd/g'` to $back_dir/$i" 2>&1 | tee -a $log
	    backup_error=1
	fi
    done
    for mount_path in `cat /proc/mounts | egrep "yaffs|jffs2" | awk '{print $2}'`
    do
	echo "Making tar archive backup of $mount_path ..." | tee -a $log
	tar cvf $back_dir/`echo $mount_path | sed -e 's#^/##g' -e 's#/#_#g'`.tar $mount_path >> $log 2>&1
	if [ "$?" -ne "0" ]
	then
	    echo "ERROR: Problem making backup of $mount_path to $back_dir/`echo $mount_path | sed -e 's#^/##g' -e 's#/#_#g'`.tar" 2>&1 | tee -a $log
	    backup_error=1
	fi
    done
    mkdir -p /mnt/user/lock > /dev/null 2>&1
    touch /mnt/user/lock/backup-first_dump_of_mtd_partitions-done.lock 2>&1 | tee -a $log
    echo "Backup done." | tee -a $log
fi

if [ "$backup_error" = "1" ]
then
    echo "Backup of some of the partitions was not done correctly. Are you sure you want to install OpenLGTV BCM?" | tee -a $log
    echo "Type \"YES\" or \"NO\"" | tee -a $log
    # confirmation handling
    answer=NO
    read answer
    if [ "$answer" != "YES" ]
    then
        echo "OK, not flashing" | tee -a $log
        echo "If you want to make backup again at second installation attempt then remove /mnt/user/lock/backup-first_dump_of_mtd_partitions-done.lock file:" | tee -a $log
        echo "rm -f /mnt/user/lock/backup-first_dump_of_mtd_partitions-done.lock" | tee -a $log
        exit 1
    fi
fi

# check for files existence
if [ -f $cdir/$file.sqf -a -f $cdir/$file.sha1 ]
then
    echo "Comparing flash file size and SHA1 checksum..."     | tee -a $log
else
    if [ -f ./$file.sqf -a -f ./file.sha1 ]
    then
	echo "Found needed files in current dir..."           | tee -a $log
	export cdir=.
	echo "Comparing flash file size and SHA1 checksum..." | tee -a $log
    else
	echo "Cannot continue, file $file.sqf or $file.sha1 does not exist in install.sh script dir and current dir." | tee -a $log
	exit 1
    fi
fi
# comparing size
if [ "`cat $cdir/$file.sqf | wc -c`" -ne "$size" ]
then
    echo "$file.sqf file size is incorrect. Download firmware again." | tee -a $log
    exit 1
fi
# comparing magic bytes
#if [ "`od -N4 -c $file.sqf | head -n1 | awk '{print $2 $3 $4 $5}'`" != "$magic" ]
#if [ "`head -c4 $file.sqf`" != "$magic" ]
if [ "`head -c4 $cdir/$file.sqf | od -c | head -n1 | awk '{print $2 $3 $4 $5}'`" != "$magic" ]
then
    echo "File $file.sqf header is incorrect. Download firmware again." | tee -a $log
    exit 1
fi
# copy to /tmp/
if [ "`echo $cdir | awk '{print substr($1,1,4)}'`" = "/tmp" ]
then
    echo "Current dir is inside /tmp, skipping copying files to /tmp"
    export tmp=$cdir
else
    cp $cdir/$file.sqf $cdir/$file.sha1 $tmp/ 
    if [ "$?" -ne "0" ]
    then
	echo "Something is wrong. Cannot copy the files to $tmp/" | tee -a $log
	exit 1
    fi
fi
# sha1sum compare
#cat $tmp/$file.sha1 | sed "s#$file#$tmp/$file#" > $tmp/$file.2.sha1 2>$tmpout | tee -a $log
sh -c "cat $tmp/$file.sha1 | sed \"s#$file#$tmp/$file#\" > $tmp/$file.2.sha1" > $tmpout 2>&1
cat $tmpout | tee -a $log
#sha1sum -c $tmp/$file.2.sha1 > $tmpout 2>&1
sh -c "sha1sum $tmp/$file.sqf > $tmp/$file.2x.sha1" 2>&1 | tee -a $log
diff $tmp/$file.2.sha1 $tmp/$file.2x.sha1 > $tmpout 2>&1
if [ "$?" -ne "0" ]
then
    cat $tmpout | tee -a $log
    echo "Checksum is incorrect. Download firmware again." | tee -a $log
    exit 1
fi
cat $tmpout | tee -a $log
# char and block devices search
if [ -c /dev/mtd$mtd -a -b /dev/mtdblock$mtd ]
then
    echo "/dev/mtd$mtd and /dev/mtdblock$mtd exist... - good" | tee -a $log
else
    echo "Did you run this installation script in TV? Looks like the device dont have the proper /dev/mtd$mtd and /dev/mtdblock$mtd devices." | tee -a $log
    exit 1
fi
if [ "$development" = "1" -a ! -f "/mnt/user/lock/development-logs-dumped.lock" ]
then
    devel_dir=$OpenLGTV_BCM_USB/development-logs
    mkdir -p $devel_dir
    if [ "$?" -eq "0" ]
    then
	echo "OpenLGTV BCM development version - taking more info from running system to $devel_dir" | tee -a $log
	echo "They are taken only once and might be useful for making better support platforms other than EU" | tee -a $log
	dmesg > $devel_dir/dmesg.log
	cat /proc/mtd > $devel_dir/proc_mtd.log
	cat /proc/mounts > $devel_dir/proc_mounts.log
	cat /proc/cpuinfo > $devel_dir/proc_cpuinfo.log
	cat /proc/cmdline > $devel_dir/proc_cmdline.log
	cat /proc/modules > $devel_dir/proc_modules.log
	cat /proc/version > $devel_dir/proc_version.log
	cat /etc/ver > $devel_dir/etc_ver.log
	uname -a > $devel_dir/uname-a.log
	ps w > $devel_dir/ps-w.log
	free > $devel_dir/free.log
	mount > $devel_dir/mount.log
	df -h > $devel_dir/df-h.log
	ls -laR /mnt/addon > $devel_dir/ls-alR-mnt_addon.log
	ls -laR /mnt/browser > $devel_dir/ls-alR-mnt_browser.log
	ls -laR /mnt/lg > $devel_dir/ls-alR-mnt_lg.log
	cat /mnt/addon/contents/config.xml > $devel_dir/mnt_addon_contents_config.xml
	cat /mnt/addon/bin/addon_mgr.bat > $devel_dir/mnt_addon_bin_addon_mgr.bat
	cat /mnt/addon/browser/browser_application.txt > $devel_dir/mnt_addon_browser_browser_application.txt
	cat /dev/mtd$mtd > $devel_dir/mtd$mtd.rootfs.dump
	cat /dev/mtd$lginit > $devel_dir/mtd$lginit.lginit.dump
	free > $devel_dir/free2.log
	#cp -r /mnt/addon $devel_dir > /dev/null 2>&1
	#cp -r /mnt/browser $devel_dir > /dev/null 2>&1
	mkdir -p /mnt/user/lock
	touch /mnt/user/lock/development-logs-dumped.lock
	echo "Debug info saved in $devel_dir, please give them + install log to OpenLGTV BCM developers for analyse." | tee -a $log
	echo "Please give us /var/log/OpenLGTV_BCM.log file taken from first boot, too - its very useful in case of any problems." | tee -a $log
    fi
fi

# Safety checks for supported rootfs version and partitions numbers
if [ "`cat /etc/ver | awk -F, '{print $1}'`" != "$supported_rootfs_ver" ]
then
    echo "ERROR: found NOT SUPPORTED yet TV model (unknown rootfs version) - please give yours firmware dump to OpenLGTV BCM developers for making support yours TV model" | tee -a $log
    echo "OpenLGTV BCM is not installed and no changes have been made to yours TV firmware" | tee -a $log
    exit 1
fi
if [ -z "`cat /proc/mtd | grep ^mtd$mtd: | grep rootfs`" ]
then
    echo "ERROR: /dev/mtd$mtd IS NOT rootfs parition, please give yours firmware dump to OpenLGTV BCM developers for making support yours TV model" | tee -a $log
    echo "OpenLGTV BCM is not installed and no changes have been made to yours TV firmware" | tee -a $log
    exit 1
fi
if [ -z "`cat /proc/mtd | grep ^mtd$lginit: | grep lginit`" ]
then
    echo "ERROR: /dev/mtd$lginit IS NOT lginit parition, please give yours firmware dump to OpenLGTV BCM developers for making support yours TV model" | tee -a $log
    echo "OpenLGTV BCM is not installed and no changes have been made to yours TV firmware" | tee -a $log
    exit 1
fi

# Backup
echo "Making backup from /dev/mtd$mtd to $dir/$file-$rootfs_backup.sqf" | tee -a $log
#cat /dev/mtd3 > $dir/$file-$rootfs_backup.sqf 2>$tmpout
sh -c "cat /dev/mtd3 > $dir/$file-$rootfs_backup.sqf" > $tmpout 2>&1
if [ "$?" -ne "0" ]
then
    cat $tmpout | tee -a $log
    echo "Cannot make current firmware dump from partition /dev/mtd$mtd" | tee -a $log
    echo "Refusing to flash" | tee -a $log
    exit 1
fi
# compare dump size
if [ "`cat $dir/$file-$rootfs_backup.sqf | wc -c`" -ne "$size" ]
then
    echo "Gathered dump from /dev/mtd$mtd partition has wrong size." | tee -a $log
    echo "Refusing to flash" | tee -a $log
    exit 1
fi
sync
# comparing magic bytes of dump
#if [ "`od -N4 -c $dir/$file-$rootfs_backup.sqf | head -n1 | awk '{print $2 $3 $4 $5}'`" != "$magic" ]
#if [ "`head -c4 $dir/$file-$rootfs_backup.sqf`" != "$magic" ]
if [ "`head -c4 $dir/$file-$rootfs_backup.sqf | od -c | head -n1 | awk '{print $2 $3 $4 $5}'`" != "$magic" ]
then
    echo "Gathered dump header from /dev/mtd$mtd partition is incorrect. Maybe you try to flash to wrong partition?" | tee -a $log
    exit 1
fi

if [ ! -f "/mnt/user/lock/backup-first_dump_of_writable_partitions-done.lock" ]
then
    for mount_path in `cat /proc/mounts | egrep "yaffs|jffs2" | awk '{print $2}'`
    do
	echo "Making tar backup of $mount_path ..." | tee -a $log
	# v- theres not gzip in default firmware
	#tar czvf $dir/`echo $mount_path | sed 's#^/##g' | sed 's#/#_#g'`.tar.gz $mount_path
	tar cf $dir/`echo $mount_path | sed 's#^/##g' | sed 's#/#_#g'`.tar $mount_path 2>&1 | tee -a $log
    done
    mkdir -p /mnt/user/lock
    touch /mnt/user/lock/backup-first_dump_of_writable_partitions-done.lock
fi

# kill web browser, addon_mgr and stagecraft to gain some free memory
echo "Stopping web browser process to gain some more free memory..." | tee -a $log
killall lb4wk                                                   2>&1 | tee -a $log
echo "Stopping addon_mgr process to gain more free memory..."        | tee -a $log
killall addon_mgr                                               2>&1 | tee -a $log
echo "Stopping stagecraft process to gain more free memory..."       | tee -a $log
killall stagecraft                                              2>&1 | tee -a $log
sleep 1                                                         2>&1 | tee -a $log

# check free ram
currfreemem=`free | grep Mem | awk '{print $4}'`
currbuffmem=`free | grep Mem | awk '{print $6}'`
curravailmem=$(($currfreemem + $currbuffmem))
reqavailmem=$((2*$reqfreemem))
if [ "$currfreemem" -lt "$reqfreemem" -a "$curravailmem" -lt "$reqavailmem" ]
then
    echo "There might be problem as you have only $currfreemem KB RAM free (+$currbuffmem KB on buffers), its less than $reqfreemem KB ($reqavailmem KB with buffers)." | tee -a $log
    echo "Refusing to flash as later there could be problem with available memory." | tee -a $log
    echo "Dont worry - just reboot TV (or power off and on) and try install again." | tee -a $log
    exit 1
else
    echo "You have $currfreemem KB RAM free (+$currbuffmem KB on buffers) - good." | tee -a $log
fi
# question
echo "Do you really want to flash the /dev/mtd$mtd (`cat /proc/mtd | grep mtd$mtd: | awk '{print $4}'`) device?" | tee -a $log
echo "Type \"YES\" or \"NO\"" | tee -a $log
# confirmation handling
if [ "$confirmations" = "1" ]
then
    read answer
else
    echo "Auto confirmation to YES..." | tee -a $log
    answer=YES
fi
if [ "$answer" != "YES" ]
then
    echo "OK, not flashing" | tee -a $log
    exit 1
fi
# ERASING
echo "From now on DO NOT POWER OFF YOURS TV AND PC" | tee -a $log
echo "Erasing /dev/mtd$mtd partition... for prepare it to flash" | tee -a $log
flash_eraseall /dev/mtd$mtd 2>$tmpout
if [ "$?" -ne "0" ]
then
    cat $tmpout | tee -a $log
    echo "ERROR: Erasing /dev/mtd$mtd partition havent succeed." | tee -a $log
    errorr=1
else
    echo "Erasing succeed." | tee -a $log
    echo "Now starting to flash /dev/mtd$mtd partition..." | tee -a $log
    echo "Still DO NOT POWER OFF YOURS TV AND PC" | tee -a $log
    sync
    # FLASHING
    #cat $tmp/$file.sqf > /dev/mtd$mtd 2>$tmpout
    sh -c "cat $tmp/$file.sqf > /dev/mtd$mtd" > $tmpout 2>&1
    if [ "$?" -ne "0" ]
    then
	cat $tmpout | tee -a $log
	echo "ERROR: Flashing /dev/mtd$mtd partition havent succeed." | tee -a $log
	errorr=1
    else
	echo "Flashing process succeeded, but wait until the script ends and gets back to shell" | tee -a $log
	sync
	echo "We need to ensure the partition is ok" | tee -a $log
	sync
	#sleep 30
	sleep 10
	sync
    fi
fi
# ERROR handling
if [ "$errorr" = "1" ]
then
    echo "Trying to flash through /dev/mtdblock$mtd instead..." | tee -a $log
    echo "This method is not as good for flashing by hand but still could work as eraseing and flashing is handled by driver" | tee -a $log
    echo "This flashing method should take about 5 minutes for ensuring the saftyness" | tee -a $log
    #cat $tmp/$file.sqf > /dev/mtdblock$mtd 2>$tmpout
    sh -c "cat $tmp/$file.sqf > /dev/mtdblock$mtd" > $tmpout 2>&1
    if [ "$?" -ne "0" ]
    then
	cat $tmpout | tee -a $log
	echo "ERROR: Flashing to /dev/mtdblock$mtd partition havent succeed." | tee -a $log
	echo "Flashing to /dev/mtdblock$mtd partition havent succeed." | tee -a $log
	echo "Go ask for help at #openlgtv IRC channel at irc.freenode.net server." | tee -a $log
	echo "DONT REBOOT OR POWER OFF TV AS IT MIGHT NOT POWER ON AGAIN" | tee -a $log
	exit 1
    else
	sync
	echo "Looks like flashing through /dev/mtdblock$mtd succeed." | tee -a $log
	echo "But you cant reboot or poweroff TV yet" | tee -a $log
	sync
	echo "Theres some erasing/flashing done in background." | tee -a $log
	sync
	sleep 180
	sync
    fi
fi
# making second dump
#cat /dev/mtd$mtd > $dir/$file-$backup2.sqf 2>$tmpout
sh -c "cat /dev/mtd$mtd > $dir/$file-$backup2.sqf" > $tmpout 2>&1
cat $tmpout | tee -a $log
sync
diff $dir/$file-$backup2.sqf $dir/$file.sqf > $tmpout 2>&1 
if [ "$?" -ne "0" ]
then
    cat $tmpout | tee -a $log
    echo "ERROR: Looks like flashing has succeed but the dump after flashing is not the same as file flashed." | tee -a $log
    sync
    echo "Lets wait a bit longer and check again..." | tee -a $log
    sync
    sleep 120
    sync
    #cat /dev/mtd$mtd > $dir/$file-$backup2.sqf 2>$tmpout
    sh -c "cat /dev/mtd$mtd > $dir/$file-$backup2.sqf" > $tmpout 2>&1
    cat $tmpout | tee -a $log
    sync
    diff $dir/$file-$backup2.sqf $dir/$file.sqf > $tmpout 2>&1
    if [ "$?" -ne "0" ]
    then
	cat $tmpout | tee -a $log
	echo "ERROR: The dumped file still differs from flashed file." | tee -a $log
	echo "Go ask for help at #openlgtv IRC channel at irc.freenode.net server." | tee -a $log
	echo "If youre connected via telnet or SSH prepare RS232 Null-Modem cable..." | tee -a $log
	echo "... to connect to the TV to try flashing through CFE bootloader" | tee -a $log
	echo "DONT REBOOT OR POWER OFF TV AS IT MIGHT NOT POWER ON AGAIN" | tee -a $log
	exit 1
    fi
fi
cat $tmpout | tee -a $log
echo "Looks like flashing finally succeeded." | tee -a $log
# removing second backup, after flashing
rm -f $dir/$file-$backup2.sqf
# renaming flash file to prevent another flashing
if [ "$dir" != "$tmp" ]
then
    echo "Renaming original file to prevent second time flashing..." | tee -a $log
    mv $dir/$file.sqf $dir/$file-$suffix.sqf > $tmpout 2>&1
    cat $tmpout | tee -a $log
else
    echo "Please rename the file $file.sqf yourself to prevent future flashing the same firmware again" | tee -a $log
    echo "You might copy the $dir/$file-$rootfs_backup.sqf file to have backup." | tee -a $log
fi
sync
# making backup of lginit
echo "Making backup of lginit from /dev/mtd$lginit partition..." | tee -a $log
#cat /dev/mtd$lginit > $dir/$file-$lginit_backup.sqf 2>$tmpout
sh -c "cat /dev/mtd$lginit > $dir/$file-$lginit_backup.sqf" > $tmpout 2>&1
if [ "$?" -ne "0" ]
then
    cat $tmpout | tee -a $log
    echo "WARNING: could not make dump of lginit (/dev/mtd$lginit) partition" | tee -a $log
    warnr=1
fi
sync
# comparing magic bytes of lginit dump
if [ "`head -c4 $dir/$file-$lginit_backup.sqf | od -c | head -n1 | awk '{print $2 $3 $4 $5}'`" = "$magic_clean" ]
then
    echo "Gathered dump header from /dev/mtd$mtd partition shows that the lginit partition is already erased - good." | tee -a $log
    echo "Moving all files to flashed subdir to prevent autoupgrade on next boot..."
    mkdir -p $dir/flashed $tmp/flashed
    mv $dir/*.sqf $dir/*.sha1 $dir/*.log $dir/flashed/ > $tmpout 2>&1
    log=`echo $log | sed "s#$file#flashed/$file#"`
    cat $tmpout | tee -a $log
    date 2>&1 | tee -a $log
    echo "" | tee -a $log
    sync
    if [ "$rebooting" = "1" ]
    then
	echo "Rebooting TV..." | tee -a $log
	reboot
    else
	echo "You may now poweroff and poweron TV" | tee -a $log
    fi
    exit 0
fi
# question
echo "Do you really want to erase the /dev/mtd$lginit (`cat /proc/mtd | grep mtd$lginit: | awk '{print $4}'`) device?" | tee -a $log
echo "Type \"YES\" or \"NO\"" | tee -a $log
# confirmation handling
if [ "$confirmations" = "1" ]
then
    read answer
else
    echo "Auto confirmation to YES..." | tee -a $log
    answer=YES
fi
if [ "$answer" != "YES" ]
then
    echo "OK, not flashing" | tee -a $log
    exit 1
fi
# erasing lginit partition
echo "Trying to remove lginit..." | tee -a $log
flash_eraseall /dev/mtd$lginit 2>$tmpout
if [ "$?" -ne "0" ]
then
    cat $tmpout | tee -a $log
    echo "WARNING: Erasing lginit (/dev/mtd$lginit) partition problem." | tee -a $log
    echo "Trying fallback with zeroing this partition..." | tee -a $log
    warnr=1
    echo "Trying to flash through /dev/mtdblock$lginit instead..." | tee -a $log
    echo "This method is not as good for flashing by hand but still could work as eraseing and flashing is handled by driver" | tee -a $log
    echo "This flashing method should take about 5 minutes for ensuring the saftyness" | tee -a $log
    head -c$lginit_size /dev/zero > $tmp/lginit-zeroed.img 2>$tmpout
    cat $tmpout | tee -a $log
    #cat $tmp/lginit-zeroed.img > /dev/mtdblock$lginit 2>$tmpout
    sh -c "cat $tmp/lginit-zeroed.img > /dev/mtdblock$lginit" > $tmpout 2>&1
    if [ "$?" -ne "0" ]
    then
	cat $tmpout | tee -a $log
	echo "ERROR: Flashing zeroed partition to /dev/mtdblock$lginit partition havent succeed." | tee -a $log
	echo "TV should still boot ok after reboot, but still might work like original LG firmware" | tee -a $log
	echo "After reboot try to erase the partition yourself using this command (copy and paste it to not make mistake):" | tee -a $log
	echo "flash_eraseall /dev/mtd$lginit" | tee -a $log
	sync
    else
	sync
	echo "Looks like flashing by zeroing through /dev/mtdblock$lginit succeed." | tee -a $log
	echo "But you cant reboot or poweroff TV yet" | tee -a $log
	sync
	echo "Theres some erasing/flashing done in background." | tee -a $log
	sync
	sleep 30
	sync
    fi
fi
# rebooting...
sleep 5
sync
echo "Moving all files to flashed subdir to prevent autoupgrade on next boot..."
mkdir -p $dir/flashed $tmp/flashed
mv $dir/*.sqf $dir/*.sha1 $dir/*.log $dir/flashed/ > $tmpout 2>&1
log=`echo $log | sed "s#$file#flashed/$file#"`
cat $tmpout | tee -a $log
sync
date 2>&1 | tee -a $log
echo "" | tee -a $log
if [ "$rebooting" = "1" ]
then
    echo "Rebooting TV..." | tee -a $log
    reboot
else
    echo "You may now poweroff and poweron TV" | tee -a $log
fi

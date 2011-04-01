#!/bin/sh
# OpenLGTV BCM installation script by xeros, ver. 0.4

# it needs $file.sqf and $file.md5 files in the same dir as this script

# if 'confirmations' is set to '1' then it asks for confirmation, if '0' then autoconfirm
# if 'rebooting' is set to '1' then TV is autorebooted after after successful flashing

# vars set
confirmations=1
rebooting=0

ver=0.2.0
file=OpenLGTV_BCM-v$ver
size=3145728
mtd=3
magic=hsqs
magic_clean=377377377377
lginit=4
lginit_size=262144

tmp=/tmp
dir=`dirname $0`
cdir=$dir
#log=$dir/$file.log
log="$dir/$file.log $tmp/$file.log"
tmpout=$tmp/output.log
freemem=20000


backup=pre-backup
suffix=flashed
backup2=$suffix-backup

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
# check for files existence
if [ -f $cdir/$file.sqf -a -f $cdir/$file.md5 ]
then
    echo "Comparing flash file size and MD5 checksum..." | tee -a $log
else
    echo "Cannot continue, file $file.sqf or $file.md5 does not exist." | tee -a $log
    exit 1
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
cp $cdir/$file.sqf $cdir/$file.md5 $tmp/ 
if [ "$?" -ne "0" ]
then
    echo "Something is wrong. Cannot copy the files to $tmp/" | tee -a $log
    exit 1
fi
# md5sum compare
#cat $tmp/$file.md5 | sed "s#$file#$tmp/$file#" > $tmp/$file.2.md5 2>$tmpout | tee -a $log
sh -c "cat $tmp/$file.md5 | sed \"s#$file#$tmp/$file#\" > $tmp/$file.2.md5" > $tmpout 2>&1
cat $tmpout | tee -a $log
md5sum -c $tmp/$file.2.md5 > $tmpout 2>&1
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
# Backup
echo "Making backup from /dev/mtd$mtd to $dir/$file-$backup.sqf" | tee -a $log
#cat /dev/mtd3 > $dir/$file-$backup.sqf 2>$tmpout
sh -c "cat /dev/mtd3 > $dir/$file-$backup.sqf" > $tmpout 2>&1
if [ "$?" -ne "0" ]
then
    cat $tmpout | tee -a $log
    echo "Cannot make current firmware dump from partition /dev/mtd$mtd" | tee -a $log
    echo "Refusing to flash" | tee -a $log
    exit 1
fi
# compare dump size
if [ "`cat $dir/$file-$backup.sqf | wc -c`" -ne "$size" ]
then
    echo "Gathered dump from /dev/mtd$mtd partition has wrong size." | tee -a $log
    echo "Refusing to flash" | tee -a $log
    exit 1
fi
sync
# comparing magic bytes of dump
#if [ "`od -N4 -c $dir/$file-$backup.sqf | head -n1 | awk '{print $2 $3 $4 $5}'`" != "$magic" ]
#if [ "`head -c4 $dir/$file-$backup.sqf`" != "$magic" ]
if [ "`head -c4 $dir/$file-$backup.sqf | od -c | head -n1 | awk '{print $2 $3 $4 $5}'`" != "$magic" ]
then
    echo "Gathered dump header from /dev/mtd$mtd partition is incorrect. Maybe you try to flash to wrong partition?" | tee -a $log
    exit 1
fi
# check free ram
if [ "`free | grep Mem | awk '{print $4}'`" -lt "$freemem" ]
then
    echo "There might be problem as you have less than $freemem KB RAM free." | tee -a $log
    echo "(The builtin web browser is set to send OutOfMemory signals if there is less than 20MB free RAM)" | tee -a $log
    echo "Refusing to flash" | tee -a $log
    exit 1
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
	sleep 30
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
# renaming flash file to prevent another flashing
if [ "$dir" != "$tmp" ]
then
    echo "Renaming original file to prevent second time flashing..." | tee -a $log
    mv $dir/$file.sqf $dir/$file-$suffix.sqf > $tmpout 2>&1
    cat $tmpout | tee -a $log
else
    echo "Please rename the file $file.sqf yourself to prevent future flashing the same firmware again" | tee -a $log
    echo "You might copy the $dir/$file-$backup.sqf file to have backup." | tee -a $log
fi
sync
# making backup of lginit
echo "Making backup of lginit from /dev/mtd$lginit partition..." | tee -a $log
#cat /dev/mtd$lginit > $dir/$file-lginit-$backup.sqf 2>$tmpout
sh -c "cat /dev/mtd$lginit > $dir/$file-lginit-$backup.sqf" > $tmpout 2>&1
if [ "$?" -ne "0" ]
then
    cat $tmpout | tee -a $log
    echo "WARNING: could not make dump of lginit (/dev/mtd$lginit) partition" | tee -a $log
    warnr=1
fi
sync
# comparing magic bytes of lginit dump
if [ "`head -c4 $dir/$file-lginit-$backup.sqf | od -c | head -n1 | awk '{print $2 $3 $4 $5}'`" = "$magic_clean" ]
then
    echo "Gathered dump header from /dev/mtd$mtd partition shows that the lginit partition is already erased - good." | tee -a $log
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
date 2>&1 | tee -a $log
echo "" | tee -a $log
if [ "$rebooting" = "1" ]
then
    echo "Rebooting TV..." | tee -a $log
    reboot
else
    echo "You may now poweroff and poweron TV" | tee -a $log
fi

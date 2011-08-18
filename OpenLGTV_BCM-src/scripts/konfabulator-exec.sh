#!/bin/sh
# konfabulator-exec.sh script by xeros
# Source code released under GPL License
if [ ! -d "$ywedir" -a ! -h "$ywedir" ]
then
    ywedir_old="$ywedir"
    for usb_port in usb1 usb2
    do
	for drive in Drive1 Drive2 Drive3 Drive4
	do
	    [ -d "/mnt/$usb_port/$drive/OpenLGTV_BCM/ywe" ] && ywedir="/mnt/$usb_port/$drive/OpenLGTV_BCM/ywe"
	done
    done
    if [ "$ywedir" != "$ywedir_old" ]
    then
	echo "OpenLGTV_BCM-INFO: konfabulator-exec.sh: ywe not found in ywedir=$ywedir_old path, but found in $ywedir..." | tee -a /var/log/OpenLGTV_BCM.log
    fi
    #ywedir=/mnt/usb1/Drive1/OpenLGTV_BCM/ywe
fi

if [ -f "$ywedir/bin/konfabulator.sh" -o -h "$ywedir/bin/konfabulator.sh" ]
then
	echo "OpenLGTV_BCM-INFO: konfabulator-exec.sh: running $ywedir/bin/konfabulator.sh..." | tee -a /var/log/OpenLGTV_BCM.log
	$ywedir/bin/konfabulator.sh $* 2>&1 | tee -a /var/log/OpenLGTV_BCM.log
	killall lb4wk > /dev/null 2>&1
else
	# if konfabulator.sh file does not exist, try to run web browser instead
	echo "OpenLGTV_BCM-WARN: konfabulator-exec.sh: $ywedir/bin/konfabulator.sh file does not exist, trying to start web browser instead..." | tee -a /var/log/OpenLGTV_BCM.log
	if [ -f "/mnt/browser/run3556" -o -h "/mnt/browser/run3556" ]
	then
	    /mnt/browser/run3556 254  2>&1 | tee -a /var/log/OpenLGTV_BCM.log
	else
	    echo "OpenLGTV_BCM-ERROR: konfabulator-exec.sh: both $ywedir/bin/konfabulator.sh and /mnt/browser/run3556 files do not exist, killing StageCraft so you wont get black screen but remote still might have problems..." | tee -a /var/log/OpenLGTV_BCM.log
	    killall stagecraft        2>&1 | tee -a /var/log/OpenLGTV_BCM.log
	fi 
fi

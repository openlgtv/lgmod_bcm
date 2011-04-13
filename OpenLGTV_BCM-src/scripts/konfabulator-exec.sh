#!/bin/sh
if [ ! -d "$ywedir" -o ! -h "$ywedir" ]
then
    echo "OpenLGTV_BCM-INFO: konfabulator-exec.sh: not found ywedir=$ywedir path, trying set it to /mnt/usb1/Drive1/OpenLGTV_BCM/ywe instead..." | tee -a /var/log/OpenLGTV_BCM.log
    ywedir=/mnt/usb1/Drive1/OpenLGTV_BCM/ywe
fi

if [ -f "$ywedir/bin/konfabulator.sh" -o -h "$ywedir/bin/konfabulator.sh" ]
then
	echo "OpenLGTV_BCM-INFO: konfabulator-exec.sh: running $ywedir/bin/konfabulator.sh..." | tee -a /var/log/OpenLGTV_BCM.log
	$ywedir/bin/konfabulator.sh $* 2>&1 | tee -a /var/log/OpenLGTV_BCM.log
else
	# if konfabulator.sh file does not exist, try to run web browser instead
	echo "OpenLGTV_BCM-WARN: konfabulator-exec.sh: $ywedir/bin/konfabulator.sh file does not exist, trying to start web browser instead..." | tee -a /var/log/OpenLGTV_BCM.log
	if [ -f "/mnt/browser/run3556" -o -h "/mnt/browser/run3556" ]
	then
	    /mnt/browser/run3556 254 2>&1 | tee -a /var/log/OpenLGTV_BCM.log
	else
	    echo "OpenLGTV_BCM-ERROR: konfabulator-exec.sh: both $ywedir/bin/konfabulator.sh and /mnt/browser/run3556 files do not exist, killing StageCraft so you wont get black screen but remote still might have problems..." | tee -a /var/log/OpenLGTV_BCM.log
	    killall stagecraft 2>&1 | tee -a /var/log/OpenLGTV_BCM.log
	fi 
fi

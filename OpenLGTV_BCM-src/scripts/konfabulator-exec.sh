#!/bin/sh
# konfabulator-exec.sh script by xeros
# Source code released under GPL License

# TODO: move USB storage device mounted check outside of this script

[ -z "$ywedir" ] && ywedir=/mnt/addon/ywe

#if [ ! -d "$ywedir" -a ! -h "$ywedir" ]
#then
    if [ "$OpenLGTV_BCM_USB" = "" ]
    then
	if [ -f "/tmp/usbdir" ]
	then
	    export OpenLGTV_BCM_USB="`cat /tmp/usbdir`/OpenLGTV_BCM"
	fi
    fi
    ywedir_old="$ywedir"
    [ -d "$OpenLGTV_BCM_USB/ywe" ] && ywedir="$OpenLGTV_BCM_USB/ywe"
    if [ "$ywedir" != "$ywedir_old" ]
    then
	echo "OpenLGTV_BCM-INFO: konfabulator-exec.sh: ywe not found in ywedir=$ywedir_old path, but found in $ywedir..."
    fi
#fi

if [ -f "$ywedir/bin/konfabulator.sh" -o -h "$ywedir/bin/konfabulator.sh" ]
then
	echo "OpenLGTV_BCM-INFO: konfabulator-exec.sh: running $ywedir/bin/konfabulator.sh..."
	$ywedir/bin/konfabulator.sh $*
	killall lb4wk GtkLauncher > /dev/null 2>&1
	while [ -e "$ywedir/bin/konfabulator.sh" ]
	do
	    sleep 2
	done
	echo "OpenLGTV_BCM-INFO: konfabulator-exec.sh: USB storage device unmounted/disconnected trying to stop Konfabulator and umount dirs..."
	killall konfabulator
	sleep 1
	umount -f /mnt/widget.data
	for ywd in /mnt/ywe_lg /mnt/ywe_s
	do
	    umount -f $ywd/config-oem.xml
	    umount -f $ywd/bin/konfabulator.sh
	    umount -f $ywd
	done
else
	# if konfabulator.sh file does not exist, try to run web browser instead
	echo "OpenLGTV_BCM-WARN: konfabulator-exec.sh: $ywedir/bin/konfabulator.sh file does not exist, trying to start web browser with info message instead..."
	if [ -f "/mnt/browser/run3556" -o -h "/mnt/browser/run3556" ]
	then
	    /mnt/browser/run3556 http://127.0.0.1:88/ywe/
	else
	    echo "OpenLGTV_BCM-ERROR: konfabulator-exec.sh: both $ywedir/bin/konfabulator.sh and /mnt/browser/run3556 files do not exist, killing StageCraft so you wont get black screen but remote still might have problems..."
	    killall stagecraft
	fi 
fi

#!/bin/sh
# Hotplug wrapper for LGMOD
# Created by djpety (c)2011
# Modified/adapted for LGMOD S7 by mmm4m5m and for OpenLGTV BCM by xeros
# v1.1

HOTPLUG_FW_DIRS='/mnt/user/firmware /lib/firmware'

echo "hotplug: ACTION=$ACTION SUBSYSTEM=$SUBSYSTEM FIRMWARE=$FIRMWARE DEVPATH=$DEVPATH PHYSDEVDRIVER=$PHYSDEVDRIVER ($@)" > /dev/kmsg

if [ "$ACTION" == "add" ]
then
    if [ "$SUBSYSTEM" = "firmware" ]
    then
	CMD='cat'
	for i in $HOTPLUG_FW_DIRS; do
		FW="$i/$FIRMWARE"; [ -f "$FW" ] && break
		[ -f "$FW.gz" ] && { FW="$FW.gz"; CMD='gzip -d -c'; break; }
	done
	if [ -f "$FW" ]; then
		if echo 1 > /sys/$DEVPATH/loading &&
			$CMD $FW > /sys/$DEVPATH/data; then
			echo 0 > /sys/$DEVPATH/loading
			echo "hotplug: Done: $ACTION $SUBSYSTEM $FIRMWARE" > /dev/kmsg
			exit 0; # skip LG hotplug?
		else
			echo 0 > /sys/$DEVPATH/loading
			echo "hotplug: Error $? ($ACTION $SUBSYSTEM $FIRMWARE)" > /dev/kmsg
			#exit 1; # skip LG hotplug?
		fi
	else
		echo "hotplug: Error: $FIRMWARE not found." > /dev/kmsg
	fi
    else
	if [ "$PHYSDEVDRIVER" = "usb-storage" ]
	then
	    (/bin/sleep 1; date; /etc/rc.d/rc.usb hotplug) >> /var/log/OpenLGTV_BCM.log &
	fi
    fi
fi

/bin/hotplug "$@"

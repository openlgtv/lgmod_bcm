#!/bin/sh
# Hotplug wrapper for LGMOD
# Originally created by djpety (c)2011
# Modified/adapted for LGMOD S7 by mmm4m5m and for OpenLGTV BCM by xeros
# v1.2.1

HOTPLUG_FW_DIRS='/mnt/user/firmware /lib/firmware'
USBHID_CONNECTED_DIR="/var/run/usbhid.connected"

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
	#if [ "$PHYSDEVDRIVER" = "usb-storage" ]
	# Launch "rc.usb hotplug sd?" only for /block/sd? devices, ommiting launching on found partitions
	#if [ "$PHYSDEVDRIVER" = "sd" -a "$SUBSYSTEM" = "block" -a "${DEVPATH:0:9}" = "/block/sd" -a "${DEVPATH:10:1}" = "" ]
	if [ "${DEVPATH:0:9}" = "/block/sd" -a "${DEVPATH:10:1}" = "" ]
	then
	    /etc/rc.d/rc.usb hotplug "${DEVPATH:7:3}" >> /var/log/OpenLGTV_BCM.log &
	else
	    if [ "$PHYSDEVDRIVER" = "usbhid" -a "${DEVPATH:20:5}" = "event" ]
	    then
		(if mkdir "$USBHID_CONNECTED_DIR" 2>/dev/null; then /etc/rc.d/rc.directfb hotplug add; fi) >> /var/log/OpenLGTV_BCM.log &
	    fi
	fi
    fi
else
    if [ "$ACTION" == "remove" ]
    then
	if [ "$PHYSDEVDRIVER" = "usbhid" -a "${DEVPATH:20:5}" = "event" ]
	then
	    (date; rmdir "$USBHID_CONNECTED_DIR"; /etc/rc.d/rc.directfb hotplug remove) >> /var/log/OpenLGTV_BCM.log &
	fi
    fi
fi

/bin/hotplug "$@"

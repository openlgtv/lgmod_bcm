#!/bin/sh
# Hotplug wrapper for LGMOD
# Originally created by djpety (c)2011
# Modified/adapted for LGMOD S7 by mmm4m5m and for OpenLGTV BCM by xeros
# v1.3.0

HOTPLUG_FW_DIRS='/mnt/user/firmware /lib/firmware'
USBHID_CONNECTED_DIR="/var/run/usbhid.connected"

echo "hotplug: SEQNUM=$SEQNUM ACTION=$ACTION SUBSYSTEM=$SUBSYSTEM FIRMWARE=$FIRMWARE DEVNAME=$DEVNAME DEVTYPE=$DEVTYPE DEVPATH=$DEVPATH PHYSDEVDRIVER=$PHYSDEVDRIVER PHYSDEVPATH=$PHYSDEVPATH PHYSDEVBUS=$PHYSDEVBUS DEVICE=$DEVICE MODALIAS=$MODALIAS MAJOR=$MAJOR MINOR=$MINOR PRODUCT=$PRODUCT INTERFACE=$INTERFACE TYPE=$TYPE BUSNUM=$BUSNUM ($@)" > /dev/kmsg
# examples:
# hotplug: SEQNUM=451 ACTION=add SUBSYSTEM=block FIRMWARE= DEVNAME=sda DEVTYPE=disk DEVPATH=/block/sda PHYSDEVDRIVER=sd PHYSDEVPATH=/devices/platform/ehci-brcm.0/usb1/1-2/1-2.2/1-2.2:1.0/host4/target4:0:0/4:0:0:0 PHYSDEVBUS=scsi DEVICE= MODALIAS= MAJOR=8 MINOR=0 PRODUCT= INTERFACE= TYPE= BUSNUM= (block)
# hotplug: SEQNUM=452 ACTION=add SUBSYSTEM=block FIRMWARE= DEVNAME=sda1 DEVTYPE=partition DEVPATH=/block/sda/sda1 PHYSDEVDRIVER=sd PHYSDEVPATH=/devices/platform/ehci-brcm.0/usb1/1-2/1-2.2/1-2.2:1.0/host4/target4:0:0/4:0:0:0 PHYSDEVBUS=scsi DEVICE= MODALIAS= MAJOR=8 MINOR=1 PRODUCT= INTERFACE= TYPE= BUSNUM= (block)
# hotplug: SEQNUM=470 ACTION=add SUBSYSTEM=block FIRMWARE= DEVNAME=sdb DEVTYPE=disk DEVPATH=/block/sdb PHYSDEVDRIVER=sd PHYSDEVPATH=/devices/platform/ehci-brcm.0/usb1/1-2/1-2.1/1-2.1:1.0/host5/target5:0:0/5:0:0:0 PHYSDEVBUS=scsi DEVICE= MODALIAS= MAJOR=8 MINOR=16 PRODUCT= INTERFACE= TYPE= BUSNUM= (block)
# hotplug: SEQNUM=478 ACTION=remove SUBSYSTEM=block FIRMWARE= DEVNAME=sdb DEVTYPE=disk DEVPATH=/block/sdb PHYSDEVDRIVER=sd PHYSDEVPATH=/devices/platform/ehci-brcm.0/usb1/1-2/1-2.1/1-2.1:1.0/host5/target5:0:0/5:0:0:0 PHYSDEVBUS=scsi DEVICE= MODALIAS= MAJOR=8 MINOR=16 PRODUCT= INTERFACE= TYPE= BUSNUM= (block)


if [ -f "/mnt/lg/lginit/lginit" ]
then
    if mkdir "/tmp/lginit-kill" 2>/dev/null
    then
	/etc/rc.d/rc.kill-lginit > /dev/kmsg &
    fi
    /bin/hotplug-real "$@"
    exit 0
fi

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
    fi
fi

if [ "$PHYSDEVDRIVER" = "usbhid" -a "${DEVPATH:20:5}" = "event" ]
then
    [ "$ACTION" = "add"    ] && (if    mkdir "$USBHID_CONNECTED_DIR" 2>/dev/null; then /etc/rc.d/rc.directfb hotplug $ACTION; fi) >> /var/log/OpenLGTV_BCM.log &
    [ "$ACTION" = "remove" ] && (date; rmdir "$USBHID_CONNECTED_DIR" 2>/dev/null;      /etc/rc.d/rc.directfb hotplug $ACTION)     >> /var/log/OpenLGTV_BCM.log &
fi

#if [ "${DEVPATH:0:9}" = "/block/sd" -a "${DEVPATH:10:1}" = "" ]
if [ "$SUBSYSTEM" = "block" -a "$DEVTYPE" = "disk" ]
then
    #/etc/rc.d/rc.usb hotplug "${DEVPATH:7:3}" "$ACTION" >> /var/log/OpenLGTV_BCM.log &
    /etc/rc.d/rc.usb hotplug "$DEVNAME" "$ACTION" "usb${PHYSDEVPATH:43:1}" >> /var/log/OpenLGTV_BCM.log &
    # example: .../rc.usb hotplug sda add usb1
fi

/bin/hotplug-real "$@"

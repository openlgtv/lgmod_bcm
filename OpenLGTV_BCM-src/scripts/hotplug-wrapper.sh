#!/bin/sh
# Hotplug wrapper for LGMOD
# Created by djpety (c)2011
# v1.0
HOTPLUG_FW_DIR=/lib/firmware
 
if [ "$ACTION" == "add"  ] && [ "$SUBSYSTEM" == "firmware" ]; then
 
        echo 1 > /sys/$DEVPATH/loading
        gzip -d -c $HOTPLUG_FW_DIR/$FIRMWARE.gz > /sys/$DEVPATH/data
        echo 0 > /sys/$DEVPATH/loading
else
        /bin/hotplug "$@"
fi
 
#echo "--- Hotplug debug ---" >> /mnt/usb1/Drive1/hotdebug.log
#echo `env` >> /mnt/usb1/Drive1/hotdebug.log


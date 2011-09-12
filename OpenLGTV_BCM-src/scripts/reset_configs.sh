#!/bin/sh
# OpenLGTV BCM configs cleaner by xeros
# Source code released under GPL License

[ -z "$bootlogf" ] && bootlogf=/var/log/OpenLGTV_BCM.log

if [ -z "$OpenLGTV_BCM_USB" ]
then
    if [ -f "/tmp/usbdir" ]
    then
	export USB_DIR="`cat /tmp/usbdir`"
    else
	# TODO: just a ugly, hacky workaround, I am too busy to change it now
	export USB_DIR="/tmp"
	mkdir -p /tmp/OpenLGTV_BCM
    fi
    export OpenLGTV_BCM_USB="$USB_DIR/OpenLGTV_BCM"
fi

if [ "$1" = "netcast_only" ]
then
	echo "OpenLGTV_BCM-INFO: making copy of OpenLGTV BCM netcast configs from /mnt/user/* to USB storage device..."
	cfg_bck_dir="$OpenLGTV_BCM_USB/netcast_config_backup"
	mkdir -p "$cfg_bck_dir"
	echo "OpenLGTV_BCM-INFO: making copy of NetCast configs from /mnt/user/netcast to USB storage device..."
	cp -rf /mnt/user/netcast $cfg_bck_dir/
	echo "OpenLGTV_BCM-INFO: erasing NetCast configs from /mnt/user/netcast ..."
	rm -rf /mnt/user/netcast
	echo "OpenLGTV_BCM-INFO: making copy of YWE configs from /mnt/user/ywe to USB storage device..."
	cp -rf /mnt/user/ywe $cfg_bck_dir/
	echo "OpenLGTV_BCM-INFO: erasing YWE configs from /mnt/user/ywe ..."
	rm -rf /mnt/user/ywe
else
	echo "OpenLGTV_BCM-INFO: making copy of OpenLGTV BCM configs from /mnt/user/* to USB storage device..."
	[ -z "$cfg_bck_dir" ] && cfg_bck_dir="$OpenLGTV_BCM_USB/config_backup"
	mkdir -p "$cfg_bck_dir"
	cp -rf /mnt/user/* $cfg_bck_dir/
	#cp -rf /mnt/user/.* $cfg_bck_dir/
	echo "OpenLGTV_BCM-INFO: erasing data from /mnt/user/..."
	rm -rf /mnt/user/*
	echo "OpenLGTV_BCM-INFO: making copy of OpenLGTV BCM configs from /home/* to USB storage device..."
	cp -rf /home/.ash_history /home/.hush_history /home/.ssh $cfg_bck_dir/
	echo "OpenLGTV_BCM-INFO: erasing OpenLGTV BCM configs from /home/* ..."
	rm -rf /home/.ash_history /home/.hush_history /home/.ssh
	echo "OpenLGTV_BCM-INFO: erasing DirectFB input drivers from /home/inputdrivers/..."
	rm -rf /home/inputdrivers
	[ -f "$OpenLGTV_BCM_USB/reset_config" ] && mv $OpenLGTV_BCM_USB/reset_config $OpenLGTV_BCM_USB/reset_config.used
fi

echo "OpenLGTV_BCM-INFO: making copy of custom NetCast icons from /home/netcast_icons/* to USB storage device..."
cp -rf /home/netcast_icons $cfg_bck_dir/
echo "OpenLGTV_BCM-INFO: erasing custom NetCast icons from /home/netcast_icons/..."
rm -rf /home/netcast_icons
sync
#echo "OpenLGTV_BCM-INFO: config folder is copied to USB drive and deleted. Rebooting..."
echo "OpenLGTV_BCM-INFO: config folder is copied to USB drive and deleted, you may reboot now."
#/bin/date +"OpenLGTV_BCM-TIME: %F %T script: $0"
cp -f $bootlogf $cfg_bck_dir/
#umount -f /mnt/usb1/Drive1 > /dev/null 2>&1
#umount -f /mnt/usb2/Drive1 > /dev/null 2>&1
sync
#reboot
exit 0

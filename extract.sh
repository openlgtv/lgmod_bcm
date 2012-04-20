#!/bin/sh
# OpenLGTV BCM 0.5.0-SVN20120420 installation script v.1.99 by xeros
# Based on extract.sh code from LGMOD S7 by mmm4m5m
# Source code released under GPL License

SKIP_LINES=111

echo "[ OpenLGTV BCM installer ]"

if [ "$1" = "--help" -o "$1" = "-help" -o "$1" = "-h" -o "$1" = "help" ]
then
    echo "Usage: $0 [option]"
    echo "Where [option] can be one of the following:"
    echo " extract     - just extract image to /tmp"
    echo " chroot      - extract+mount+chroot into new rootfs with shell, no install"
    echo " info        - gather much useful info for development into info.log file"
    echo " info paste  - as above + paste into pastebin.org and return url to logs"
    echo " noinstall   - check for prerequestities and make backup, no install"
    echo " install     - makes real installation"
    echo " nobackup    - skip doing backup before installation"
    echo " backup      - force making backup, even if it's already done"
    echo " drop_caches - drop caches during installation to free memory (unstable)"
    echo " help        - this usage information"
    exit 0
fi

export file_tarsh="$0"
# basename not available on 2009 BCM models
#export base="/tmp/`basename ${0%.tar.sh}`"
basef="${0##*/}"
export base="/tmp/${basef%.tar.sh}"
export file_sqf="${basef%.tar.sh}.sqf"
#export separator="----------------------------------------------------------------"
export separator="------------------------------------------------------------------------------"

[ -d "$base" ] && rm -rf $base

if [ "$1" = "drop_caches" -o "$2" = "drop_caches" ]
then
    echo "Dropping caches..."
    echo 3 > /proc/sys/vm/drop_caches
    sleep 1
fi
mkdir -p "$base"

echo "Extracting $0"
echo "to ${base}:"
echo "$separator"

#tail -n +51 "$0" | unzip -o - -d "$base" || { echo "Error: Extraction failed."; exit 1; }; sync #no unzip in orig fw
tail -n +$SKIP_LINES "$0" | tar xv -C "$base" || { echo "Error: Extraction failed."; exit 1; }; sync
echo "$separator"
echo "OpenLGTV BCM installation image has been extracted successfully."
echo "$separator"

[ "$1" = "extract" ] && exit 0

[ "`cat /proc/mtd 2>/dev/null | wc -l`" -lt "30" ] && echo "This installer is for Broadcom based LG TVs, do not run it on PC or Saturn platform based TVs" && exit 1

# enforce variables from settings file and export them for install.sh
if [ -f "/mnt/user/cfg/settings" ]
then
    source /mnt/user/cfg/settings
    for svar in `cat /mnt/user/cfg/settings | awk -F= '{print $1}'`; do export $svar; done
fi

# vars used by install.sh subprocess
export current_rootfs_ver="`cat /etc/ver | awk -F, '{print $1}'`"
export ver_installed="`cat /etc/ver2 2>/dev/null`"
dir="`dirname $0`"
[ -z "$dir" -o "$dir" = "." ] && dir="`pwd`"
export dir
export chrooted=1

CHR=/tmp/install-root
DIR="$base"
rootfs=$(echo "$DIR/"OpenLGTV_BCM*.sqf)

echo "Mounting root filesystem from squashfs image file and linking mountpoints..."

mkdir -p "$CHR" && mount -t squashfs "$rootfs" "$CHR" -o loop || { echo "Error: Mount root failed: $rootfs ($CHR)"; exit 1; }

mount -t proc    installproc   ${CHR}/proc
mount -t usbfs   installusbfs  ${CHR}/proc/bus/usb
mount -t devpts  installdevpts ${CHR}/dev/pts
mount -t sysfs   installsysfs  ${CHR}/sys

for i in `cat /proc/mounts | awk '{print $2}' | grep -v "^/$" | grep -v "proc" | grep -v "sysfs" | grep -v "devpts" | grep -v "/var"`; do mount --bind $i ${CHR}${i}; done

#TODO: use /scripts/install.sh and remove install.sh from zip file - need to add path handling in install.sh
#chroot "$CHR" "$CHR/scripts/install.sh" "$base/$file_sqf" "$@"
chmod 755 "${CHR}${base}/install.sh"
# v- on pure LG rootfs /usr/sbin is not in $PATH
if [ "$1" = "chroot" ]
then
    echo "Starting shell inside chrooted (virtual) root filesystem environment..."
    echo "$separator"
    cat "$CHR/etc/motd"
    /usr/sbin/chroot "$CHR" /bin/sh --login
else
    echo "Running second part of installer:"
    echo "$base/install.sh $@"
    echo "$separator"
    /usr/sbin/chroot "$CHR" "$base/install.sh" "$@"
fi
#TODO: umount,...
tac=`which tac`; [ -z "$tac" ] && tac="$CHR/usr/bin/tac" # on LG rootfs there's no 'tac'
for i in `grep " $CHR" /proc/mounts | awk '{print $2}' | $tac`; do umount ${i}; done

exit;

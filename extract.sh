#!/bin/sh
# OpenLGTV BCM 0.5.0-beta installation script v.1.93 by xeros
# Based on extract.sh code from LGMOD S7 by mmm4m5m
# Source code released under GPL License

SKIP_LINES=96

echo "OpenLGTV BCM installator"

if [ "$1" = "--help" -o "$1" = "-help" -o "$1" = "-h" -o "$1" = "help" ]
then
    echo "Usage: $0 [option]"
    echo "Where [option] can be one of the following:"
    echo " extract     - just extracts image to /tmp"
    echo " chroot      - extracts, mounts, chroots into new rootfs with /bin/sh only, no installation"
    echo " no_install  - as above but checks for prerequestities and makes backup if running on LG firmware then exits just before flashing"
    echo " install     - makes real installation"
    echo " no_backup   - skip doing backup before installation"
    echo " drop_caches - drop caches during installation to free more memory (unstable)"
    echo " help        - this usage information"
    exit 0
fi

#echo 'Extracting ...'; export base="/tmp/`basename ${0%.sh.zip}`"; export file_sqf="`basename ${0%.sh.zip}`.sqf"
export base="/tmp/`basename ${0%.tar.sh}`"
export file_sqf="`basename ${0%.tar.sh}`.sqf"

echo "Extracting $0 into $base ..."

[ -d "$base" ] && rm -rf $base

if [ "$1" = "drop_caches" -o "$2" = "drop_caches" ]
then
    echo "Dropping caches..."
    echo 3 > /proc/sys/vm/drop_caches
    sleep 1
fi
mkdir -p "$base"

#tail -n +51 "$0" | unzip -o - -d "$base" || { echo "Error: Extraction failed."; exit 1; }; sync #no unzip in orig fw
tail -n +$SKIP_LINES "$0" | tar xv -C "$base" || { echo "Error: Extraction failed."; exit 1; }; sync
echo "OpenLGTV BCM installation image has been extracted."

[ "$1" = "extract" ] && exit 0

[ "`cat /proc/mtd 2>/dev/null | wc -l`" -lt "30" ] && echo "This is OpenLGTV BCM firmware installation file, do not run it on PC or Saturn platform based TVs" && exit 1

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
if [ -z "$dir" -o "$dir" = "." ]
then
    dir="`pwd`"
fi
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

for i in `cat /proc/mounts | awk '{print $2}' | grep -v "^/$" | grep -v "proc" | grep -v "sysfs" | grep -v "devpts"`; do mount --bind $i ${CHR}${i}; done

#TODO: use /scripts/install.sh and remove install.sh from zip file - need to add path handling in install.sh
#chroot "$CHR" "$CHR/scripts/install.sh" "$base/$file_sqf" "$@"
chmod 755 "${CHR}${base}/install.sh"
# v- on pure LG rootfs /usr/sbin is not in $PATH
if [ "$1" = "chroot" ]
then
    echo "Starting shell inside chrooted (virtual) root filesystem environment..."
    /usr/sbin/chroot "$CHR" /bin/sh
else
    echo "Starting installation: $base/install.sh $@"
    /usr/sbin/chroot "$CHR" "$base/install.sh" "$@"
fi
#TODO: umount,...

exit;

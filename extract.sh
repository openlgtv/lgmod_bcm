#!/bin/sh
# OpenLGTV BCM 0.5.0-alpha3 installation script v.1.82 by xeros
# Based on extract.sh code from LGMOD S7 by mmm4m5m
# Source code released under GPL License

#echo 'Extracting ...'; export base="/tmp/`basename ${0%.sh.zip}`"; export file_sqf="`basename ${0%.sh.zip}`.sqf"
echo 'Extracting ...'; export base="/tmp/`basename ${0%.tar.sh}`"; export file_sqf="`basename ${0%.tar.sh}`.sqf"
mkdir -p "$base"; echo 3 > /proc/sys/vm/drop_caches; sleep 1

SKIP_LINES=52

#tail -n +51 "$0" | unzip -o - -d "$base" || { echo "Error: Extraction failed."; exit 1; }; sync #no unzip in orig fw
tail -n +$SKIP_LINES "$0" | tar xv -C "$base" || { echo "Error: Extraction failed."; exit 1; }; sync

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

mkdir -p "$CHR" && mount -t squashfs "$rootfs" "$CHR" || { echo "Error: Mount root failed: $rootfs ($CHR)"; exit 1; }

for i in `cat /proc/mounts | awk '{print $2}' | grep -v "^/$"`; do mount --bind $i ${CHR}${i}; done

#TODO: use /scripts/install.sh and remove install.sh from zip file - need to add path handling in install.sh
#chroot "$CHR" "$CHR/scripts/install.sh" "$base/$file_sqf" "$@"
chmod 755 "${CHR}${base}/install.sh"
# v- on pure LG rootfs /usr/sbin is not in $PATH
/usr/sbin/chroot "$CHR" "$base/install.sh" "$@"

#TODO: umount, autoupgrade, rest...

exit;

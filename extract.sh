#!/bin/sh
# OpenLGTV BCM 0.5.0-devel installation script v.1.80 by xeros
# Based on extract.sh code from LGMOD S7 by mmm4m5m
# Source code released under GPL License

[ "`cat /proc/mtd 2>/dev/null | wc -l`" -lt "30" ] && echo "This is OpenLGTV BCM firmware installation file, do not run it on PC or Saturn platform based TVs" && exit 1

echo 'Extracting ...'; export base="/tmp/`basename ${0%.sh.zip}`"; export file_sqf="`basename ${0%.sh.zip}`.sqf"
mkdir -p "$base"; echo 3 > /proc/sys/vm/drop_caches; sleep 1
unzip -o "$0" -d "$base"; sync

# enforce variables from settings file and export them for install.sh
if [ -f "/mnt/user/cfg/settings" ]
then
    source /mnt/user/cfg/settings
    for svar in `cat /mnt/user/cfg/settings | awk -F= '{print $1}'`; do export $svar; done
fi

# vars used by install.sh subprocess
export current_rootfs_ver="`cat /etc/ver | awk -F, '{print $1}'`"
export ver_installed="`cat /etc/ver2 2>/dev/null`"
export dir="`dirname $0`"
export chrooted=1

CHR=/tmp/install-root
DIR="$base"
rootfs=$(echo "$DIR/"OpenLGTV_BCM*.sqf)

mkdir -p "$CHR" && mount -t squashfs "$rootfs" "$CHR" || err=5
[ $err = 0 ] || { echo "Error($err): Mount root failed: $rootfs ($CHR)"; exit $err; }

for i in `cat /proc/mounts | awk '{print $2}' | grep -v "^/$"`; do mount --bind $i ${CHR}${i}; done

#TODO: use /scripts/install.sh and remove install.sh from zip file - need to add path handling in install.sh
#chroot "$CHR" "$CHR/scripts/install.sh" "$base/$file_sqf" "$@"
chroot "$CHR" "$base/install.sh" "$@"


#TODO: umount, autoupgrade, rest...

exit;

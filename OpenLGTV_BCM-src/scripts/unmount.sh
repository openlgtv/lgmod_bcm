#!/bin/sh
# OpenLGTV BCM unmount.sh script by xeros
# Source code released under GPL License

what="$1"
what_pre="$1"
[ -z "$what" ] && what=" /" && matched=1
[ -z "$matched" ] && [ "${what:0:1}" = " " ] && matched=2
[ -z "$matched" ] && [ "${what:0:1}" = "^" ] && matched=3
[ -z "$matched" ] && [ "${what:0:4}" = "/dev" ] && what="${what}" && matched=4
[ -z "$matched" ] && [ "${what:0:4}" = "/mnt" ] && what="^`grep \" $what\" /proc/mounts | cut -d\" \" -f1` " && matched=5
[ -z "$matched" ] && [ "${what:0:1}" = "/" ] && what=" $what" && matched=6
[ -z "$matched" ] && [ -n "`awk \"/\t${what}\$/\" /proc/filesystems`" ] && what=" $what " && matched=7
[ -z "$matched" ] && mtdpart="`grep -m1 \"\\\"$what\\\"\" /proc/mtd | sed 's/^mtd/mtdblock/'`" && [ -n "$mtdpart" ] && what="^/dev/${mtdpart%%:*} " && matched=8

echo "OpenLGTV_BCM-INFO: Unmount script: matched input \"$what_pre\" as \"$what\", match pattern number: \"$matched\" - unmounting partitions..."

for dst in `grep "$what" /proc/mounts | cut -d" " -f2 | tac`
do
    echo "OpenLGTV_BCM-INFO: Unmount script: unmounting $dst"
    umount -r "$dst"
done

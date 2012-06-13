#!/bin/sh
# OpenLGTV BCM unmount.sh script by xeros
# Source code released under GPL License

umnt_bg=0
[ "$1" = "-bg" ] && umnt_bg=1 && shift
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
    if [ "${what_pre:0:7}" = "/dev/sd" ]
    then
	echo "OpenLGTV_BCM-INFO: Unmount script: checking processes that use \"$what_pre\" devices in mountpoint: \"$dst\""
	# simplier would be with 'fuser -k' but first need to check if RELEASE or other essential process is not using it
	for prc in `fuser -m "$dst"`
	do
	    prc_line=`ps www | grep "^ $prc "`
	    echo "OpenLGTV_BCM-INFO: Unmount script: killing process: \"$prc_line\""
	    kill "$prc"
	done
    fi
    echo "OpenLGTV_BCM-INFO: Unmount script: unmounting \"$dst\""
    if [ "$umnt_bg" -eq 1 ]
    then
	umount -f -r "$dst" &
    else
	umount -f -r "$dst"
    fi
done

sync

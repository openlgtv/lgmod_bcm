#!/bin/sh
# Source code released under GPL License
# Info script for Saturn6/Saturn7/BCM by mmm4m5m,xeros

# modify with care - script is used by install.sh

VER='v11'; # version of info file (file syntax)
busybox=''; #/bin/busybox; # old
MODEL=`echo /mnt/lg/user/model.*`
MODEL_BCM=/mnt/user/etc/model
[ -f "$MODEL" ] && MODEL="${MODEL#*model.}" || MODEL=''
[ -z "$MODEL" -a -f "$MODEL_BCM" ] && MODEL="`cat "$MODEL_BCM"`"

part="$1"
if   [ "$1" = root ];    then shift; # part 1 - before chroot
elif [ "$1" = chroot ];  then shift; # part 2 - in chroot - part 1 (from $infotemp) will be included
elif [ "$1" = paste ];   then shift; # all info (parts 1+2) - upload to pastebin.com (pastebin.ca)
elif [ "$1" = mtdinfo ]; then shift; # mtdinfo only - optional: $1=bin_file $2=number_of_partitions
elif [ "$1" = dumprel ]; then shift; # dumprel only - optional: $1=release_file
else part=''; fi; # all info (parts 1+2)

infotemp=/tmp/info-file
infofile="$1"; [ -z "$1" ] && infofile="$infotemp"
wgetfile="$infofile.wget"; # encoded/prepared for wget --post-data



# stand alone commands (could be in separate file)
DROP() {
	if [ "`uname -r | awk '{print substr($1,5,2)}'`" -gt 28 ]; then # not S6/S7/SmartTV = BCM - drop_caches is broken on newer kernels
		return 1
	else
		echo 3 > /proc/sys/vm/drop_caches
	fi
}

Err() { local e=$? m="$2"; [ $1 -gt $err ] && err=$1; [ -z "$m" ] && m="$1"; echo "Error($e): $m" >&2; return $e; }

mtdinfo() {
	local err=0 info ver f="$1" c="$2"
	if [ -z "$f" ]; then
		f=/dev/`grep -m1 '"mtdinfo"' /proc/mtd | cut -d: -f1`
		if [ -d /mnt/user ]; then # not S6/S7 = BCM
			[ "$f" = /dev/mtd1 ] || Err 9 "mtdinfo in $f: Not BCM TV?"
		else
			[ "$f" = /dev/mtd2 ] || Err 9 "mtdinfo in $f: Not S7 TV?"
		fi
	fi
	if [ -z "$c" ]; then
		c=`grep -v 'erasesize\|total' /proc/mtd | wc -l`
		if [ -d /mnt/user ]; then # not S6/S7 = BCM
			:; # TODO
		else
			[ $c = 26 ] || [ $c = 24 ] || Err 7 "$c-1 partitions: Not S7 TV?"
		fi
	fi

	[ -e "$f" ] || { Err 8 "file not found: $f"; return $?; }
	info=`$busybox hexdump $f -vs4 -n8 -e'"%x"'` || { Err 6 "read from $f"; return $?; }

	# shell substring makes problem with running script on old busybox (stock BCM 2010 and 2011 rootfs)
	#ver=${info:0:7}; echo "Current  EPK version: ${ver:0:1}.${ver:1:2}.${ver:3:2}.${ver:5:2}"
	#ver=${info:7:7}; echo "Previous EPK version: ${ver:0:1}.${ver:1:2}.${ver:3:2}.${ver:5:2}"
	cur_epk=`echo $info | awk '{printf "%s.%s.%s.%s",substr($0,1,1),substr($0,2,2),substr($0,4,2),substr($0,6,2)}'` || Err 5 "invalid data"
	old_epk=`echo $info | awk '{printf "%s.%s.%s.%s",substr($0,8,1),substr($0,9,2),substr($0,11,2),substr($0,13,2)}'` || Err 4 "invalid data"
	echo "Current  EPK version: $cur_epk"
	echo "Previous EPK version: $old_epk"

	info=`$busybox hexdump $f -vs240 -e'32 "%_p" " %08x ""%08x " 32 "%_p" " %8d"" %8x " /1 "Uu:%x" /1 " %x " /1 "CIMF:%x" /1 " %x" "\n"' | head -n$c`
	echo "00:$info" | head -n1; echo "$info" | tail -n+2 | grep '' -n | sed -e 's/^[0-9]:/0\0/'

	echo; echo "MTDINFO additional strings:"
	dd bs=$(( 240 + 84*c )) skip=1 if=$f 2>/dev/null | strings || Err 3 "invalid strings"
	return $err
}

dumprel() {
	local err=0 info_REL s b i none f="$1"
	if [ -z "$f" ]; then
		f=/mnt/lg/lgapp/bin/RELEASE
		[ -f "$f" ] || f=/mnt/lg/lgapp/RELEASE
	fi
	[ -e "$f" ] || { Err 8 "file not found: $f"; return $?; }
	info_REL=/scripts/info_RELEASE.sh
	[ -f "$info_REL" ] || info_REL=/home/lgmod/info_RELEASE.sh

	if [ -x /usr/bin/bbe -a -x "$info_REL" ]; then
		# TODO - include info_REL script here
		$info_REL "$f"
	else
		s=$(stat -c%s "$f"); b=$((s/18)); none=1
		for i in 9 10 11 12; do
			DROP; dd bs=$b skip=$i count=1 if="$f" || { Err 18; break; }
			cat /tmp/info-dump | tr [:space:] ' '|tr -c ' [:alnum:][:punct:]' '\n'| \
				grep '....'|grep -v '.\{30\}'|grep -m1 -B1 -A5 swfarm && none=0 && break
		done
		[ $none = 1 ] && Err 18; none=1
		for i in 15 16 14; do
			DROP; dd bs=$b skip=$i count=1 if="$f" || { Err 18; break; }
			cat /tmp/info-dump | tr [:space:] ' '|tr -c ' [:alnum:][:punct:]' '\n'| \
				grep '....'|grep -v '.\{30\}'|grep -m1 -B1 -A10 swfarm && none=0 && break
		done
		rm -f /tmp/info-dump; [ $none = 1 ] && Err 18 'info not found'
	fi
	return $err
}



save=''; # Note: last 'INFO' is saved and used if 'ERR'
INFO() { { echo; echo; echo "$@"; } >> "$infofile"; save="$@"; }
ERR() {
	local e=$? m="$2"; [ $1 -gt $err ] && err=$1
	[ -n "$save" ] && echo "$save" && save=''
	[ -z "$m" ] && m="Error($1): exitcode=$e"
	echo "$m" >> "$infofile"; echo "$m"
}

err=0
CMD() {
	local e="$1"; shift; INFO '$#' "$@"
	$@ >> "$infofile" 2>&1 || ERR "$e"
}



# info file parts
INFO_ROOT() {
	# part 1 (outside install.sh chroot) - stock busybox and all mount points as is (if RELEASE works)
	INFO '$# df -h'; tmp=`df -h` 2>> "$infofile" || ERR 12; echo "$tmp" | grep -v '^/dev/sd' >> "$infofile"
	CMD 12 busybox
	CMD 10 help

	for i in /var/www/cgi-bin/version /etc/version_for_lg /mnt/lg/model/* \
		/mnt/lg/user/lgmod/boot /mnt/lg/user/lgmod/init/* \
		/tmp/openrelease.log /var/log/OPENRELEASE.log \
		/mnt/lg/cmn_data/openrelease.cfg /mnt/lg/cmn_data/openrelease_keymap.cfg \
		/mnt/user/etc/openrelease/openrelease.cfg /mnt/user/etc/openrelease/openrelease_keymap.cfg \
		/mnt/user/cfg/settings /mnt/user/etc/opkg/opkg.conf \
		/etc/ver /etc/version /etc/ver2 /mnt/user/etc/ver2; do
		[ -f "$i" ] || continue
		echo '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' >> "$infofile"
		CMD 16 cat $i
	done
	echo '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' >> "$infofile"
	i=/var/log/OpenLGTV_BCM.log; [ -f $i ] || i=/tmp/openrelease.out; [ -f $i ] && CMD 16 cat $i
	echo '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' >> "$infofile"

	for i in /etc /mnt/lg/lginit /mnt/lg/bt /mnt/lg/user /mnt/lg/cmn_data /mnt/lg/model \
			/mnt/lg/lgapp /mnt/lg/res/lgres /mnt/lg/res/lgfont /usr/local \
			/mnt/addon/bin /mnt/addon/lib /mnt/addon/stagecraft /mnt/addon/netflix /mnt/addon/vcs \
			/mnt/addon/vudu /mnt/addon/ywe /mnt/addon/browser /mnt/addon/krbrowser /mnt/browser /home \
			/mnt/game /mnt/cache /mnt/idfile \
			/mnt/nsu /mnt/lg/lglib /mnt/tplist /mnt/pqldb /mnt/lg/widevine \
			/mnt/usb1/Drive1/OpenLGTV_BCM \
			/mnt/usb1/Drive2/OpenLGTV_BCM \
			/mnt/usb1/Drive3/OpenLGTV_BCM \
			/mnt/usb1/Drive4/OpenLGTV_BCM \
			/mnt/usb2/Drive1/OpenLGTV_BCM \
			/mnt/usb2/Drive2/OpenLGTV_BCM \
			/mnt/usb2/Drive3/OpenLGTV_BCM \
			/mnt/usb2/Drive4/OpenLGTV_BCM \
			/tmp/extroot; do
		[ -f "$i" ] || [ -d "$i" ] || continue
		[ -d "$i/" ] && i="$i/"; CMD 16 ls -lR $i; done
	for i in /mnt/addon/ /mnt/addon/contents/ /mnt/lg/ciplus/ /mnt/lg/res/estreamer/ /tmp/; do
		[ -f "$i" ] || [ -d "$i" ] || continue
		[ -d "$i/" ] && i="$i/"; CMD 16 ls -l $i; done
}

INFO_CHROOT_HEADER() {
	# part 2 (inside install.sh chroot) - header (after INFO_ROOT)
	dmesg > $infotemp.dmesg; # get dmesg in advance in case small buffer

	# important info - before dmesg, dump files/directories, INFO_ROOT
	DROP && sleep 1
	CMD 11 cat /proc/mtd
	CMD 13 mtdinfo

	INFO '#$ dump the magic: /dev/mtd#'
	for i in `cat /proc/mtd | grep '^mtd' | sed -e 's/:.*//' -e 's/^/\/dev\//'`; do
		{ echo -n "$i: "; $busybox hexdump $i -vn32 -e'32 "%4_c" "\n"'; } >> "$infofile" 2>&1 || ERR 13; done

	INFO "INFO: `date`"
	CMD 12 free
	CMD 11 cat /proc/cpuinfo
	CMD 12 lsmod
	CMD 11 cat /proc/version
	INFO '$# cat /proc/cmdline'; tmp=`cat /proc/cmdline` 2>> "$infofile" || ERR 11; printf '%s\n' $tmp >> "$infofile"
	CMD 12 hostname
	CMD 11 cat /proc/filesystems
	INFO '$# export'; tmp=`export` 2>> "$infofile" || ERR 10; echo "$tmp" | sort >> "$infofile"
	INFO '$# printenv'; tmp=`printenv` 2>> "$infofile" || ERR 12; echo "$tmp" | sort >> "$infofile"
	if [ -h `which ps` ]; then CMD 12 ps www; else CMD 12 ps axl; CMD 12 ps axv; fi
	CMD 11 cat /proc/mounts
	INFO '$# fdisk -l'
	tmp=`fdisk -l $(cat /proc/mtd | tail -n+2 | sed -e 's/:.*//' -e 's/^mtd/\/dev\/mtdblock/')` 2>> "$infofile" || ERR 14
	echo "$tmp" | grep ':' >> "$infofile"

	# uncategorized info (most important info is above)
	for i in /proc/version_for_lg /proc/meminfo /proc/iomem /proc/interrupts /proc/bbminfo /proc/bus/usb/devices \
		/proc/modules /proc/hwinfo /proc/stat /proc/partitions /proc/devices /proc/sys/kernel/panic \
		/proc/bcmdriver/version /proc/bcmdriver/meminfo /sys/devices/platform/brcmstb/cfe_boardname \
		/sys/class/mtd/mtd0/type /sys/class/mtd/mtd0/flags /sys/class/mtd/mtd0/size /sys/class/mtd/mtd0/erasesize \
		/sys/class/mtd/mtd0/writesize /sys/class/mtd/mtd0/oobsize /sys/class/mtd/mtd0/numeraseregions \
		/sys/class/mtd/mtd0/subpagesize /sys/class/mtd/mtd0/name ; do
		[ -f "$i" ] || continue; CMD 11 cat $i; done

	INFO '$# dmesg'
	cat $infotemp.dmesg | grep ACTIVE >> "$infofile"; # in S7 this shows 'TV statup time' (picture on the screen)
	cat $infotemp.dmesg >> "$infofile" 2>&1 || ERR 15
	echo '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' >> "$infofile"
}

INFO_CHROOT_FOOTER() {
	# part 2 (inside install.sh chroot) - footer (after INFO_ROOT)
	f=/mnt/lg/lgapp/bin/RELEASE; [ -f "$f" ] || f=/mnt/lg/lgapp/RELEASE
	info_REL=/scripts/info_RELEASE.sh; [ -f "$info_REL" ] || info_REL=/home/lgmod/info_RELEASE.sh
	if [ -f "$f" ] && [ -x /usr/bin/bbe -a -x "$info_REL" ]; then
		CMD 18 $info_REL $f
	elif [ -f "$f" ]; then
		INFO '#$ dump RELEASE version'
		s=$(stat -c%s $f); b=$((s/18)); none=1
		for i in 9 10 11 12; do
			DROP; dd bs=$b skip=$i count=1 if=$f > /tmp/info-dump 2>> "$infofile" || { ERR 18; break; }
			cat /tmp/info-dump | tr [:space:] ' '|tr -c ' [:alnum:][:punct:]' '\n'| \
				grep '....'|grep -v '.\{30\}'|grep -m1 -B1 -A5 swfarm >> "$infofile" && none=0 && break
		done
		[ $none = 1 ] && ERR 18 || none=1
		for i in 15 16 14; do
			DROP; dd bs=$b skip=$i count=1 if=$f > /tmp/info-dump 2>> "$infofile" || { ERR 18; break; }
			cat /tmp/info-dump | tr [:space:] ' '|tr -c ' [:alnum:][:punct:]' '\n'| \
				grep '....'|grep -v '.\{30\}'|grep -m1 -B1 -A10 swfarm >> "$infofile" && none=0 && break
		done
		rm -f /tmp/info-dump; [ $none = 1 ] && ERR 18 'Error: not found'
	else ERR 0 'Note: not found'; fi

	INFO "INFO: `date`"
	f=/mnt/lg/lginit/lg-init; [ -f $f ] || f=/mnt/lg/lginit/lginit
	INFO '#$' "strings $f"
	if [ -f "$f" ]; then
		DROP; md5sum $f >> "$infofile" || ERR 18
		w=5;m=3;cat $f |tr [:space:] ' '|tr -c ' [:alnum:][:punct:]' '\n'|sed -e'/[a-zA-Z]\{'$m'\}\|[0-9]\{'$m'\}/!d' \
			-e'/[-_=/\.:0-9a-zA-Z]\{'$w'\}/!d' -e's/  \+/ /g'| head -n70 >> "$infofile" || ERR 18
	else ERR 0 'Note: not found'; fi
	# TODO - replace above lines with: CMD 18 dumprel $f

	INFO "INFO: `date`"

	f=`grep -m1 '"boot"' /proc/mtd | cut -d: -f1`
	INFO '#$' "strings boot(version) : /dev/$f"
	if [ -d /mnt/user ]; then # not S6/S7 = BCM
		[ "$f" = mtd0 ] || ERR 17 "Error: boot in $f: Not BCM TV?"
	else
		[ "$f" = mtd1 ] || ERR 17 "Error: boot in $f: Not S7 TV?"
	fi
	if [ -c "/dev/$f" ]; then
		DROP; s=7;w=5;m=3;cat /dev/$f |tr [:space:] ' '|tr -c ' [:alnum:][:punct:]' '\n'| \
			sed -e'/[a-zA-Z]\{'$m'\}\|[0-9]\{'$m'\}/!d' -e'/[-_=/\.:0-9a-zA-Z]\{'$w'\}/!d' \
			-e's/  \+/ /g' -e'/.\{'$s'\}/!d'| head -n5 >> "$infofile" || ERR 18
		DROP; s=7;w=5;m=3;cat /dev/$f |tr [:space:] ' '|tr -c ' [:alnum:][:punct:]' '\n'| \
			sed -e'/[a-zA-Z]\{'$m'\}\|[0-9]\{'$m'\}/!d' -e'/[-_=/\.:0-9a-zA-Z]\{'$w'\}/!d' \
			-e's/  \+/ /g' -e'/.\{'$s'\}/!d'| tail -n35 >> "$infofile" || ERR 18
	fi

	F1="$f"; f=`grep -m2 '"boot"' /proc/mtd | cut -d: -f1 | tail -n+2`; F2="$f"
	if [ -d /mnt/user ]; then # not S6/S7 = BCM
		[ -z "$f" ] || ERR 17 "Error: boot backup in $f: Not BCM TV?"
	else
		INFO '#$' "strings(version) boot backup: /dev/$f"
		[ "$f" = mtd5 ] || ERR 17 "Error: boot backup in $f: Not S7 TV?"
	fi
	if [ -c "/dev/$f" ]; then
		DROP; s=7;w=5;m=3;cat /dev/$f |tr [:space:] ' '|tr -c ' [:alnum:][:punct:]' '\n'| \
			sed -e'/[a-zA-Z]\{'$m'\}\|[0-9]\{'$m'\}/!d' -e'/[-_=/\.:0-9a-zA-Z]\{'$w'\}/!d' \
			-e's/  \+/ /g' -e'/.\{'$s'\}/!d'| head -n5 >> "$infofile" || ERR 18
		DROP; s=7;w=5;m=3;cat /dev/$f |tr [:space:] ' '|tr -c ' [:alnum:][:punct:]' '\n'| \
			sed -e'/[a-zA-Z]\{'$m'\}\|[0-9]\{'$m'\}/!d' -e'/[-_=/\.:0-9a-zA-Z]\{'$w'\}/!d' \
			-e's/  \+/ /g' -e'/.\{'$s'\}/!d'| tail -n35 >> "$infofile" || ERR 18
	fi

	if [ -c "/dev/$F1" ] && [ -c "/dev/$F2" ]; then
		DROP; INFO '$#' "diff /dev/$F1 /dev/$F2"
		diff /dev/$F1 /dev/$F2 >> "$infofile" 2>&1 || ERR 0
	fi

	F=crc32info; f=`grep "\"$F\"" /proc/mtd | cut -d: -f1`
	if [ -n "$f" ]; then
		INFO '#$' "hexdump -n256 /dev/$f ($F)"
		hexdump -n256 -e '1/8  "%02.2_ax:  "' -e '16/1 "%02X "' -e '"\n"' /dev/$f >> "$infofile" || ERR 31; fi
	for F in env_nvm hist cfginfo; do
		f=`grep "\"$F\"" /proc/mtd | cut -d: -f1`; [ -n "$f" ] || continue
		INFO '#$' "strings /dev/$f ($F)"; strings /dev/$f >> "$infofile" || ERR 32; done
}



# info file variants - without chroot or with chroot (called twice from install.sh)=
INFO_CHROOT() {
	INFO_CHROOT_HEADER
	[ -f $infotemp ] && CMD 11 cat $infotemp
	INFO_CHROOT_FOOTER
}

INFO_ALL() {
	INFO_CHROOT_HEADER
	INFO_ROOT
	INFO_CHROOT_FOOTER
}



# process command line parameters
[ "$part" = mtdinfo ] && { mtdinfo "$@"; exit $?; }
[ "$part" = dumprel ] && { dumprel "$@"; exit $?; }
[ "$part" != root ] && echo "NOTE: Create info file (1 min, $infofile) ..."

echo "$VER $MODEL: $@" > "$infofile" || { echo "Error: Info file failed: $infofile"; exit 19; }
INFO "INFO: `date`"
if   [ "$part" = root ];   then INFO_ROOT
elif [ "$part" = chroot ]; then INFO_CHROOT
else INFO_ALL; fi
INFO "INFO: `date`"; DROP; sync

[ $err = 0 ] || echo "Error($err): Info file failed: $infofile"
[ "$part" != root ] && [ $err = 0 ] && echo "Done: Info file: $infofile"


if [ "$part" = paste ]; then
	which wget >/dev/null || { echo "NOTE: wget not found (extroot?)" && exit 1; }
	name="$MODEL"; [ -z "$name" ] && name=`hostname`; [ -z "$name" ] && name='NA'

	#URL='http://pastebin.ca/quiet-paste.php?api=GO2sUUgKHm5v4WAAXooevnRBoI0bdGhc'; # type=23 - bash (?)
	#echo -n "name=$name&type=&description=/tmp/OpenLGTV-info-file.txt&expiry=1+month&s=Submit+Post&content=" > "$wgetfile" || exit

	URL='http://pastebin.com/api_public.php'; # paste_format=bash (?)
	echo -n "paste_name=$name&paste_format=text&paste_expire_date=1M&paste_private=1&paste_code=" > "$wgetfile" || exit

	cat "$infofile" | sed -e 's|%|%25|g' -e 's|&|%26|g' -e 's|+|%2b|g' -e 's| |+|g' >> "$wgetfile" &&
		echo wget -O /tmp/info-file.pbin --timeout=30 --post-data=\"\`cat $wgetfile\`\" "'$URL'" &&
		wget -O /tmp/info-file.pbin --timeout=30 --post-data="`cat $wgetfile`" "$URL" &&
		echo 'NOTE: To share your info file, please find the link below:'
	cat /tmp/info-file.pbin | head; echo
fi

#!/bin/sh
# links_images_preload.sh script by xeros
# Source code released under GPL License

#TODO: make some logging and make local links in html file without need of sed, remove comments
#TODO: make running this script only when version changes or no icons_dir/file, not on each boot ?

echo "OpenLGTV_BCM-INFO: links_icons_preload.sh: running..."

icons_dir="/home/netcast_icons/www"

ilink1="http://smarttv.net46.net/smarttv_logos.zip"
ilink2="http://dl.dropbox.com/u/43758310/smarttv_logos.zip"
ilink3="http://smarttv.awardspace.info/smarttv_logos.xxx"

imd5="a3f458d48113421c5a3a131bc5b44864"

useragent="Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"

ilinks_count=3

if [ ! -d "$icons_dir" -o "$uver" != "$ver" ]
then
    echo "OpenLGTV_BCM-INFO: links_icons_preload.sh: OpenLGTV BCM upgrade/downgrade detected - downloading currently supported icons..."
    while [ -z "$PING_OK" ]
    do
	rnd=$RANDOM
	let "rnd %= $ilinks_count"
	case $rnd in
	0)
	    ilink="$ilink1";;
	1)
	    ilink="$ilink2";;
	*)
	    ilink="$ilink3";;
	esac
	ihost="`echo $ilink | awk -F/ '{print $3}'`"
	# ugly workaround for disabled pings on dl.dropbox.com
	[ "$ihost" = "dl.dropbox.com" ] && ihost="dropbox.com"
	echo "OpenLGTV_BCM-INFO: links_icons_preload.sh: trying to use download link: $ilink"
	PING_OK="`ping -4 -c 1 $ihost 2>/dev/null | grep '64 bytes from'`"
	sleep 3
    done

    cur_dir=`pwd`
    mkdir -p "$icons_dir"
    cd "$icons_dir"
    wget -q -c -U "$useragent" "$ilink" -O /tmp/icons.zip
    md5s="`md5sum /tmp/icons.zip`"
    if [ "${md5s:0:32}" != "$imd5" ]
    then
	echo "OpenLGTV_BCM-ERROR: links_icons_preload.sh: icons downloaded but zip file checksum mismatch: ${md5s:0:32} != $imd5"
	rm /tmp/icons.zip
	exit 1
    else
	echo "OpenLGTV_BCM-INFO: links_icons_preload.sh: icons downloaded and checksum is OK, unzipping..."
	unzip -n /tmp/icons.zip
	rm /tmp/icons.zip
    fi
fi

cd $cur_dir

echo "OpenLGTV_BCM-INFO: links_icons_preload.sh: exit"

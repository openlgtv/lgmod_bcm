#!/bin/sh
# links_images_preload.sh script by xeros
# Source code released under GPL License

echo "OpenLGTV_BCM-INFO: icons_download.sh: running..."

icons_dir="/home/netcast_icons/www"
#ilink1="http://dl.dropbox.com/u/43758310/smarttv_logos.zip"
#ilink2="http://smarttv.awardspace.info/smarttv_logos.xxx"
ilink1="http://svn.openlgtv.org.ru/OpenLGTV_BCM/trunk/addons/images/www/icons.zip"
ilink2="http://svn.openlgtv.org.ru/OpenLGTV_BCM/trunk/addons/images/www/icons.zip"
ilink3=""
#imd5="a3f458d48113421c5a3a131bc5b44864"
imd5="7c19bece3f7b27cdf9196b07868026f2"
useragent="Mozilla/5.0 (X11; Linux x86; rv:10.0.2) Gecko/20100101 Firefox/10.0.2"
#ilinks_count=3
ilinks_count=2

if [ ! -d "$icons_dir" -o "$uver" != "$ver" -o ! -f "$icons_dir/unknown.png" ]
then
    echo "OpenLGTV_BCM-INFO: icons_download.sh: OpenLGTV BCM upgrade/downgrade detected - downloading currently supported icons..."
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
	echo "OpenLGTV_BCM-INFO: icons_download.sh: trying to use download link: $ilink"
	[ -n "$ihost" ] && PING_OK="`ping -4 -c 1 $ihost 2>/dev/null | grep '64 bytes from'`"
	sleep 3
    done
    cur_dir=`pwd`
    mkdir -p "$icons_dir"
    cd "$icons_dir"
    wget -q -c -U "$useragent" "$ilink" -O /tmp/icons.zip
    md5s="`md5sum /tmp/icons.zip`"
    if [ "${md5s:0:32}" != "$imd5" ]
    then
	echo "OpenLGTV_BCM-ERROR: icons_download.sh: icons downloaded but zip file checksum mismatch: ${md5s:0:32} != $imd5"
	rm /tmp/icons.zip
	exit 1
    else
	echo "OpenLGTV_BCM-INFO: icons_download.sh: icons downloaded and checksum is OK, unzipping..."
	unzip -n /tmp/icons.zip
	rm /tmp/icons.zip
    fi
fi
cd $cur_dir
echo "OpenLGTV_BCM-INFO: icons_download.sh: exit"

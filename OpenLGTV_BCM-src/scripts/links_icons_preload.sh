#!/bin/sh
# links_images_preload.sh script by xeros
# Source code released under GPL License

#TODO: make some logging and make local links in html file without need of sed, remove comments
#TODO: make running this script only when version changes or no icons_dir/file, not on each boot ?

#icons_dir="/tmp/links_icons"
icons_dir="/home/netcast_icons/www"

ilink1="http://smarttv.net46.net/smarttv_logos.zip"
ilink2="http://dl.dropbox.com/u/43758310/smarttv_logos.zip"
ilink3="http://smarttv.awardspace.info/smarttv_logos.xxx"

imd5="a3f458d48113421c5a3a131bc5b44864"

useragent="Mozilla/5.0 (X11; Linux x86_64; rv:7.0) Gecko/20100101 Firefox/7.0"

ilinks_count=3

rnd=$RANDOM
let "rnd %= $ilinks_count"

if [ ! -f "$icons_dir/links.html" ]
then
    #while [ -z "`ping -4 -c 1 www.ottomano.it 2>/dev/null | grep '64 bytes from'`" ]
    while [ -z "$PING_OK" ]
    do
	case $rnd in
	0)
	    ilink="$ilink1";;
	1)
	    ilink="$ilink2";;
	*)
	    ilink="$ilink3";;
	esac
	PING_OK="`ping -4 -c 1 $ilink 2>/dev/null | grep '64 bytes from'`"
	sleep 3
    done

    cur_dir=`pwd`
    mkdir -p "$icons_dir"
    cd "$icons_dir"
    #for i in `cat /var/www/browser/links.html | sed 's/ /\n/g' | grep "\.png" | sed -e 's/src=//g' -e 's/"//g'`
    #do
    #	wget -q -c "$i"
    #done
    wget -q -c -U "$useragent" "$ilink" -O /tmp/icons.zip
    md5s="`md5sum /tmp/icons.zip`"
    if [ "${md5s:0:32}" -ne "$imd5" ]
    then
	rm /tmp/icons.zip
	exit 1
    else
	unzip /tmp/icons.zip
	rm /tmp/icons.zip
    fi
    
    cat /var/www/browser/links.html | sed 's/\(src="\)http.*\/\([a-z_A-Z0-9]*.png\)/\1Images\/tmp\/\2/g' > $icons_dir/links.html
fi

mount --bind $icons_dir/links.html /var/www/browser/links.html

cd $cur_dir

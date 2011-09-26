#!/bin/sh
# links_images_preload.sh script by xeros
# Source code released under GPL License

#icons_dir="/tmp/links_icons"
icons_dir="/home/netcast_icons/www"

if [ ! -f "$icons_dir/links.html" ]
then
    while [ -z "`ping -4 -c 1 www.ottomano.it 2>/dev/null | grep '64 bytes from'`" ]
    do
	sleep 10
    done

    cur_dir=`pwd`
    mkdir -p "$icons_dir"
    cd "$icons_dir"
    for i in `cat /var/www/browser/links.html | sed 's/ /\n/g' | grep "\.png" | sed -e 's/src=//g' -e 's/"//g'`
    do
	wget -q -c "$i"
    done
    cat /var/www/browser/links.html | sed 's/\(src="\)http.*\/\([a-z_A-Z0-9]*.png\)/\1Images\/tmp\/\2/g' > $icons_dir/links.html
fi

mount --bind $icons_dir/links.html /var/www/browser/links.html

cd $cur_dir

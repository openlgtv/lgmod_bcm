#!/bin/sh
# links_images_preload.sh script by xeros
# Source code released under GPL License

cur_dir=`pwd`
mkdir -p /tmp/links_icons
cd /tmp/links_icons
for i in `cat /var/www/browser/links.html | sed 's/ /\n/g' | grep "\.png" | sed -e 's/src=//g' -e 's/"//g'`
do
    wget -q -c $i
done
cat /var/www/browser/links.html | sed 's/\(src="\)http.*\/\([a-z_A-Z0-9]*.png\)/\1Images\/tmp\/\2/g' > /tmp/links_icons/links.html
mount --bind /tmp/links_icons/links.html /var/www/browser/links.html
cd $cur_dir

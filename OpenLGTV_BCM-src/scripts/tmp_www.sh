#!/bin/sh
# tmp_www.sh script by xeros
# Source code released under GPL License

echo "OpenLGTV_BCM-INFO: tmp_www.sh: script runing"
echo "OpenLGTV_BCM-INFO: tmp_www.sh: making copy of /var/www to /tmp/www"
cp -r /var/www /tmp
echo "OpenLGTV_BCM-INFO: tmp_www.sh: mount-binding /tmp/www to /var/www"
mount --bind /tmp/www /var/www
echo "OpenLGTV_BCM-INFO: calling rc.httpd to restart httpd services"
/etc/rc.d/rc.httpd restart
echo "OpenLGTV_BCM-INFO: tmp_www.sh: script end"

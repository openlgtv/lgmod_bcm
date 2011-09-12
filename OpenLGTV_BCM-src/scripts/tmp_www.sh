#!/bin/sh
# tmp_www.sh script by xeros
# Source code released under GPL License

echo "OpenLGTV_BCM-INFO: tmp_www.sh: script runing"
echo "OpenLGTV_BCM-INFO: tmp_www.sh: making copy of /var/www to /tmp/www"
cp -r /var/www /tmp
echo "OpenLGTV_BCM-INFO: tmp_www.sh: stopping current httpd processes"
killall httpd
echo "OpenLGTV_BCM-INFO: tmp_www.sh: mount-binding /tmp/www to /var/www"
mount --bind /tmp/www /var/www
echo "OpenLGTV_BCM-INFO: starting local httpd on 127.0.0.1:88"
#httpd -h /var/www
httpd -c /etc/httpd.conf -p 127.0.0.1:88 -h /var/www
if [ -f "/mnt/user/etc/httpd.conf" ]
then
    echo "OpenLGTV_BCM-INFO: starting external httpd on 0.0.0.0:80 - connections need authentication"
    httpd -c /mnt/user/etc/httpd.conf -p 0.0.0.0:80 -h /var/www -r "OpenLGTV BCM WebUI"
else
    echo "OpenLGTV_BCM-WARN: external httpd config in /mnt/user/etc/httpd.conf not found - you wont be able to connect to WebUI from PC"
fi
echo "OpenLGTV_BCM-INFO: tmp_www.sh: script end"

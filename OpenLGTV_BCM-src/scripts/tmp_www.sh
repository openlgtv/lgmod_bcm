#!/bin/sh
# tmp_www.sh script by xeros
# Source code released under GPL License
echo "OpenLGTV_BCM-INFO: tmp_www.sh: script runing"                       | tee -a /var/log/OpenLGTV_BCM.log
echo "OpenLGTV_BCM-INFO: tmp_www.sh: making copy of /var/www to /tmp/www" | tee -a /var/log/OpenLGTV_BCM.log
cp -r /var/www /tmp                                                  2>&1 | tee -a /var/log/OpenLGTV_BCM.log
echo "OpenLGTV_BCM-INFO: tmp_www.sh: stopping current httpd processes"    | tee -a /var/log/OpenLGTV_BCM.log
killall httpd                                                        2>&1 | tee -a /var/log/OpenLGTV_BCM.log
echo "OpenLGTV_BCM-INFO: tmp_www.sh: mount-binding /tmp/www to /var/www"  | tee -a /var/log/OpenLGTV_BCM.log
mount --bind /tmp/www /var/www                                       2>&1 | tee -a /var/log/OpenLGTV_BCM.log
echo "OpenLGTV_BCM-INFO: starting local httpd on 127.0.0.1:88"            | tee -a /var/log/OpenLGTV_BCM.log
#httpd -h /var/www | tee -a /var/log/OpenLGTV_BCM.log
httpd -c /etc/httpd.conf -p 127.0.0.1:88 -h /var/www                 2>&1 | tee -a /var/log/OpenLGTV_BCM.log
if [ -f "/mnt/user/etc/httpd.conf" ]
then
    echo "OpenLGTV_BCM-INFO: starting external httpd on 0.0.0.0:80 - connections need authentication" | tee -a /var/log/OpenLGTV_BCM.log
    httpd -c /mnt/user/etc/httpd.conf -p 0.0.0.0:80 -h /var/www -r "OpenLGTV BCM WebUI"          2>&1 | tee -a /var/log/OpenLGTV_BCM.log
else
    echo "OpenLGTV_BCM-WARN: external httpd config in /mnt/user/etc/httpd.conf not found - you wont be able to connect to WebUI from PC" | tee -a /var/log/OpenLGTV_BCM.log
fi
echo "OpenLGTV_BCM-INFO: tmp_www.sh: script end"                          | tee -a /var/log/OpenLGTV_BCM.log

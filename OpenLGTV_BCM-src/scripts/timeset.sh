#!/bin/sh
# OpenLGTV BCM time setting script by xeros
# Source code released under GPL License

# TODO: make more testing how reliable is ntpclient alone - maybe it could be used without script like this

[ -z "$ntpsrvr"  ] && ntpserver="pool.ntp.org"
[ -z "$ntpdelay" ] && ntpdelay=16
timeset=""

while [ -z "$timeset" ]
do
    ntpclient -c 1 -i 1 -h "$ntpsrv" -s > /dev/null 2>&1 && timeset=1 || sleep "$ntpdelay"
done

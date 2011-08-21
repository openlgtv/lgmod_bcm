#!/bin/ash
# OpenLGTV BCM script proxy-start.sh by xeros
# Proxy script for JavaScript code injection starting
# Source code released under GPL License

# proxy_log_debug values:
# 0 - no logging at all
# 1 - logging only processes
# 2 - logging whole request on stderr
# 3 - logging request and answer to file

[ -z "$proxy_connect_port" ]      && proxy_connect_port=80
[ -z "$proxy_listen_port" ]       && proxy_listen_port=8888
[ -z "$proxy_listen_port_hex" ]   && proxy_listen_port_hex=22B8
[ -z "$proxy_usleep_time" ]       && proxy_usleep_time=80
#[ -z "$proxy_wait_time" ]        && proxy_wait_time=4
[ -z "$proxy_wait_time" ]         && proxy_wait_time=8
[ -z "$proxy_respawn_run_check" ] && proxy_respawn_run_check=0
#[ -z "$proxy_log_debug" ]        && proxy_log_debug=3
[ -z "$proxy_log_debug" ]         && proxy_log_debug=0
[ -z "$proxy_log_file" ]          && proxy_log_file=/var/log/proxy.log
[ -z "$proxy_sh" ]                && proxy_sh=/scripts/proxy.sh
[ -z "$proxy_respawner" ]         && proxy_respawner=/scripts/proxy-respawner.sh
[ -z "$proxy_localhost_only" ]    && proxy_localhost_only=1

# for proxy testing on PC
#[ -z "$awk" ]                    && awk="busybox awk"
[ -z "$awk" ]                     && awk=awk
[ -z "$sed" ]                     && sed=sed
[ -z "$nc" ]                      && nc=nc
[ -z "$tcpsvd" ]                  && tcpsvd=tcpsvd

export proxy_listen_port proxy_usleep_time proxy_log_debug proxy_log_file proxy_wait_time proxy_connect_port proxy_log_file proxy_respawn_run_check

export id=1
#echo IDX $id SPAWN >&2

if [ "$proxy_localhost_only" ]
then
    proxy_listen_ip="127.0.0.1"
    proxy_listen_ip_hex="0100007F"
else
    proxy_listen_ip="0"
    proxy_listen_ip_hex="00000000"
fi

if [ -n "`grep $proxy_listen_ip_hex:$proxy_listen_port_hex /proc/net/tcp`" ]
then
    echo "Proxy is running!"
    exit 1
fi

#depreciated - could handle properly only 1 connection at once# $nc -l -p $proxy_listen_port -e $proxy_sh
if [ "$proxy_log_debug" -ge "1" ]
then
    $tcpsvd -v $proxy_listen_ip $proxy_listen_port $proxy_sh
else
    $tcpsvd $proxy_listen_ip $proxy_listen_port $proxy_sh
fi

#echo "respawner"

#not needed with tcpsvd# $proxy_respawner

exit 0

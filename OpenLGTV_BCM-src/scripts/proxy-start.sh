#!/bin/ash
# OpenLGTV BCM script proxy-start.sh by xeros
# Proxy script for JavaScript code injection starting
# Source code released under GPL License

# this script is not finished, currently it's better to use proxy-respawner.sh instead

# proxy_log_debug values:
# 0 - no logging at all
# 1 - logging only processes
# 2 - logging whole request on stderr
# 3 - logging request and answer to file

[ -z "$proxy_connect_port" ]      && proxy_connect_port=80
[ -z "$proxy_listen_port" ]       && proxy_listen_port=8888
[ -z "$proxy_listen_port_hex" ]   && proxy_listen_port_hex=22B8
[ -z "$proxy_usleep_time" ]       && proxy_usleep_time=80
[ -z "$proxy_wait_time" ]         && proxy_wait_time=4
[ -z "$proxy_respawn_run_check" ] && proxy_respawn_run_check=0
#[ -z "$proxy_log_debug" ]        && proxy_log_debug=3
[ -z "$proxy_log_debug" ]         && proxy_log_debug=0
[ -z "$proxy_log_file" ]          && proxy_log_file=/var/log/proxy.log
[ -z "$proxy_lock_file" ]         && proxy_lock_file=/var/run/proxy.lock
[ -z "$proxy_sh" ]                && proxy_sh=/scripts/proxy.sh
[ -z "$proxy_respawner" ]         && proxy_respawner=/scripts/proxy-respawner.sh

export proxy_listen_port proxy_usleep_time proxy_log_debug proxy_log_file proxy_wait_time proxy_connect_port proxy_log_file proxy_lock_file proxy_respawn_run_check

export id=1
#echo IDX $id SPAWN >&2

if [ -n "`grep 00000000:$proxy_listen_port_hex /proc/net/tcp`" -o -f "$proxy_lock_file" ]
then
    echo "Proxy is running!"
    exit 1
fi

touch $proxy_lock_file

busybox nc -l -p $proxy_listen_port -e $proxy_sh

#echo "respawner"

$proxy_respawner

rm $proxy_lock_file

exit 0

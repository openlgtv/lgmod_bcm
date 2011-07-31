#!/bin/ash
# OpenLGTV BCM script proxy-respawner.sh by xeros
# Proxy script for JavaScript code injection respawner
# Source code released under GPL License

# proxy_log_debug values:
# 0 - no logging at all
# 1 - logging only processes
# 2 - logging whole request on stderr
# 3 - logging request and answer to file

[ -z "$proxy_listen_port" ]      && proxy_listen_port=8888
[ -z "$proxy_listen_port_hex" ]  && proxy_listen_port_hex=22B8
[ -z "$proxy_usleep_time" ]      && proxy_usleep_time=30
#[ -z "$proxy_log_debug" ]       && proxy_log_debug=3
[ -z "$proxy_log_debug" ]        && proxy_log_debug=0
[ -z "$proxy_log_file" ]         && proxy_log_file=/var/log/proxy.log
#[ -z "$proxy_log_file" ]        && proxy_log_file=log.log
[ -z "$proxy_wait_time" ]        && proxy_wait_time=4
[ -z "$proxy_connect_port" ]     && proxy_connect_port=80
#[ -z "$proxy_sh" ]              && proxy_sh=./proxy.sh
[ -z "$proxy_sh" ]               && proxy_sh=/scripts/proxy.sh
[ -z "$proxy_lock_file" ]        && proxy_lock_file=/var/run/proxy.lock

export proxy_listen_port proxy_usleep_time proxy_log_debug proxy_log_file proxy_wait_time proxy_connect_port proxy_log_file proxy_lock_file

#if [ -n "`grep 00000000:$proxy_listen_port_hex /proc/net/tcp`" -o -f "$proxy_lock_file" ]
#then
#    echo "Proxy is running!"
#    exit 1
#fi

touch $proxy_lock_file

export id=1
#busybox nc -l -p $proxy_listen_port -e $proxy_sh
#if [ "$proxy_log_debug" -ge "1" ]; then echo ID $id EXIT; fi

#echo Running loop >&2
while true
do
	#if [ -z "`busybox netstat -t -l -n | grep :$proxy_listen_port`" ]
	if [ -z "`grep 00000000:$proxy_listen_port_hex /proc/net/tcp`" ]
	then
		if [ "$proxy_log_debug" -ge "1" ]
		then
		    echo ID $id SPAWN
		fi
		#$(busybox nc -l -l -p $proxy_listen_port -e $proxy_sh; if [ "$proxy_log_debug" -ge "1" ]; then echo echo ID $id EXIT; fi) &
		nc -l -l -p $proxy_listen_port -e $proxy_sh &
		export id=$(($id+1))
		# TODO: better check and quicker start of new connection listeners without more resources usage
		#usleep $proxy_usleep_time
	fi
	if [ ! -f "$proxy_lock_file" ]
	then
	    echo "`basename $0`: Proxy lock file ($proxy_lock_file) removed - exiting!"
	    killall nc
	    exit 1
	fi
	#usleep $proxy_usleep_time
done
# &
#echo After loop >&2

#echo ID $id SPAWN >&2
##$proxy_sh; if [ "$proxy_log_debug" -ge "1" ]; then echo echo ID $id EXIT >&2; fi
##export id=$(($id+1))


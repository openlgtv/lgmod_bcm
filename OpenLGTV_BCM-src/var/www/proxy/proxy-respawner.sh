#!/bin/ash
# OpenLGTV BCM script proxy-respawner.sh by xeros
# Proxy script for JavaScript code injection respawner
# Source code released under GPL License

export listen_port=8888
export usleep_time=100

export id=1
while true
do
	if [ -z "`busybox netstat -t -l -n | grep :$listen_port`" ]
	then
		echo ID $id SPAWN
		$(busybox nc -l -l -p $listen_port -e ./proxy.sh; echo echo ID $id EXIT; ) &
		export id=$(($id+1))
		# TODO: better check and quicker start of new connection listeners
		busybox usleep $usleep_time
	fi
done

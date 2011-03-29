#!/bin/sh

echo "Mounting /share/global_platform/bcm3549 as home"
SERVER_IP=$(cat /proc/cmdline | awk -v RS='[ :\:]' -F= '/nfsroot/{print $2}')
mount -t nfs -o rsize=4096,wsize=4096,tcp $SERVER_IP:/share/global_platform/bcm3549 /home
mount -t tmpfs none /usr/etc -o size=4k

echo "Registering users into user list"
USER_LIST=$(ls /home)
cp /etc/passwd.org /usr/etc/passwd
for SERVER_USER in $USER_LIST
do
	if [ -d /home/$SERVER_USER ] && [ $SERVER_USER != root ];then
		echo "$SERVER_USER::0:0:$SERVER_USER:/home/$SERVER_USER:/bin/sh" >> /usr/etc/passwd
	fi
done

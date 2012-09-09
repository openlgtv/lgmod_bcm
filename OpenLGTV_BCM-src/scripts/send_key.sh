#!/bin/sh
# send_key.sh xeros
# Source code released under GPL License

# Supported input arguments 
# - <KEY_CODE> - two digit hexadecimal keycode (key code is passed to RELEASE without parsing)
# - K_<KEY> - <KEY> as key name from openrelease_keymap.cfg (key name is translated to key code and sent to RELEASE only when OPENRELEASE was not enabled or there's no other assigned action, otherwise OPENRELEASE action is being parsed and executed)

# You can put more key codes or key names as additional args (key codes and key names can be mixed also)

# So far only these actions are supported via OPENRELEASE settings (when used K_<KEY> arguments):
# - default - default action
# - K_<KEY> - defautl action for other key <KEY>
# - K_X<KEY_CODE> - key with keycode (<KEYCODE> in hex: for example AA)
# - SYSTEM: <COMMAND> - execute <COMMAND>

# TODO: support for key modes switching and more actions

openrelease_cfg=/etc/openrelease/openrelease.cfg
openrelease_keymap=/etc/openrelease/openrelease_keymap.cfg
irkeymap=/etc/irkeymap.cfg
id=01
scriptname=`basename $0`

[ -z "$1" ] && echo "You have to provide at least one 2-digit hex keycode or key name as argument, for example: $0 K_NETCAST" && exit 1

for argv in "$@"
do
    IRcode=""
    IRkey=""
    [ "${#argv}" -le "2" ] && IRcode="$argv" || IRkey="$argv"
    if [ -n "$IRcode" -o -n "$IRkey" ]
    then
	[ "$IRcode" = "" ] && IRcode=`grep -m1 "^${IRkey}=" "$irkeymap" | cut -d= -f2`
	rel_stdin="`grep -m1 ^input ${openrelease_cfg} | cut -d= -f2 | sed 's/ *//g'`"
	if [ -z "`grep "OPENRELEASE=1" /mnt/user/cfg/settings`" -o "$rel_stdin" = "NULL" ]
	then
	    tmux send-keys -t "RELEASE" "mc $id $IRcode" C-m
	else
	    if [ -z "$rel_stdin" ]
	    then
		rel_stdin="/tmp/openrelease.in"
	    fi
	    [ "$IRkey" != "" ] && openrel_action=`grep -m1 "^${IRkey} *=" "$openrelease_keymap" | sed -e "s/^$IRkey *= *//g" -e 's/"//g'`
	    if [ "${openrel_action:0:2}" = "K_" ]
	    then
		if [ "${openrel_action:0:3}" = "K_X" ]
		then
		    IRcode="${openrel_action:3:2}"
		else
		    IRcode=`grep -m1 "^${openrel_action}=" "$irkeymap" | cut -d= -f2`
		fi
		openrel_action=default
	    fi
	    #if [ -z "$openrel_action" -o "$openrel_action" = "default" ]
	    # prevent actions key loop? any better idea for logic here?
	    if [ -z "$openrel_action" -o "$openrel_action" = "default" -o "${openrel_action:0:28}" = "SYSTEM: /scripts/send_key.sh" -o "${openrel_action:0:27}" = "SYSTEM:/scripts/send_key.sh" ]
	    then
		[ -n "$IRcode" ] && echo "mc $id $IRcode" >> "$rel_stdin"
	    else
		if [ "${openrel_action:0:7}" = "SYSTEM:" ]
		then
		    command="${openrel_action#SYSTEM:}"
		    command="${command# }"
		    command="${command% &}"
		    [ -n "$command" ] && $command &
		fi
	    fi
	fi
    fi
done

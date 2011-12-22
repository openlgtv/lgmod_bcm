#!/bin/haserl
# remote.cgi by mihaifireball & xeros
# Source code released under GPL License
content-type: text/html

<html>

<?  
    # So far only these actions are supported via OPENRELEASE settings:
    # - default - default action
    # - K_<KEY> - defautl action for other key <KEY>
    # - K_X<KEY_CODE> - key with keycode (<KEYCODE> in hex: for example AA)
    # - SYSTEM: <COMMAND> - execute <COMMAND>

    openrelease_cfg=/etc/openrelease/openrelease.cfg
    openrelease_keymap=/etc/openrelease/openrelease_keymap.cfg
    irkeymap=/var/www/remote/irkeymap.cfg

    if [ "$FORM_IRcode" != "" -o "$FORM_IRkey" != "" ]
    then
	[ "$FORM_IRcode" = "" ] && FORM_IRcode=`grep -m1 "^${FORM_IRkey}=" "$irkeymap" | cut -d= -f2`
	rel_stdin="`grep -m1 ^input ${openrelease_cfg} | cut -d= -f2 | sed 's/ *//g'`"
	if [ -z "`grep "OPENRELEASE=1" /mnt/user/cfg/settings`" -o "$rel_stdin" = "NULL" ]
	then
	    tmux send-keys -t "RELEASE" "mc 01 $FORM_IRcode" C-m
	else
	    if [ -z "$rel_stdin" ]
	    then
		rel_stdin="/tmp/openrelease.in"
	    fi
	    [ "$FORM_IRkey" != "" ] && openrel_action=`grep -m1 "^${FORM_IRkey}" "$openrelease_keymap" | sed -e "s/^$FORM_IRkey *= *//g" -e 's/"//g'`
	    if [ "${openrel_action:0:2}" = "K_" ]
	    then
		if [ "${openrel_action:0:3}" = "K_X" ]
		then
		    FORM_IRcode="${openrel_action:3:2}"
		else
		    FORM_IRcode=`grep -m1 "^${openrel_action}=" "$irkeymap" | cut -d= -f2`
		fi
		openrel_action=default
	    fi
	    if [ -z "$openrel_action" -o "$openrel_action" = "default" ]
	    then
		[ -n "$FORM_IRcode" ] && echo "mc 01 $FORM_IRcode" >> "$rel_stdin"
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
?>

<script language="javascript" type="text/javascript">history.back();</script>

</body>
</html>

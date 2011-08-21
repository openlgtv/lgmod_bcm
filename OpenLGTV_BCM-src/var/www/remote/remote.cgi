#!/bin/haserl
# remote.cgi by mihaifireball
# adapted to work with OPENRELEASE redirections by xeros
# Source code released under GPL License
content-type: text/html

<html>

<?  if [ "$FORM_IRcode" != "" ]
    then
	rel_stdin="`grep ^input /mnt/user/etc/openrelease/openrelease.cfg | awk -F= '{print $2}' | sed 's/ *//g'`"
	if [ -z "`grep "OPENRELEASE=1" /mnt/user/cfg/settings`" -o "$rel_stdin" = "NULL" ]
	then
	    tmux send-keys -t "RELEASE" "mc 01 $FORM_IRcode" C-m
	else
	    if [ -z "$rel_stdin" ]
	    then
		rel_stdin="/tmp/openrelease.in"
	    fi
	    echo "mc 01 $FORM_IRcode" >> "$rel_stdin"
	fi
    fi
?>

<script language="javascript" type="text/javascript">history.back();</script>

</body>
</html>

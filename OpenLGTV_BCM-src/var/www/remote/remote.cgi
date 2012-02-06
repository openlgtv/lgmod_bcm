#!/usr/bin/haserl
# remote.cgi by mihaifireball & xeros
# Source code released under GPL License
content-type: text/html

<html>
<body>

<?  
    if [ -n "$FORM_IRcode" -o -n "$FORM_IRkey" ]
    then
	[ -n "$FORM_IRcode" ] && action="$FORM_IRcode" || action="$FORM_IRkey"
	/scripts/send_key.sh "$action" &
    fi
?>

<script language="javascript" type="text/javascript">history.back();</script>

</body>
</html>

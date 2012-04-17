#!/usr/bin/haserl
# remote.cgi by mihaifireball & xeros
# Source code released under GPL License
content-type: text/html

<html>
<head>
<meta http-equiv="Content-Script-Type" content="text/javascript">
<!-- META http-equiv="refresh" content="0;url=index.html" -->
<script language="javascript" type="text/javascript">
function goBack()
{
    //if (!history.back()) { window.location.replace('index.html'); }
    history.go(-1);
}
window.onload=goBack();
</script>
</head>
<body>

<?  
    if [ -n "$FORM_IRcode" -o -n "$FORM_IRkey" ]
    then
	[ -n "$FORM_IRcode" ] && action="$FORM_IRcode" || action="$FORM_IRkey"
	/scripts/send_key.sh "$action" &
    fi
?>

<!-- script language="javascript" type="text/javascript">history.back();</script -->

</body>
</html>

#!/bin/haserl
content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<!-- index.cgi for OpenLGTV BCM WebUI by xeros -->
<!-- Source code released under GPL License -->
<HEAD>
<? 
if [ -z "`cat /mnt/user/cfg/pin`" ]
then
    if [ -z "${QUERY_STRING}" ]
    then
	echo '<META http-equiv="refresh" content="0;url=home.cgi">' 
    else
	echo "<META http-equiv='refresh' content='0;url=${FORM_auth}?${QUERY_STRING}'>" 
    fi
fi
?>
</HEAD>
<BODY>
<FONT SIZE="+0">
<CENTER>
<BR/><BR/>
<IMG SRC="Images/openlgtvbcm_logo.png" ALT="OpenLGTV BCM"/>
<BR/>OpenLGTV BCM Web UI<BR/><BR/>
[Work in Progress]<BR/>
<? env ?>
</CENTER>
</FONT>
</BODY>
</HTML>

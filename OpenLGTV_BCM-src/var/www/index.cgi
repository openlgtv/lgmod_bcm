#!/bin/haserl
content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<!-- index.cgi for OpenLGTV BCM WebUI by xeros -->
<!-- Source code released under GPL License -->
<HEAD>
<? 
pin="`cat /mnt/user/cfg/pin 2>/dev/null`"
if [ -z "${pin}" ]
then
    if [ -z "${QUERY_STRING}" ]
    then
	echo '<META http-equiv="refresh" content="0;url=home.cgi">' 
    else
	echo "<META http-equiv='refresh' content='0;url=${FORM_auth}?${QUERY_STRING}'>" 
    fi
else
    #TODO: write pin authorization in JavaScript so /auth.cgi?auth=... could be used to authorize by pin to any local or remote sites (useful for OPENRELEASE button assignments to WebUI/FileManager/etc... (parental lock))
    echo "<div style='position: absolute; left: 300px; top: 350px; width:600px; background-color:red;height:70px; font-size:50px; padding: 50px; border: 1px solid #D3D3D3;'>Enter PIN:</div>"
fi
?>
</HEAD>
<BODY bgcolor="black">
<? tail -n 11 /var/www/index.html ?>

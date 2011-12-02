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
    echo "<div style='position: absolute; left: 300px; top: 350px; width:600px; background-color:red;height:70px; font-size:50px; padding: 50px; border: 1px solid #D3D3D3;'><b>Enter PIN: &nbsp; <span id='pin'></span></b></div>"
    echo -e "	<script type='text/javascript'> \n\
	var pin='${pin}'; \n\
	var pin2=''; \n\
	var eventHandler = detectEvent; \n\
	document['onkeydown'] = eventHandler; \n\
	function detectEvent(e) { \n\
	    var evt = e || window.event; \n\
	    var key=evt.keyCode; \n\
	    if ( key >= 48 & key <= 57 ) \n\
	    { \n\
		document.getElementById('pin').innerHTML += '*'; \n\
		pin2 += String.fromCharCode(evt.keyCode); \n\
	    } else if ( key == 13 ) \n\
	    { \n\
		if ( pin2 == pin ) \n\
		{ "
		    if [ -z "${QUERY_STRING}" ]
		    then
			echo "window.location.replace('home.cgi');"
		    else
			echo "window.location.replace('${FORM_auth}?${QUERY_STRING}');"
		    fi
		echo -e " \n\
		} else {\n\
		    document.getElementById('pin').innerHTML = ''; \n\
		    pin2=''; \n\
		} \n\
	    } else if ( key == 461 ) \n\
	    { \n
		window.NetCastBack(); \n\
	    } else if ( key == 1001 ) \n\
	    { \n\
		window.NetCastExit(); \n\
	    } \n\
	    return false; \n\
	} \n\
    </script>"
fi
?>
</HEAD>
<? tail -n 11 /var/www/index.html ?>

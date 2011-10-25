#!/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- OpenLGTV BCM FileManager by xeros -->
<!-- Source code released under GPL License -->

<style type="text/css">
    //#fullheight{height:500px}
    body {
	font-family:monospace;
	height: 720px;
	//font-family:"TiresiasScreenfont";
    }
    a:link {
	color:black;
	text-decoration:bold;
    }
    tbody.main {
	width: 95%;
	height: 95%;
	//overflow:scroll;
	//height:10em;
	//display:inline-block;
	overflow-y:auto;
	overflow-x: hidden;
	max-height:700px;
    }
    tbody.scrollable {
	display: block;
	height: 100%;
	overflow-y: auto;
	overflow-x: hidden;
	max-height:700px;
    }
    td.panel {
	min-width: 410px;
    }
</style>
<title>CGI FileManager by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

<?

#useragent="Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"
#useragent="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"

log_file=/tmp/log/fm.log

if [ "$FORM_side" != "" ]
then
    export side="$FORM_side"
else
    export side="l"
fi

if [ "$FORM_lpth" != "" ]
then
    export lpth="$FORM_lpth"
fi

if [ "$FORM_rpth" != "" ]
then
    export rpth="$FORM_rpth"
fi

if [ "$FORM_action" != "" ]
then
    export action="$FORM_action"
fi

if [ "$FORM_link" != "" ]
then
    export link="$FORM_link"
fi

echo "var side = '$side';"
echo "var lpth = '$lpth';"
echo "var rpth = '$rpth';"

?>

var col = 1; //number of 'cells' in a row
var current = 1;
var next = current;
//var side = 'l';
var side = 'r';
var nside = side;

document.onkeydown = check;
window.onload = OnLoadSetCurrent;
     
function check(e)
	{
	if (!e) var e = window.event;
	(e.keyCode) ? key = e.keyCode : key = e.which;
	try
		{
		switch(key)
			{
			//case 33: next = (1*current) - 30; break; //ch up
			//case 34: next = (1*current) + 30; break; //ch down
			case 37: next = current; nside = 'l'; break; //left
			//case 38: next = current - col; break; //up
			case 39: next = current; nside = 'r'; break; //right
			//case 40: next = (1*current) + col; break; //down
			}
		if (key==33|key==34|key==37|key==38|key==39|key==40)
			{
			if (next==0)
			    {
				next = 1;
			    }
			//Check if new link exists, if not then go to previous one until finds the one that exists
			if (!document.links['link_' + nside + next])
			{
			    do {
				next = next - 1;
			    } while ((!document.links['link_' + nside + next])&&(next >= 1));
			}
			ChangeBgColor();
			//Move to the next bookmark
			var code=document.links['link_' + nside + next].name;
			document.links['link_' + nside + next].focus();
			current = next;
			side = nside;
			//Prevent scrolling
			return false;
			}
		else if (key==32) 
			{
			    document.getElementById('link_' + side + current).click();
		//	    //alert(document.getElementById('link_' + side + current).href); // link destination
		//	    //alert(document.getElementById('link_' + side + current).text); // link name
		//	    var dest='fm-action.cgi?action=copy' + '&side=' + side + '&lpath=' + lpth + '&rpath=' + rpth + '&link=' + document.getElementById('link_' + side + current).href;
		//	    alert(dest);
		//	    window.location=dest;
			    return false;
			}
		//else if (key==404) 
		//	{
		//	//the green button on the remote control have been pressed
		//	//Switch to the Keyboard
		//	top.frames["Keyboard"].focus();
		//	}
		else if (key==461) 
			{
			//the back button on the remote control have been pressed
			//NetCastBack API
			//window.NetCastBack();
			//lets get back to WebUI instead of closing NetCast service
			history.go(-1);
			}
		else if (key==1001) 
			{
			//the exit button on the remote control have been pressed
			//NetCastExit API
			window.NetCastExit();
			}
		}catch(Exception){}
	}

function ChangeBgColor()
	{
	//Change the TD element BgColor.
	//document.bgColor = '#D3D3D3';
	document.getElementById('tr_' + side + current).bgColor = '#FFFFFF';
	document.getElementById('tr_' + nside + next).bgColor = '#D3D3D3';
	}
	

function setCurrent(element)
	{
	var string = element.id;
	//cut number after 'link' name
	current = string.slice(4,string.length);
	}
	

	function OnLoadSetCurrent(element)
	{
	current=1;
	//top.frames["Keyboard"].focus();
	document.links['link_' + side + current].focus();
	ChangeBgColor();
	}
	
document.defaultAction = true;


// -->
</script>


</HEAD>
<BODY bgcolor="black">

<?

if [ "$side" = "l" ]
then
    export spth="$lpth"
    export dpth="$rpth"
else
    export spth="$rpth"
    export dpth="$lpth"
fi

#echo "spth: $spth dpth: $dpth lpth: $lpth rpth: $rpth"

echo '<center><font size="+3" color="yellow"><br/><br/><b>OpenLGTV BCM FileManager</b> by xeros<br/><br/><br/></font>'

#echo '<div style="position: absolute; left: 10px; top: 10px; width:860px; font-size:16px; background-color:white;">'
echo '<div style="width:80%; margin:auto; font-size:16px; background-color:white;">'

if [ "$action" = "play" ]
then
    #echo '<script type="text/javascript" src="player/base64.js"></script>'
    echo "Starting playback of $spth ...<br/>"
    sleep 1
    echo "<script type='text/javascript'>"
    #echo "window.location='file:///mnt/browser/pages/player/index.html?lg_media_url=base64(http://127.0.0.1:88/root$spth)';"
    echo "window.location=\"root$spth\";"
    echo "</script>"
    echo "<br/>Done"
fi

if [ "$FORM_confirm" != "yes" ]
then
    echo "<center><font size='+4' color='brown'><br/><b>"
    if [ "$action" = "copy" -o "$action" = "move" ]
    then
	echo "Are you sure you want to ${action}?<br/><font size='+1' color='black'><br/>$spth to $dpth/</font>"
    else
	if [ "$action" = "delete" ]
	then
	    echo "Are you sure you want to ${action}?<br/><font size='+2' color='black'><br/>$spth</font>"
	else
	    echo "UNRECOGNISED ACTION!"
	    sleep 1
	    echo '<script type="text/javascript">history.go(-1);</script>"'
	fi
    fi
    echo "</b><br/><br/></font>"
    echo "<table><tr><td id='tr_l1' width='200px' align='center'><b><a id='link_l1' href='${REQUEST_URI}&confirm=yes'><font size='+4'>Yes</font></a></b></td><td id='tr_r1' width='200px' align='center'><b><a id='link_r1' href='javascript:history.go(-1);'><font size='+4'>No</font></a></b></td></tr></table></center><br/><br/>"
else
    if [ "$action" = "copy" ]
    then
	echo "Copying $spth to $dpth/ ...<br/>"
	cp -r "$spth" "$dpth/" 2>&1
	echo "<br/>Done"
    fi
    if [ "$action" = "move" ]
    then
	echo "Moving $spth to $dpth/ ...<br/>"
	mv "$spth" "$dpth/" 2>&1
	echo "<br/>Done"
    fi
    if [ "$action" = "delete" ]
    then
	if [ "$spth" != "" -a "$spth" != "/" ]
	then
	    echo "Removing $spth ...<br/>"
	    rm -r "$spth" 2>&1
	    echo "<br/>Done"
	fi
    fi
    sleep 1
    echo '<script type="text/javascript">history.go(-2);</script>"'
fi
echo '</div>'

?>
</BODY></HTML>

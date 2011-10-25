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
	max-height:650px;
    }
    td.panel {
	min-width: 415px;
    }
    td.filename {
	min-width: 400px;
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

echo "var side = '$side';"
echo "var lpth = '$lpth';"
echo "var rpth = '$rpth';"

#echo "<script type='text/javascript'>"
if [ "$side" = "l" -a "$lpth" != "" ]
then
    cpth="$lpth"
else
    if [ "$side" = "r" -a "$rpth" != "" ]
    then
	cpth="$rpth"
    fi
fi

if [ -f "$cpth" ]
then
    echo "var cpth = '$cpth';"
    #echo "var dest='fm-action.cgi?action=play' + '&side=' + side + '&lpth=' + lpth + '&rpth=' + rpth + '&link=' + document.getElementById('link_' + side + current).href;"
    echo "var dest='fm-action.cgi?action=play&side=$side&lpth=$cpth&rpth=$cpth';"
    sleep 1
    echo "window.location=dest;"
fi
#echo "</script>"


?>

var col = 1; //number of 'cells' in a row
var current = 1;
var next = current;
//var side = 'l';
var nside = side;

//Attach the function with the event
if(document.addEventListener) document.addEventListener('keydown', check, false);
else if(document.attachEvent) document.attachEvent('onkeydown', func);
else document.onkeydown = check;

window.onload = OnLoadSetCurrent;
     
function check(e)
	{
	if (!e) var e = window.event;
	(e.keyCode) ? key = e.keyCode : key = e.which;
	//workaround to check for 'enter' on WebKit which doesnt want to work in 'try' block
	if (key==10|key==13) 
		{   //enter
		    //alert(document.getElementById('link_' + side + current).href); // link destination
		    //alert(document.getElementById('link_' + side + current).text); // link name
		    document.getElementById('link_' + side + current).click();
		    return false;
		}
	try
		{
		switch(key)
			{
			case 33: next = (1*current) - 10; break; //ch up
			case 34: next = (1*current) + 10; break; //ch down
			case 37: next = current; nside = 'l'; break; //left
			case 38: next = current - col; break; //up
			case 39: next = current; nside = 'r'; break; //right
			case 40: next = (1*current) + col; break; //down
			}
		if (key==33|key==34|key==37|key==38|key==39|key==40)
			{
			if (next<=0)
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
			e.preventDefault();
			return false;
			}
		else if (key==403|key==119) 
			{
			//the red button on the remote control or F8 have been pressed
			//Delete file or directory
			// lpath and rpath variables are wrong - but the right ones lpth and rpth are gathered from link
			var dest='fm-action.cgi?action=delete' + '&side=' + side + '&lpath=' + lpth + '&rpath=' + rpth + '&link=' + document.getElementById('link_' + side + current).href;
			window.location=dest;
			//Prevent default action
			return false;
			}
		else if (key==404|key==116) 
			{
			//the green button on the remote control or F5 have been pressed
			//Copy file or directory
			var dest='fm-action.cgi?action=copy' + '&side=' + side + '&lpath=' + lpth + '&rpath=' + rpth + '&link=' + document.getElementById('link_' + side + current).href;
			window.location=dest;
			//Prevent default action
			return false;
			}
		else if (key==405|key==117) 
			{
			//the yellow button on the remote control or F6 have been pressed
			//Move file or directory
			var dest='fm-action.cgi?action=move' + '&side=' + side + '&lpath=' + lpth + '&rpath=' + rpth + '&link=' + document.getElementById('link_' + side + current).href;
			window.location=dest;
			//Prevent default action
			return false;
			}
		else if (key==406) 
			{
			//the blue button on the remote control have been pressed
			//Play the media file
			var dest='fm-action.cgi?action=play' + '&side=' + side + '&lpath=' + lpth + '&rpath=' + rpth + '&link=' + document.getElementById('link_' + side + current).href;
			window.location=dest;
			}
		//else if (key==404) 
		//	{
			//the green button on the remote control have been pressed
			//Switch to the Keyboard
		//	top.frames["Keyboard"].focus();
		//	}
		else if (key==461) 
			{
			//the back button on the remote control have been pressed
			//NetCastBack API
			//window.NetCastBack();
			//lets get back to WebUI instead of closing NetCast service
			history.go(-1);
			//Prevent default action
			return false;
			}
		else if (key==1001) 
			{
			//the exit button on the remote control have been pressed
			//NetCastExit API
			window.NetCastExit();
			//Prevent default action
			return false;
			}
		}catch(Exception){}
	if (e.stopPropagation)
	    {
	    e.stopPropagation();
	    e.preventDefault();
	    }
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



#if [ "$type" = "menu" ]
#then
    echo '<center><font size="+1" color="yellow"><b>OpenLGTV BCM FileManager</b> by xeros</font><br/>'
    echo '<font size="+3">'
    echo "<table id='fullheight' width='100%' border='1' cellspacing='5' bgcolor='white' style='min-height:700px; height:700px; max-height=700px;' padding='0' cellpadding='0px'>"
    echo "<thead><tr border='1' height='20px'><td valign='top' align='center' bgcolor='yellow' width='50%'><b>$lpth/</b></td><td valign='top' align='center' bgcolor='yellow' width='50%'><b>$rpth/</b></td></tr></thead>"
    echo "<tbody id='main'><tr><td valign='top' width='50%' class='panel'>"
    echo '<Table id="fullheight" name="items" class="items" Border=0 cellspacing=0 width="100%"><tbody class="scrollable">'
    if [ "$lpth" != "" ]
    then
	lpth_up="${lpth%/*}"
	echo "<tr id=\"tr_l1\"><td class='filename'><img src=\"Images/file_icons/dir.gif\"/><a id=\"link_l1\" href=\"fm.cgi?type=related&side=l&lpth=$lpth_up&rpth=$rpth\" target=\"_parent\"><font size='+1'><b>..</b></font><br/></a></td><td align=\"right\">---&nbsp;&nbsp;</td><td>---</td></tr>"
	litem_nr=2
    else
	litem_nr=1
    fi
    SIFS="$IFS"
    IFS=$'\n'
    for lcontent in `busybox stat -c "%n@%F@%z@%A@%s" $lpth/* | grep "@directory" | sed -e "s#$lpth/##g" -e 's# #\&nbsp;#g'` `busybox stat -c "%n@%F@%z@%A@%s" $lpth/* | grep -v "@directory" | sed -e "s#$lpth/##g" -e 's# #\&nbsp;#g'` 
    do
	lfilename="${lcontent%%@*}"
	lfilename_space="${lfilename//&nbsp;/ }"
	lfilename_ext="${lfilename_space##*.}"
	if [ "${#lfilename_space}" -gt "53" ]
	then
	    if [ "$ltype" = "directory" ]
	    then
		lfilename="${lfilename_space:0:53}~"
		lfilename="${lfilename// /&nbsp;}"
	    else
		lfilename="${lfilename_space:0:50}~.${lfilename_ext}"
		lfilename="${lfilename// /&nbsp;}"
	    fi
	fi
	lcontent_2x="${lcontent#*@}" # from 2nd columnt up to end
	ltype="${lcontent_2x%%@*}"
	lcontent_3x="${lcontent_2x#*@}" # from 3rd columnt up to end
	ldate="${lcontent_3x%%@*}"
	ldate_cut="${ldate%%.*}"
	lcontent_4x="${lcontent_3x#*@}" # from 4th columnt up to end
	lperm="${lcontent_4x%%@*}"
	lcontent_5x="${lcontent_4x#*@}" # from 5th columnt up to end
	lsize="${lcontent_5x%%@*}"
	if [ "$ltype" = "directory" ]
	then
	    limage="dir.gif"
	    dlink="fm.cgi?type=related&side=l&lpth=$lpth/$lfilename_space&rpth=$rpth"
	else
	    limage="generic.gif"
	    #if [ "${lfilename_ext}" != "" ]
	    #then
		#case "${lfilename_ext}" in
		#    avi ) dlink="fm-action.cgi?action=play&side=$side&lpath=$lpth/$lfilename_space&rpath=$rpth&link=$lpth/$lfilename_space";;
		#    *) dlink="fm.cgi?type=related&side=l&lpth=$lpth/$lfilename_space&rpth=$rpth";;
		#esac
	    #else
		dlink="fm.cgi?type=related&side=l&lpth=$lpth/$lfilename_space&rpth=$rpth"
	    #fi
	fi
	echo "<tr id=\"tr_l${litem_nr}\"><td class='filename'><img src=\"Images/file_icons/$limage\"/><a id=\"link_l${litem_nr}\" href=\"$dlink\" target=\"_parent\"><font size='+0'><b>$lfilename</b></font></a></td><td align=\"right\">$lsize&nbsp;&nbsp;</td><td>$ldate_cut</td></tr>"
	litem_nr=$(($litem_nr+1))
    done
    IFS="$SIFS"
    echo '</tbody></table></td><td valign="top" width="50%" class="panel">'
    echo '<Table id="fullheight" name="items" class="items" Border=0 cellspacing=0 width="100%"><tbody class="scrollable">'
    if [ "$rpth" != "" ]
    then
	rpth_up="${rpth%/*}"
	echo "<tr id=\"tr_r1\"><td class='filename'><img src=\"Images/file_icons/dir.gif\"/><a id=\"link_r1\" href=\"fm.cgi?type=related&side=r&rpth=$rpth_up&lpth=$lpth\" target=\"_parent\"><font size='+1'><b>..</b></font><br/></a></td><td align=\"right\">---&nbsp;&nbsp;</td><td>---</td></tr>"
	ritem_nr=2
    else
	ritem_nr=1
    fi
    SIFS="$IFS"
    IFS=$'\n'
    for rcontent in `busybox stat -c "%n@%F@%z@%A@%s" $rpth/* | grep "@directory" | sed -e "s#$rpth/##g" -e 's# #\&nbsp;#g'` `busybox stat -c "%n@%F@%z@%A@%s" $rpth/* | grep -v "@directory" | sed -e "s#$rpth/##g" -e 's# #\&nbsp;#g'` 
    do
	rfilename="${rcontent%%@*}"
	rfilename_space="${rfilename//&nbsp;/ }"
	if [ "${#rfilename_space}" -gt "53" ]
	then
	    if [ "$rtype" = "directory" ]
	    then
		rfilename="${rfilename_space:0:53}~"
		rfilename="${rfilename// /&nbsp;}"
	    else
		rfilename="${rfilename_space:0:50}~.${rfilename_space##*.}"
		rfilename="${rfilename// /&nbsp;}"
	    fi
	fi
	rcontent_2x="${rcontent#*@}" # from 2nd columnt up to end
	rtype="${rcontent_2x%%@*}"
	rcontent_3x="${rcontent_2x#*@}" # from 3rd columnt up to end
	rdate="${rcontent_3x%%@*}"
	rdate_cut="${rdate%%.*}"
	rcontent_4x="${rcontent_3x#*@}" # from 4th columnt up to end
	rperm="${rcontent_4x%%@*}"
	rcontent_5x="${rcontent_4x#*@}" # from 5th columnt up to end
	rsize="${rcontent_5x%%@*}"
	if [ "$rtype" = "directory" ]
	then
	    rimage="dir.gif"
	else
	    rimage="generic.gif"
	fi
	echo "<tr id=\"tr_r${ritem_nr}\"><td class='filename'><img src=\"Images/file_icons/$rimage\"/><a id=\"link_r${ritem_nr}\" href=\"fm.cgi?type=related&side=r&rpth=$rpth/$rfilename_space&lpth=$lpth\" target=\"_parent\"><font size='+0'><b>$rfilename</b></font></a></td><td align=\"right\">$rsize&nbsp;&nbsp;</td><td>$rdate_cut</td></tr>"
	ritem_nr=$(($ritem_nr+1))
    done
    IFS="$SIFS"
    echo '</tbody></table></td></tr></tbody>'
    echo '</table></font></center>'
?>
</BODY></HTML>

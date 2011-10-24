#!/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- filemanager.cgi by xeros -->
<!-- Source code released under GPL License -->

<!-- warn: it is just a start of coding... -->

<style type="text/css">
    #fullheight{height:500px}
    body {
	font-family:monospace;
	height: 500px;
	//font-family:"TiresiasScreenfont";
    }
    a:link {
	color:black;
	text-decoration:bold;
    }
    tbody {
	height: 70%;
	overflow:scroll;
	//height:10em;
    }
</style>
<title>CGI FileManager by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

<?

#useragent="tv_samsung/4"
#useragent="Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"
#useragent="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"
menuLoc="fm.cgi?ls=/"

#if [ "$FORM_url" != "" ]
#then
#    url="$FORM_url"
#    type="$FORM_type"
#    log_file=/tmp/log/vod/ipla/$type.log
#    echo "var col = 3; //number of 'cells' in a row"
#else
#    url="$menuLoc"
#    type=menu
#    log_file=/tmp/log/vod/ipla/$type.log
    echo "var col = 1; //number of 'cells' in a row"
#fi

log_file=/tmp/log/fm/fm.log

if [ ! -d "/tmp/log/fm" ]
then
    mkdir -p /tmp/log/fm
fi

if [ "$FORM_side" != "" ]
then
    echo "var side = '$FORM_side'"
    export side="$FORM_side"
else
    echo "var side = 'l'"
    export side="l"
fi

?>

var current = 1;
var next = current;
//var side = 'l';
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
			case 33: next = (1*current) - 20; break; //ch up
			case 34: next = (1*current) + 20; break; //ch down
			case 37: next = current; nside = 'l'; break; //left
			case 38: next = current - col; break; //up
			case 39: next = current; nside = 'r'; break; //right
			case 40: next = (1*current) + col; break; //down
			}
		//alert('key: '+key+' current: '+current+' next: '+next);
		if (key==33|key==34|key==37|key==38|key==39|key==40)
			{
			if (next==0)
			    {
				next = 1;
			    }
			//Check if new link exists, if not then go to previous one until finds the one that exists
			if (!document.links['link_' + nside + next])
			{
			    //alert('link_' + side + current + ' link_' + nside + next);
			    do {
				next = next - 1;
			    } while ((!document.links['link_' + nside + next])&&(next >= 1));
			}
			ChangeBgColor();
			//Move to the next bookmark
			var code=document.links['link_' + nside + next].name;
			document.links['link_' + nside + next].focus();
			//set TD background
			//document.getElementById('td' + next).style.backgroundImage = 'url(Images/EmptyBookmarkFocus.png)';
			//document.getElementById('td' + current).style.backgroundImage = 'url(Images/EmptyBookmarkNoFocus.png)';
			//set current=next
			current = next;
			side = nside;
			//Prevent scrolling
			return false;
			}
		else if (key==32) 
			{
			    //alert('link_' + side + current + ' link_' + nside + next);
			    alert(document.getElementById('link_' + side + current).href); // link destination
			    alert(document.getElementById('link_' + side + current).text); // link name
			}
		else if (key==404) 
			{
			//the green button on the remote control have been pressed
			//Switch to the Keyboard
			top.frames["Keyboard"].focus();
			}
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

#wget -q -U "$useragent" -O - "$url" > $log_file

if [ "$FORM_lpth" != "" ]
then
    lpth="$FORM_lpth"
fi

if [ "$FORM_rpth" != "" ]
then
    rpth="$FORM_rpth"
fi

#echo "side: $side"

#echo "$url $log_file <br/>"

#if [ "$type" = "menu" ]
#then
    echo '<center><font size="+1" color="yellow"><b>OpenLGTV BCM FileManager</b> by xeros</font><br/>'
    echo '<font size="+3">'
    echo "<table id='fullheight' width='100%' border='1' cellspacing='5' bgcolor='white' style='min-height:515px; height:515px' padding='0' cellpadding='0px'>"
    echo "<thead><tr border='1'><td width='50%' valign='top' align='center' bgcolor='yellow'><b>$lpth/</b></td><td width='50%' valign='top' align='center' bgcolor='yellow'><b>$rpth/</b></td></tr></thead>"
    echo "<tbody><tr><td width='50%' valign='top' style='min-height:515px; height:515px'>"
    echo '<Table id="fullheight" name="items" class="items" Border=0 cellspacing=0 width="100%">'
    if [ "$lpth" != "" ]
    then
	lpth_up="${lpth%/*}"
	echo "<tr id=\"tr_l1\"><td><img src=\"Images/file_icons/dir.gif\"/><a id=\"link_l1\" href=\"fm.cgi?type=related&side=l&lpth=$lpth_up&rpth=$rpth\" target=\"_parent\"><font size='+1'><b>..</b></font><br/></a></td><td align=\"right\">---&nbsp;&nbsp;</td><td>---</td></tr>"
	litem_nr=2
    else
	litem_nr=1
    fi
    SIFS="$IFS"
    IFS=$'\n'
    #for lcontent in `busybox stat -c "%n@%F@%z@%A@%s" $lpth/* | sed -e "s#$lpth/##g" -e 's# #\&nbsp;#g'`
    for lcontent in `busybox stat -c "%n@%F@%z@%A@%s" $lpth/* | grep "@directory" | sed -e "s#$lpth/##g" -e 's# #\&nbsp;#g'` `busybox stat -c "%n@%F@%z@%A@%s" $lpth/* | grep -v "@directory" | sed -e "s#$lpth/##g" -e 's# #\&nbsp;#g'` 
    do
	#echo "$i"
	#echo "$lcontent"
	#lcontent=`busybox stat -c "%n@%F@%z@%A@%s" "$i" | sed -e "s#$lpth/##g" -e 's# #\&nbsp;#g'`
	#filename="${content:57}"
	#filename="${content#*@}"
	lfilename="${lcontent%%@*}"
	lfilename_space="${lfilename//&nbsp;/ }"
	if [ "${#lfilename_space}" -gt "50" ]
	then
	    lfilename="${lfilename:0:45}~.${lfilename_space##*.}"
	fi
	lcontent_2x="${lcontent#*@}" # from 2nd columnt up to end
	ltype="${lcontent_2x%%@*}"
	lcontent_3x="${lcontent_2x#*@}" # from 3rd columnt up to end
	#date="${content:44:13}"
	ldate="${lcontent_3x%%@*}"
	ldate_cut="${ldate%%.*}"
	lcontent_4x="${lcontent_3x#*@}" # from 4th columnt up to end
	lperm="${lcontent_4x%%@*}"
	lcontent_5x="${lcontent_4x#*@}" # from 5th columnt up to end
	#size="${content:34:13}"
	lsize="${lcontent_5x%%@*}"
	#filename="${content_3x}"
	#feedUrl=`echo $content | sed 's/\",\"/\"\n\"/g' | grep -i \"feedUrl\" | awk -F: '{print $2}' | tr -d '\"'`
	#feedTitle=`echo $content | sed 's/\",\"/\"\n\"/g' | grep -i \"feedTitle\" | awk -F: '{print $2}' | sed 's/\#\#/ /g' | tr -d '\"'`
	#if [ "`echo $content | grep '/category/'`" ]
	#then
	#    echo "<tr><td><center><font size='+3'><b><a id=\"link$item_nr\" href=\"ipla.cgi?type=category&url=http://$feedUrl\" target=\"_parent\">$feedTitle</a></b></font></center><br/></td></tr>"
	#else
	#    echo "<tr><td><center><font size='+3'><b><a id=\"link$item_nr\" href=\"ipla.cgi?type=related&url=http://$feedUrl\" target=\"_parent\">$feedTitle</a></b></font></center><br/></td></tr>"
	#fi
	#echo "<tr><td><font size='+1'><b><a id=\"link$item_nr\" href=\"fm.cgi?type=related&pth=$pth\" target=\"_parent\">$content X $filename Y $date Z $size</a></b></font><br/></td></tr>"
	if [ "$ltype" = "directory" ]
	then
	    limage="dir.gif"
	else
	    limage="generic.gif"
	fi
	echo "<tr id=\"tr_l${litem_nr}\"><td><img src=\"Images/file_icons/$limage\"/><a id=\"link_l${litem_nr}\" href=\"fm.cgi?type=related&side=l&lpth=$lpth/$lfilename_space&rpth=$rpth\" target=\"_parent\"><font size='+0'><b>$lfilename</b></font><br/></a></td><td align=\"right\">$lsize&nbsp;&nbsp;</td><td>$ldate_cut</td></tr>"
	#echo "<tr><td><font size='+1'><b><a id=\"link$item_nr\" href=\"fm.cgi?type=related&pth=$pth\" target=\"_parent\">$content</a></b></font><br/></td></tr>"
	litem_nr=$(($litem_nr+1))
    done
    IFS="$SIFS"
    echo '</table></td><td width="50%" valign="top" style="min-height:515px; height:515px">'
    echo '<Table id="fullheight" name="items" class="items" Border=0 cellspacing=0 width="100%">'
    if [ "$rpth" != "" ]
    then
	rpth_up="${rpth%/*}"
	echo "<tr id=\"tr_r1\"><td><img src=\"Images/file_icons/dir.gif\"/><a id=\"link_r1\" href=\"fm.cgi?type=related&side=r&rpth=$rpth_up&lpth=$lpth\" target=\"_parent\"><font size='+1'><b>..</b></font><br/></a></td><td align=\"right\">---&nbsp;&nbsp;</td><td>---</td></tr>"
	ritem_nr=2
    else
	ritem_nr=1
    fi
    SIFS="$IFS"
    IFS=$'\n'
    #for rcontent in `busybox stat -c "%n@%F@%z@%A@%s" $rpth/* | sed -e "s#$rpth/##g" -e 's# #\&nbsp;#g'`
    for rcontent in `busybox stat -c "%n@%F@%z@%A@%s" $rpth/* | grep "@directory" | sed -e "s#$rpth/##g" -e 's# #\&nbsp;#g'` `busybox stat -c "%n@%F@%z@%A@%s" $rpth/* | grep -v "@directory" | sed -e "s#$rpth/##g" -e 's# #\&nbsp;#g'` 
    do
	#echo "$i"
	#echo "$lcontent"
	#lcontent=`busybox stat -c "%n@%F@%z@%A@%s" "$i" | sed -e "s#$lpth/##g" -e 's# #\&nbsp;#g'`
	#filename="${content:57}"
	#filename="${content#*@}"
	rfilename="${rcontent%%@*}"
	rfilename_space="${rfilename//&nbsp;/ }"
	if [ "${#rfilename_space}" -gt "50" ]
	then
	    rfilename="${rfilename:0:45}~.${rfilename_space##*.}"
	fi
	rcontent_2x="${rcontent#*@}" # from 2nd columnt up to end
	rtype="${rcontent_2x%%@*}"
	rcontent_3x="${rcontent_2x#*@}" # from 3rd columnt up to end
	#date="${content:44:13}"
	rdate="${rcontent_3x%%@*}"
	rdate_cut="${rdate%%.*}"
	rcontent_4x="${rcontent_3x#*@}" # from 4th columnt up to end
	rperm="${rcontent_4x%%@*}"
	rcontent_5x="${rcontent_4x#*@}" # from 5th columnt up to end
	#size="${content:34:13}"
	rsize="${rcontent_5x%%@*}"
	#filename="${content_3x}"
	#feedUrl=`echo $content | sed 's/\",\"/\"\n\"/g' | grep -i \"feedUrl\" | awk -F: '{print $2}' | tr -d '\"'`
	#feedTitle=`echo $content | sed 's/\",\"/\"\n\"/g' | grep -i \"feedTitle\" | awk -F: '{print $2}' | sed 's/\#\#/ /g' | tr -d '\"'`
	#if [ "`echo $content | grep '/category/'`" ]
	#then
	#    echo "<tr><td><center><font size='+3'><b><a id=\"link$item_nr\" href=\"ipla.cgi?type=category&url=http://$feedUrl\" target=\"_parent\">$feedTitle</a></b></font></center><br/></td></tr>"
	#else
	#    echo "<tr><td><center><font size='+3'><b><a id=\"link$item_nr\" href=\"ipla.cgi?type=related&url=http://$feedUrl\" target=\"_parent\">$feedTitle</a></b></font></center><br/></td></tr>"
	#fi
	#echo "<tr><td><font size='+1'><b><a id=\"link$item_nr\" href=\"fm.cgi?type=related&pth=$pth\" target=\"_parent\">$content X $filename Y $date Z $size</a></b></font><br/></td></tr>"
	if [ "$rtype" = "directory" ]
	then
	    rimage="dir.gif"
	else
	    rimage="generic.gif"
	fi
	echo "<tr id=\"tr_r${ritem_nr}\"><td><img src=\"Images/file_icons/$rimage\"/><a id=\"link_r${ritem_nr}\" href=\"fm.cgi?type=related&side=r&rpth=$rpth/$rfilename_space&lpth=$lpth\" target=\"_parent\"><font size='+0'><b>$rfilename</b></font><br/></a></td><td align=\"right\">$rsize&nbsp;&nbsp;</td><td>$rdate_cut</td></tr>"
	#echo "<tr><td><font size='+1'><b><a id=\"link$item_nr\" href=\"fm.cgi?type=related&pth=$pth\" target=\"_parent\">$content</a></b></font><br/></td></tr>"
	ritem_nr=$(($ritem_nr+1))
    done
    IFS="$SIFS"
    echo '</tbody></table></td></tr>'
    echo '</table></font></center>'
?>
</BODY></HTML>

<? exit 0 ?>

<?
#else
    echo '<font size="+1">'
    echo '<Table id="items" name="items" class="items" Border=0 cellspacing=0 width="100%">'
    echo '<tr>'
    item_nr=1
    if [ "$type" = "category" ]
    then
	for content in `egrep -i '\"thumb\"|\"url\"|\"title\"|\{|\}' $log_file | tr '\n' ' ' | tr '{}' '\n' | grep -i "/category/" | sed -e 's/  */ /g' -e 's/ "/"/g' -e 's/ /\#\#/g' -e 's/\",/\"!#!/g' -e 's#http://##g'`
	do
	    feedUrl=`echo $content | sed 's/!#!/\n/g' | grep -i "\"url\":" | awk -F: '{print $2}' | tr -d '\"'`
	    feedThumb=`echo $content | sed 's/!#!/\n/g' | grep -i "\"thumb\":" | awk -F: '{print $2}' | tr -d '\"'`
	    feedTitle=`echo $content | sed 's/!#!/\n/g' | grep -i "\"title\":" | awk -F: '{print $2}' | tr -d '\"' | sed -e 's/\#\#/ /g' -e 's/u0\(...\)/\&\#x0\1\;/g'`
	    echo "<td width='110px'><a id=\"link$item_nr\" href=\"ipla.cgi?type=category2&url=http://$feedUrl\" target=\"_parent\"><img src=\"http://$feedThumb\"/></td><td width='33%'><b>$feedTitle</b></a></td>"
	    if [ "$(($item_nr % 3))" = "0" ]
	    then
		echo "</tr><tr>"
	    fi
	    item_nr=$(($item_nr+1))
	done
    else
	#if [ "$type" = "category2" ]
	    for content in `egrep -i '\"date\"|\"video\"|\"thumb\"|\"url\"|\"title\"|\{|\}' $log_file | tr '\n' ' ' | tr '{}' '\n' | grep -i "/movies/" | sed -e 's/  */ /g' -e 's/\" /\"/g' -e 's/ \"/\"/g' -e 's/ /\#\#/g' -e 's/\",/\"!#!/g' -e 's#http://#http//#g'`
	    do
		feedDate=`echo $content | sed 's/!#!/\n/g' | grep -i "\"date\":" | awk -F: '{print $2}' | tr -d '\"'`
		feedThumb=`echo $content | sed 's/!#!/\n/g' | grep -i "\"thumb\":" | awk -F: '{print $2}' | sed 's#http//#http://#g' | tr -d '\"'`
		feedTitle=`echo $content | sed 's/!#!/\n/g' | grep -i "\"title\":" | awk -F: '{print $2}' | sed 's#http//#http://#g' | tr -d '\"' | sed -e 's/\#\#/ /g' -e 's/u0\(...\)/\&\#x0\1\;/g'`
		feedVideo=`echo $content | sed 's/!#!/\n/g' | grep -i "\"video\":" | awk -F: '{print $2}' | sed 's#http//#http://#g' | tr -d '\"'`
		echo "<td width='33%'><center><a id=\"link$item_nr\" href=\"$feedVideo\" target=\"_parent\"><img src=\"$feedThumb\"/><br/><b>$feedDate<br/>$feedTitle</b></a></center></td>"
		if [ "$(($item_nr % 3))" = "0" ]
		then
		    echo "</tr><tr>"
		fi
		item_nr=$(($item_nr+1))
	    done
	#fi
    fi
    echo '</tr>'
    echo '</table>'
    #echo "item_nr: $item_nr"
fi

?>

</font></center>
</BODY></HTML>

#!/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- ipla.cgi by xeros -->
<!-- Source code released under GPL License -->

<style type="text/css">
    body {
	font-family:"TiresiasScreenfont";
    }
    a:link {
	color:black;
	text-decoration:bold;
    }
</style>
<title>Ipla.tv alternative by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

<?

useragent="tv_samsung/4"
menuLoc="http://getmedia.redefine.pl/tv/menu.json?login=common_user&passwdmd5="

if [ "$FORM_url" != "" ]
then
    url="$FORM_url"
    type="$FORM_type"
    log_file=/tmp/log/vod/ipla/$type.log
    echo "var col = 3; //number of 'cells' in a row"
else
    url="$menuLoc"
    type=menu
    log_file=/tmp/log/vod/ipla/$type.log
    echo "var col = 1; //number of 'cells' in a row"
fi

if [ ! -d "/tmp/log/vod/ipla" ]
then
    mkdir -p /tmp/log/vod/ipla
fi

?>

var current;
var next;

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
			case 37: next = current - 1; break; //left
			case 38: next = current - col; break; //up
			case 39: next = (1*current) + 1; break; //right
			case 40: next = (1*current) + col; break; //down
			}
		//alert('key: '+key+' current: '+current+' next: '+next);
		if (key==37|key==38|key==39|key==40)
			{
			//Move to the next bookmark
			var code=document.links['link' + next].name;
			document.links['link' + next].focus();
			//set TD background
			//document.getElementById('td' + next).style.backgroundImage = 'url(Images/EmptyBookmarkFocus.png)';
			//document.getElementById('td' + current).style.backgroundImage = 'url(Images/EmptyBookmarkNoFocus.png)';
			//set current=next
			current = next;
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
	document.links['link1'].focus();
	}
	
document.defaultAction = true;


// -->
</script>


</HEAD>
<BODY bgcolor="green">

<?

wget -q -U "$useragent" -O - "$url" > $log_file

#echo "$url $log_file <br/>"

if [ "$type" = "menu" ]
then
    echo '<center><img src="http://www.ipla.tv/images/logo.png"/><font size="+3"><br/>alternative</font><br/>by xeros<br/><br/>'
    echo '<font size="+3">'
    echo '<Table id="items" name="items" class="items" Border=0 cellspacing=0 width="100%">'
    item_nr=1
    for content in `cat $log_file | tr '\n' ' ' | tr '{}' '\n' | grep feed | sed -e 's/ */ /g' -e 's/ \"/\"/g' -e 's#http://##g' -e 's/ /\#\#/g'`
    do
	feedUrl=`echo $content | sed 's/\",\"/\"\n\"/g' | grep -i \"feedUrl\" | awk -F: '{print $2}' | tr -d '\"'`
	feedTitle=`echo $content | sed 's/\",\"/\"\n\"/g' | grep -i \"feedTitle\" | awk -F: '{print $2}' | sed 's/\#\#/ /g' | tr -d '\"'`
	if [ "`echo $content | grep '/category/'`" ]
	then
	    echo "<tr><td><center><font size='+3'><b><a id=\"link$item_nr\" href=\"ipla.cgi?type=category&url=http://$feedUrl\" target=\"_parent\">$feedTitle</a></b></font></center><br/></td></tr>"
	else
	    echo "<tr><td><center><font size='+3'><b><a id=\"link$item_nr\" href=\"ipla.cgi?type=related&url=http://$feedUrl\" target=\"_parent\">$feedTitle</a></b></font></center><br/></td></tr>"
	fi
	item_nr=$(($item_nr+1))
    done
else
    echo '<font size="+1">'
    echo '<Table id="items" name="items" class="items" Border=0 cellspacing=0 width="100%">'
    echo '<tr>'
    item_nr=1
    if [ "$type" = "category" ]
    then
	for content in `cat $log_file | egrep -i '\"thumb\"|\"url\"|\"title\"|\{|\}' | tr '\n' ' ' | tr '{}' '\n' | grep -i "/category/" | sed -e 's/ */ /g' -e 's/ "/"/g' -e 's/ /\#\#/g' -e 's/\",/\"!#!/g' -e 's#http://##g'`
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
	    for content in `cat $log_file | egrep -i '\"date\"|\"video\"|\"thumb\"|\"url\"|\"title\"|\{|\}' | tr '\n' ' ' | tr '{}' '\n' | grep -i "/movies/" | sed -e 's/ */ /g' -e 's/\" /\"/g' -e 's/ \"/\"/g' -e 's/ /\#\#/g' -e 's/\",/\"!#!/g' -e 's#http://#http//#g'`
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

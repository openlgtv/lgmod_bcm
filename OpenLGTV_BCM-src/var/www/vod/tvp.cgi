#!/bin/sh
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- tvp.cgi by xeros -->
<!-- Source code released under GPL License -->

<style>
    body {
	font-family:"TiresiasScreenfont";
    }
    a:link {
	color:black;
	text-decoration:bold;
    }
</style>
<title>tvp.pl alternative by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

var col = 3; //number of 'cells' in a row
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

<?

useragent="Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"

#menuLoc="http://getmedia.redefine.pl/tv/menu.json?login=common_user&passwdmd5="
menuLoc="http://www.tvp.pl/pub/stat/websitelisting?object_id=2919829&child_mode=SIMPLE&rec_count=32&with_subdirs=true&link_as_copy=true&xslt=internet-tv/samsung/websites_listing.xslt&q=&samsungwidget=1&v=2&5"

#deviceid="`cat /mnt/user/ywe/deviceid`"

if [ "$FORM_url" != "" ]
then
    url=`echo "$FORM_url" | tr '@$' '?&'`
    type="$FORM_type"
    log_file=/tmp/$type.log
else
    url="$menuLoc"
    type=menu-tvp
    log_file=/tmp/$type.log
fi

#url="$menuLoc"

#log_file=$RANDOM

#echo "$url $log_file <br/>"

wget -q -U "$useragent" -O - "$url" > $log_file


if [ "$type" = "video-tvp" ]
then
    cat $log_file | grep "video_url" | sed -e 's/.*video_url="/<meta HTTP-EQUIV="REFRESH" content="1; url=/g' -e 's/">.*/">/g'
fi

?>


</HEAD>
<!-- BODY background="background.png" -->
<BODY bgcolor="lightblue">



<?



if [ "$type" = "menu-tvp" ]
then
    echo '<center><img src="http://s.v3.tvp.pl/files/portal/gfx/top_nav/tvp_pl.png"/><font size="+3"><br/>alternative</font><br/>by xeros<br/></center><br/>'
    echo '<font size="+2">'
    echo '<Table id="items" name="items" class="items" Border=0 cellspacing=0 width="100%">'
    echo '<tr>'
    item_nr=1
    #for content in `cat $log_file | grep "\"feed" | tr '\n' ' ' | sed -e 's/\(\"feedUrl\"\)/\n\1/g' -e 's/ */ /g' -e 's/ "/"/g' -e 's/\"feedUrl\"://g' -e 's/,\"feedTitle\":/;/g' | grep "/category/"`
    for content in `cat $log_file | grep -v "^$" | sed 's/^\t*//g' | tr '\n' '|' | sed 's/<object/\n<object/g' | grep -v 'version="1.0"' | sed -e 's/.*url="//g' | awk -F\| '{print "http://www.tvp.pl" $1 ";" $2 ";" $3}' | sed -e 's/" view="ProgramView">;<title>/;/g' -e 's#</title>##g' -e 's/ /|/g'`
    do
	feedUrl=`echo $content | awk -F\; '{print $1}' | tr '\?\&' '\@\$'`
	#feedTitle=`echo $content | awk -F\; '{print $2}' | tr -d '\"' | sed -e 's/\\\u\(....\)/\&#x\1;/g'`
	feedTitle=`echo $content | awk -F\; '{print $2}' | tr '|' ' '`
	feedThumb=`echo $content | awk -F\; '{print $3}' | tr '|' ' '`
	#echo "$feedUrl"
	echo "<td width='33%'><center><a id=\"link$item_nr\" href=\"tvp.cgi?type=category-tvp&url=$feedUrl\">$feedThumb<br/><font size='+2'>$feedTitle</font></a></center></td>"
	if [ "$(($item_nr % 3))" = "0" ]
	then
	    echo "</tr><tr>"
	fi
	item_nr=$(($item_nr+1))
    done
    echo '</tr>'
    echo '</table>'
    #echo "item_nr: $item_nr"
else
    echo '<font size="+1">'
    echo '<Table id="items" name="items" class="items" Border=0 cellspacing=0 width="100%">'
    echo '<tr>'
    item_nr=1
    if [ "$type" = "category-tvp" ]
    then
	for content in `cat $log_file | sed 's/<object/\n<object/g' | grep "VideoView" | sed -e 's#"/><img.*"/>#"/>#g' -e 's/></>|</g' -e 's/.*url="//g' | awk -F\| '{print "http://www.tvp.pl" $1 ";" $2 ";" $3}' | sed -e 's/;<title>/;/g' -e 's#</title>##g' -e 's/ /|/g' -e 's/">;<img/;<img/g'`
	do
	    feedUrl=`echo $content | awk -F\; '{print $1}' | tr '\?\&' '\@\$'`
	    feedThumb=`echo $content | awk -F\; '{print $2}' | tr '|' ' '`
	    # v- better works on PC
	    #feedTitle=`echo $content | awk -F\; '{print $3}' | tr -d '\"' | sed -e 's/\\\u\(....\)/\&#x\1;/g'`
	    # v- better work in TV
	    #feedTitle=`echo $content | awk -F\; '{print $3}' | tr -d '\"' | sed 's/\\u\(....\)/\&\#x\1\;/g'`
	    # v- not proper regex code but looks like backslash (in "\uXXXX") is being lost somewhere with BusyBox tools
	    #feedTitle=`echo $content | awk -F\; '{print $3}' | tr -d '\"' | sed -e 's/\#\#/ /g' -e 's/u0\(...\)/\&\#x0\1\;/g'`
	    feedTitle=`echo $content | awk -F\; '{print $3}' | tr '|' ' '`
	    echo "<td><center><a id=\"link$item_nr\" href=\"tvp.cgi?type=video-tvp&url=$feedUrl\" target=\"_parent\">$feedThumb</a></center></td><td>$feedTitle</td>"
	    if [ "$(($item_nr % 3))" = "0" ]
	    then
		echo "</tr><tr>"
	    fi
	    item_nr=$(($item_nr+1))
	done
    fi
    echo '</tr>'
    echo '</table>'
    #echo "item_nr: $item_nr"
fi

?>
</font>
</BODY></HTML>

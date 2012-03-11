#!/usr/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- tvp.cgi by xeros -->
<!-- Source code released under GPL License -->

<style type="text/css">
    body {
	font-family:"TiresiasScreenfont";
    }
    a:link,
    a:visited {
	color: black;
	background-color: lightblue;
	text-decoration: bold;
    }
    a:hover,
    a:focus,
    a:active {
	color: #CC0000;
	background-color: lightblue;
	text-decoration: bold;
    }
</style>
<title>tvp.pl alternative by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

var col = 4; //number of 'cells' in a row
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
			case 33: next = (1*current) - (5*col); break; //ch up
			case 34: next = (1*current) + (5*col); break; //ch down
			case 37: next = current - 1; break; //left
			case 38: next = current - col; break; //up
			case 39: next = (1*current) + 1; break; //right
			case 40: next = (1*current) + col; break; //down
			}
		if (key==33|key==34|key==37|key==38|key==39|key==40)
			{
			//Move to the next bookmark
			var code=document.links['link' + next].name;
			document.links['link' + next].focus();
			current = next;
			//Prevent scrolling
			return false;
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
	document.links['link1'].focus();
	}
	
document.defaultAction = true;


// -->
</script>

<?

useragent="Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"

#menuLoc="http://www.tvp.pl/pub/stat/websitelisting?object_id=2919829&child_mode=SIMPLE&rec_count=32&with_subdirs=true&link_as_copy=true&xslt=internet-tv/samsung/websites_listing.xslt&q=&samsungwidget=1&v=2&5"
menuLoc="http://www.tvp.pl/pub/stat/websitelisting?object_id=2919829&child_mode=SIMPLE&rec_count=64&with_subdirs=true&link_as_copy=true&xslt=internet-tv/samsung/websites_listing.xslt&q=&samsungwidget=1&v=2&5"
log_dir="/var/log/vod/tvp"

if [ "$FORM_url" != "" ]
then
    url=`echo "$FORM_url" | tr '@$' '?&'`
    type="$FORM_type"
else
    url="$menuLoc"
    type=menu-tvp
fi
log_file="$log_dir/$type.log"

[ ! -d "$log_dir" ] && mkdir -p "$log_dir"

wget -q -U "$useragent" -O - "$url" > $log_file


if [ "$type" = "video-tvp" ]
then
    grep "video_url" $log_file | sed -e 's/.*video_url="/<meta HTTP-EQUIV="REFRESH" content="1; url=/g' -e 's/">.*/">/g'
fi

echo '</HEAD><BODY bgcolor="lightblue">'

if [ "$type" = "menu-tvp" ]
then
    echo '<center><img src="http://s.v3.tvp.pl/files/portal/gfx/top_nav/tvp_pl.png"/><font size="+2"><br/>alternative</font><br/>by xeros<br/></center>'
    echo '<Table id="items" name="items" class="items" Border=0 cellspacing=0 width="100%">'
    echo '<tr>'
    item_nr=1
    for content in `egrep -v 'version=|^$' $log_file | tr '\n\t' '|' | sed 's/<object/\n<object/g' | sed -e 's/.*url="//g' -e 's/\&amp;/\$/g' | awk -F\| '{print "http://www.tvp.pl" $1 ";" $2 ";" $3}' | sed -e 's/" view="ProgramView">;<title>/;/g' -e 's#</title>##g' -e 's/ /|/g'`
    do
	if [ "$content" != "http://www.tvp.pl;;" ]
	then
	    feedUrl="${content%%\;*}"
	    #feedUrl="${feedUrl/\$sort_by=RELEASE_DATE/}"
	    content2x="${content#*\;}"
	    feedTitle="${content2x%%\;*}"
	    content3x="${content2x#*\;}"
	    feedThumb="${content3x%%\;*}"
	    echo "<td width='25%'><center><a id=\"link$item_nr\" href=\"tvp.cgi?type=category-tvp&url=$feedUrl\">$feedThumb<br/><font size='+2'>$feedTitle</font></a></center></td>" | tr '|' ' '
	    [ "$(($item_nr % 4))" = "0" ] && echo "</tr><tr>"
	    item_nr=$(($item_nr+1))
	fi
    done
    echo "<td width='25%'><center><a id=\"link$item_nr\" href=\"tvp.cgi?type=category-tvp&url=http://www.tvp.pl/pub/sess/samsungvideolistingwrapper?object_id=1364\$play_mode=VOD\$sort_by=RELEASE_DATE\$rec_count=128\$with_subdirs=true\$child_mode=SIMPLE\$xslt=internet-tv/samsung/website_details_wrapper.xslt\"><img src='http://s.v3.tvp.pl/images/a/c/a/uid_aca3c8ed7aec531f184a405e72605dbb1286707333195_width_141.jpg'><br/><font size='+2'>Maklowicz w podrozy</font></a></center></td>"
    [ "$(($item_nr % 4))" = "0" ] && echo '</tr><tr>'
    item_nr=$(($item_nr+1))
    echo "<td width='25%'><center><a id=\"link$item_nr\" href=\"tvp.cgi?type=category-tvp&url=http://www.tvp.pl/pub/sess/samsungvideolistingwrapper?object_id=118\$play_mode=VOD\$sort_by=RELEASE_DATE\$rec_count=128\$with_subdirs=true\$child_mode=SIMPLE\$xslt=internet-tv/samsung/website_details_wrapper.xslt\"><img src='http://s.v3.tvp.pl/images/9/2/7/uid_9279843b4042afeaaa9edb7302ad85101256650178480_width_141.jpg'><br/><font size='+2'>Jedynkowe Przedszkole</font></a></center></td>"
    [ "$(($item_nr % 4))" = "0" ] && echo '</tr><tr>'
    item_nr=$(($item_nr+1))
    echo "<td width='25%'><center><a id=\"link$item_nr\" href=\"tvp.cgi?type=category-tvp&url=http://www.tvp.pl/pub/sess/samsungvideolistingwrapper?object_id=1885\$play_mode=VOD\$sort_by=RELEASE_DATE\$rec_count=128\$with_subdirs=true\$child_mode=SIMPLE\$xslt=internet-tv/samsung/website_details_wrapper.xslt\">?<br/><br/><font size='+2'>Przegapiles?</font></a></center></td>"
    echo '</tr>'
    echo '</table>'
else
    echo '<font size="+1">'
    echo '<Table id="items" name="items" class="items" Border=0 cellspacing=0 width="100%">'
    echo '<tr>'
    item_nr=1
    if [ "$type" = "category-tvp" ]
    then
	for content in `cat $log_file | sed 's/<object/\n<object/g' | grep "VideoView" | sed -e 's#"/><img.*"/>#"/>#g' -e 's/></>|</g' -e 's/.*url="//g' -e 's/\&amp;/\$/g' | awk -F\| '{print "http://www.tvp.pl" $1 ";" $2 ";" $3}' | sed -e 's/;<title>/;/g' -e 's#</title>##g' -e 's/ /|/g' -e 's/">;<img/;<img/g'`
	do
	    feedUrl="${content%%\;*}"
	    content2x="${content#*\;}"
	    feedTitle="${content2x%%\;*}"
	    content3x="${content2x#*\;}"
	    feedThumb="${content3x%%\;*}"
	    echo "<td><center><a id=\"link$item_nr\" href=\"tvp.cgi?type=video-tvp&url=$feedUrl\" target=\"_parent\">$feedThumb</a></center></td><td>$feedTitle</td>" | tr '|' ' '
	    [ "$(($item_nr % 4))" = "0" ] && echo "</tr><tr>"
	    item_nr=$(($item_nr+1))
	done
    fi
    echo '</tr>'
    echo '</table>'
fi

?>
</BODY></HTML>

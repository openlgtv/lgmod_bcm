#!/usr/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- rss.cgi by xeros -->
<!-- Source code released under GPL License -->

<style type="text/css">
    body {
	font-family:"TiresiasScreenfont";
    }
    a:link {
	color:white;
	text-decoration:bold;
    }
    a:visited {
	color:yellow;
	text-decoration:bold;
    }
    img {
	max-width:300px;
    }
    font,p {
	color: white;
    }
    a:hover,
    a:focus,
    a:active,
    font:hover,
    font:focus,
    font:active {
	color: #FF6633;
    }
</style>
<title>RSS parser by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

var current;
var next;

var rows=3;

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
			case 33: next = (1*current) - (rows*col); break; //ch up
			case 34: next = (1*current) + (rows*col); break; //ch down
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

<?

col=2

[ -n "$FORM_col" ] && col="$FORM_col"

useragent="tv_samsung/4"
#menuLoc="http://tvwidget.pl/xml/linki.xml"
#menuLoc="http://tvwidget.pl/xml/lista.xml"
#menuLoc="http://files.samsung-tv.webnode.sk/200000160-9d71c9e7e8/pl-tematapodkast.xml"
menuLoc="http://bit.ly/interpodcast"

[ -n "$FORM_url"  ] && url="$FORM_url"   || url="$menuLoc"
[ -n "$FORM_type" ] && type="$FORM_type" || type="text/xml"
[ -z "$FORM_url" -a -z "$FORM_col" ] && col=4 && nextcol=2 || nextcol="$col" # let's set 4 columns for index site
maxwidth="$((1270/$col))"

echo "var col = $col; //number of 'cells' in a row"

echo "// --></script></HEAD>"

type2="${type#*/}"
log_dir="/var/log/vod/rss"
log_file="$log_dir/$type2.log"

[ ! -d "$log_dir" ] && mkdir -p "$log_dir"

if [ "$type" = "text/xml" ]
then
    wget -q -U "$useragent" "$url" -O "$log_file"
    echo '<BODY bgcolor="black">'
    echo '<center><font size="+3" style="color:yellow;">RSS<br/></font><font size="+1" style="color:yellow;">parser<br/><font size="0" style="color:grey;">by xeros<br/><br/></font>'
    echo '<Table id="items" class="items" Border="0" cellspacing="10" cellpadding="1" width="100%">'
    echo '<tr>'
    item_nr=1
    rm -f /tmp/log.log /tmp/log2.log
    for content in `cat "$log_file" | tr -d '\r' | tr '\n' ' ' | sed -e 's/<item>/\n<item>/g' | grep "<item>" | sed -e 's/\t*//g' -e 's/> *</></g' -e 's/ /|/g' -e 's/<\!\[CDATA\[//g' -e 's/\]\]>//g' | awk -F"</*item>" '{print $2}' | egrep "<enclosure|<link"`
    do
	feedTitle="${content#*<title>}"
	feedTitle="${feedTitle%%</title>*}"
	[ "$feedTitle" = "$content" ] && feedTitle=""
	feedTitle="${feedTitle//|/ }"
	feedTitle="${feedTitle//\"/}"
	feedDescription="${content#*<description>}"
	feedDescription="${feedDescription%%</description>*}"
	if [ "$feedDescription" != "$content" ]
	then
	    feedDescription="${feedDescription//|/ }"
	    feedDescription="${feedDescription//  / }"
	    feedDescription="${feedDescription//\&lt\;/<}"
	    feedDescription="${feedDescription//\&gt\;/>}"
	    feedDescription="${feedDescription//>/><br>}"
	    feedDescription="${feedDescription//p><br>/p>}"
	    feedDescription="${feedDescription//a><br>/a>}"
	    feedDescription="${feedDescription//<div*div>/}"
	else
	    feedDescription="${content#*<itunes:summary>}"
	    feedDescription="${feedDescription%%</itunes:summary>*}"
	    [ "$feedDescription" = "$content" ] && feedDescription=""
	fi
	feedThumbnail="${content#*<media:thumbnail|url=\"}"
	if [ "$feedThumbnail" != "$content" ]
	then
	    feedThumbnail="${feedThumbnail%%\"*}"
	else
	    feedThumbnail="${content#*<itunes:image>}"
	    feedThumbnail="${feedThumbnail%%</itunes:image>*}"
	    if [ "$feedThumbnail" = "$content" ]
	    then
		feedThumbnail="${content#*<media>}"
		feedThumbnail="${feedThumbnail%%</media>*}"
		#echo "feedThumbnail=$feedThumbnail" >> /tmp/log3.log
		[ "$feedThumbnail" = "$content" ] && feedThumbnail=""
	    fi
	fi
	#echo "feedThumbnail=$feedThumbnail" >> /tmp/log2.log
	feedEnclosure="${content##*<enclosure|}"
	if [ "$feedEnclosure" != "$content" ]
	then
	    feedEnclosure="${feedEnclosure%|/>*}"
	    feedUrl="${feedEnclosure#*url=\"}"
	    feedUrl="${feedUrl%%\"|*}"
	    feedUrl="${feedUrl//\"/}"
	    feedType="${feedEnclosure#*type=\"}"
	    feedType="${feedType%%\"|*}"
	    feedType="${feedType//\"/}"
	else
	    feedUrl="${content#*<link>}"
	    feedUrl="${feedUrl%%</link>*}"
	    #feedType="unknown"
	    feedType="text/xml"
	fi
	if [ -z "$feedThumbnail" ]
	then
	    echo "<td style='vertical-align:top; max-width:${maxwidth}px' valign='top'><center><a id=\"link$item_nr\" href=\"rss.cgi?type=$feedType&col=$nextcol&url=$feedUrl\" target=\"_parent\"><font size='+2'>$feedTitle<br/></font>$feedDescription</a><br/></center></td>"
	else
	    echo "<td style='vertical-align:top; max-width:${maxwidth}px' valign='top'><center><a id=\"link$item_nr\" href=\"rss.cgi?type=$feedType&col=$nextcol&url=$feedUrl\" target=\"_parent\"><img src='$feedThumbnail'><br/><font size='+2'>$feedTitle<br/></font>$feedDescription</a><br/></center></td>"
	fi
	[ "$item_nr" = "1" ] && echo "<script>OnLoadSetCurrent();</script>"
	[ "$(($item_nr % $col))" = "0" ] && echo "</tr><tr>"
	item_nr=$(($item_nr+1))
	echo "$content" >> /tmp/log.log
    done | tr '|' ' ' | sed -e 's/\(<img\)/<br\/>\1/gI' -e 's/ type=[A-Za-z0-9/]*//g' -e 's/\(&\)amp;#/\1#/g' -e 's#/>\(" target\)#\1#g' -e 's#<br[^>]*>\(<.r[^>]*>\)<br[^>]*>#\1#gI' -e 's#\(<br[^>]*>\)<br[^>]*>#\1#gI'
    echo '</tr>'
    echo '</table>'
    echo '</center>'
    echo '</BODY>'
else
    echo "<meta HTTP-EQUIV='REFRESH' content=\"1; url=$url\">"
    echo '<BODY bgcolor="black">'
    echo "Loading URL: $url ..."
    echo '</center>'
    echo '</BODY>'
fi

?>
</HTML>

#!/usr/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- netplayer.cgi by xeros -->
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
<title>NetPlayer alternative by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

var col = 2; //number of 'cells' in a row
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
		if (key==37|key==38|key==39|key==40)
			{
			//Move to the next bookmark
			var code=document.links['link' + next].name;
			document.links['link' + next].focus();
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
	document.links['link1'].focus();
	}
	
document.defaultAction = true;


// -->
</script>

</HEAD>

<?

useragent="tv_samsung/4"
#menuLoc="http://tvwidget.pl/xml/linki.xml"
#menuLoc="http://tvwidget.pl/xml/lista.xml"
menuLoc="http://files.samsung-tv.webnode.sk/200000160-9d71c9e7e8/pl-tematapodkast.xml"

[ "$FORM_url" != ""  ] && url="$FORM_url"   || url="$menuLoc"
[ "$FORM_type" != "" ] && type="$FORM_type" || type="text/xml"

type2="${type#*/}"
log_dir="/var/log/vod/netplayer"
log_file="$log_dir/$type2.log"

[ ! -d "$log_dir" ] && mkdir -p "$log_dir"

if [ "$type" = "text/xml" ]
then
    wget -q -U "$useragent" "$url" -O "$log_file"
    echo '<BODY bgcolor="black">'
    echo '<center><font size="+3" style="color:yellow;">NetPlayer<br/></font><font size="+1" style="color:yellow;">alternative<br/><font size="0" style="color:grey;">by xeros<br/><br/></font>'
    echo '<Table id="items" class="items" Border="0" cellspacing="10" cellpadding="1" width="100%">'
    echo '<tr>'
    item_nr=1
    for content in `cat "$log_file" | tr -d '\r' | tr '\n' ' ' | sed -e 's/<item>/\n<item>/g' | grep "<item>" | sed -e 's/\t*//g' -e 's/> *</></g' -e 's/ /|/g' -e 's/<\!\[CDATA\[//g' -e 's/\]\]>//g' | awk -F"</*item>" '{print $2}' | grep "<enclosure"`
    do
	#feedTitle=`echo "$content" | awk -F"</*title>" '{print $2}' | sed 's/|/ /g' | tr -d '\"'`
	feedTitle="${content#*<title>}"
	feedTitle="${feedTitle%%</title>*}"
	feedTitle="${feedTitle//|/ }"
	feedTitle="${feedTitle//\"/}"
	#feedDescription=`echo "$content" | awk -F"</*description>" '{print $2}' | sed -e 's/|/ /g' -e 's/&lt;/</g' -e 's/&gt;/>/g' -e 's#>#><br/>#g'`
	feedDescription="${content#*<description>}"
	feedDescription="${feedDescription%%</description>*}"
	feedDescription="${feedDescription//|/ }"
	feedDescription="${feedDescription//  / }"
	feedDescription="${feedDescription//\&lt\;/<}"
	feedDescription="${feedDescription//\&gt\;/>}"
	feedDescription="${feedDescription//>/><br>}"
	feedDescription="${feedDescription//p><br>/p>}"
	feedDescription="${feedDescription//a><br>/a>}"
	#feedEnclosure=`echo "$content" | awk -F"<enclosure\|" '{print $2}' | awk -F"\|/>" '{print $1}'`
	feedEnclosure="${content##*<enclosure|}"
	feedEnclosure="${feedEnclosure%|/>*}"
	#feedEnclosure="${feedEnclosure//|/ }"
	#feedEnclosure="${feedEnclosure//||/|}"
	#feedUrl=`echo "$feedEnclosure" | awk -F"url=\"" '{print $2}' | awk -F"\"\|" '{print $1}' | tr -d '\"'`
	feedUrl="${feedEnclosure#*url=\"}"
	feedUrl="${feedUrl%%\"|*}"
	feedUrl="${feedUrl//\"/}"
	#feedType=`echo "$feedEnclosure" | awk -F"type=\"" '{print $2}' | awk -F"\"\|" '{print $1}' | tr -d '\"'`
	feedType="${feedEnclosure#*type=\"}"
	feedType="${feedType%%\"|*}"
	feedType="${feedType//\"/}"
	echo "<td width='33%'><center><a id=\"link$item_nr\" href=\"netplayer.cgi?type=$feedType&amp;url=$feedUrl\" target=\"_parent\"><font size='+2'>$feedTitle<br/></font>$feedDescription</a><br/></center></td>" | tr '|' ' ' | sed -e 's/\(<img\)/<br\/>\1/g' -e 's/ type=[A-Za-z0-9/]*//g' -e 's#\(<br[^>]*>\)<br[^>]*>#\1#g' -e 's/\(&\)amp;#/\1#/g'
	[ "$(($item_nr % 2))" = "0" ] && echo "</tr><tr>"
	item_nr=$(($item_nr+1))
	#echo "$content" >> /tmp/log.log
    done
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

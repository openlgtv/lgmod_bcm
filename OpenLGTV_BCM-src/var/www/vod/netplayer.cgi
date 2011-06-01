#!/bin/haserl
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
<!-- BODY background="background.png" -->

<?

useragent="tv_samsung/4"
#menuLoc="http://getmedia.redefine.pl/tv/menu.json?login=common_user&passwdmd5="
menuLoc="http://tvwidget.pl/xml/linki.xml"

#deviceid="`cat /mnt/user/ywe/deviceid`"

if [ "$FORM_url" != "" ]
then
    url="$FORM_url"
else
    url="$menuLoc"
fi

if [ "$FORM_type" != "" ]
then
    type="$FORM_type"
else
    type=text/xml
fi

type2=`echo $type | awk -F/ '{print $2}'`
log_file=/tmp/netplayer/$type2.log

#url="$menuLoc"
?>


<?

#log_file=$RANDOM

#echo "$url $log_file <br/>"

if [ ! -d "/tmp/netplayer" ]
then
    mkdir -p /tmp/netplayer
fi

if [ "$type" = "text/xml" ]
then
    wget -q -U "$useragent" -O - "$url" > $log_file
    echo '<BODY bgcolor="black">'
    echo '<font size="+3" color="green">'
    echo '<center><!-- img src="http://www.ipla.tv/images/logo.png"/ --><font size="+3">NetPlayer<br/>alternative</font><br/>by xeros<br/><br/>'
    echo '<Table id="items" class="items" Border=0 cellspacing=0 width="100%">'
    echo '<tr>'
    item_nr=1
    #for content in `cat $log_file | grep "\"feed" | tr '\n' ' ' | sed -e 's/\(\"feedUrl\"\)/\n\1/g' -e 's/ *//g' -e '/^$/d' -e 's/\"feedUrl\"://g' -e 's/,\"feedTitle\":/;/g' | grep "/category/"`
    #for content in `cat $log_file | grep "\"feed" | tr '\n' ' ' | sed -e 's/\(\"feedUrl\"\)/\n\1/g' -e 's/ */ /g' -e 's/ "/"/g' -e 's/\"feedUrl\"://g' -e 's/,\"feedTitle\":/;/g' | grep "/category/"`
    for content in `cat $log_file | tr -d '\r' | tr '\n' ' ' | sed -e 's/<item>/\n<item>/g' -e 's/\t*//g' -e 's/> *</></g' -e 's/ /|/g' -e 's/<\!\[CDATA\[//g' -e 's/\]\]>//g' | grep "<item>" | awk -F"</*item>" '{print $2}'`
    do
	#feedTitle=`echo $content | awk -F"</*title>" '{print $2}' | tr -d '\"' | sed -e 's/\\\u\(....\)/\&#x\1;/g'`
	feedTitle=`echo $content | awk -F"</*title>" '{print $2}' | sed 's/|/ /g' | tr -d '\"'`
	feedDescription=`echo $content | awk -F"</*description>" '{print $2}' | sed -e 's/|/ /g' -e 's/&lt;/</g' -e 's/&gt;/>/g' -e 's#>#><br/>#g'`
	feedUrl=`echo $content | awk -F"<enclosure\|" '{print $2}' | awk -F"\|/>" '{print $1}' | awk -F"url=\"" '{print $2}' | awk -F"\"\|" '{print $1}' | tr -d '\"'`
	feedType=`echo $content | awk -F"<enclosure\|" '{print $2}' | awk -F"\|/>" '{print $1}' | awk -F"type=\"" '{print $2}' | awk -F"\"\|" '{print $1}' | tr -d '\"'`
	#echo "feedTitle: $feedTitle feedDescription: $feedDescription feedUrl: $feedUrl feedType: $feedType <br/>"
	echo "<td width='33%'><center><a id=\"link$item_nr\" href=\"netplayer.cgi?type=$feedType&amp;url=$feedUrl\" target=\"_parent\"><font size='+2'>$feedTitle<br/></font>$feedDescription</a><br/><br/></center></td>"
	if [ "$(($item_nr % 2))" = "0" ]
	then
	    echo "</tr><tr>"
	fi
	item_nr=$(($item_nr+1))
    done
    echo '</tr>'
    echo '</table>'
    #echo "item_nr: $item_nr"
    echo '</center></font>'
    echo '</BODY>'
else
    echo "<meta HTTP-EQUIV='REFRESH' content=\"1; url=$url\">"
    echo '<BODY bgcolor="black">'
    echo "Loading URL: $url ..."
    echo '</center></font>'
    echo '</BODY>'
fi

?>
</HTML>

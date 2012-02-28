#!/usr/bin/haserl
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
    a:link,
    a:visited {
	color: #000000;
	background-color: green;
    }
    a:hover,
    a:focus,
    a:active {
	color: #990000;
	background-color: green;
    }
</style>
<title>Ipla.tv alternative by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

<?
useragent="tv_samsung/4"
menuLoc="http://getmedia.redefine.pl/tv/menu.json?login=common_user&passwdmd5="
log_dir="/var/log/vod/ipla"
if [ "$FORM_url" != "" ]
then
    url="$FORM_url"
    type="$FORM_type"
    echo "var col = 3; //number of 'cells' in a row"
else
    url="$menuLoc"
    type=menu
    echo "var col = 1; //number of 'cells' in a row"
fi
log_file="$log_dir/$type.log"
[ ! -d "$log_dir" ] && mkdir -p "$log_dir"
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


</HEAD>
<BODY bgcolor="green">

<?
wget -q -U "$useragent" -O - "$url" > $log_file

if [ "$type" = "menu" ]
then
    echo '<br/><center><img src="../Images/tmp/iplapl.png"/><font size="+3"><br/>alternative</font><br/>by xeros<br/><br/>'
    echo '<font size="+3">'
    echo '<Table id="items" name="items" class="items" Border=0 cellspacing=0 width="100%">'
    item_nr=1
    for content in `cat $log_file | tr '\n' ' ' | tr '{}' '\n' | grep feed | sed -e 's/  */ /g' -e 's/ \"/\"/g' -e 's#http://##g' -e 's/ /\#\#/g'`
    do
	contentUrl="${content#*\"feedUrl\":\"}"
	[ "$contentUrl" != "$content" ] && feedUrl="${contentUrl%%\",*}"
	contentTitle="${content#*\"feedTitle\":\"}"
	[ "$contentTitle" != "$content" ] && feedTitle="${contentTitle%%\"*}"
	next_type=related
	[ "${feedUrl#*/category/}" != "${feedUrl}" ] && next_type=category
	echo "<tr><td><center><font size='+3'><b><a id=\"link$item_nr\" href=\"ipla.cgi?type=${next_type}&url=http://$feedUrl\" target=\"_parent\">$feedTitle</a></b></font></center><br/></td></tr>" | sed 's/\#\#/ /g'
	item_nr=$(($item_nr+1))
    done
else
    echo '<font size="+1">'
    echo '<Table id="items" name="items" class="items" Border=0 cellspacing=0 width="100%">'
    echo '<tr>'
    item_nr=1
    if [ "$type" = "category" ]
    then
	for content in `egrep -i '\"thumb\"|\"url\"|\"title\"|\{|\}' $log_file | tr '\n' ' ' | tr '{}' '\n' | grep -i "/category/" | sed -e 's/  */ /g' -e 's/ "/"/g' -e 's/ /\#\#/g' -e 's#http://##g'`
	do
	    contentThumb="${content#*\"thumb\":\"}"
	    [ "$contentThumb" != "$content" ] && feedThumb="${contentThumb%%\",*}"
	    contentTitle="${content#*\"title\":\"}"
	    [ "$contentTitle" != "$content" ] && feedTitle="${contentTitle%%\",*}"
	    contentUrl="${content#*\"url\":\"}"
	    [ "$contentUrl" != "$content" ] && feedUrl="${contentUrl%%\",*}"
	    echo "<td width='110px'><a id=\"link$item_nr\" href=\"ipla.cgi?type=category2&url=http://$feedUrl\" target=\"_parent\"><img src=\"http://$feedThumb\"/></td><td width='33%'><b>$feedTitle</b></a></td>" | sed -e 's/\#\#/ /g' -e 's/u0\(...\)/\&\#x0\1\;/g' -e 's/\\//g'
	    [ "$(($item_nr % 3))" = "0" ] && echo "</tr><tr>"
	    item_nr=$(($item_nr+1))
	done
    else
	    for content in `egrep -i '\"date\"|\"video|\"thumb|\"url\"|\"title\"|\{|\}' $log_file | sed -e 's/: {//g' -e 's/},//g' | tr '\n' ' ' | tr '{}' '\n' | egrep -i "/movies/|/category/" | sed -e 's/  */ /g' -e 's/\" /\"/g' -e 's/ \"/\"/g' -e 's/ /\#\#/g' -e 's#http://#http//#g'`
	    do
		echo "$content" >> /tmp/content.log
		contentDate="${content#*\"date\":\"}"
		feedDate=""
		[ "$contentDate" != "$content" ] && feedDate="${contentDate%%\"*}"
		contentThumb="${content#*\"thumbnail_304x166\":\"}"
		feedThumb=""
		[ "$contentThumb" != "$content" ] && feedThumb="${contentThumb%%\"*}"
		if [ "$feedThumb" = "" ]
		then
		    contentThumb="${content#*\"thumb\":\"}"
		    feedThumb=""
		    [ "$contentThumb" != "$content" ] && feedThumb="${contentThumb%%\"*}"
		fi
		contentTitle="${content#*\"title\":\"}"
		feedTitle=""
		[ "$contentTitle" != "$content" ] && feedTitle="${contentTitle%%\"*}"
		contentVideo="${content#*\"video_hd\":\"}"
		feedVideo=""
		[ "$contentVideo" != "$content" ] && feedVideo="${contentVideo%%\"*}"
		if [ "$feedVideo" = "" ]
		then
		    contentVideo="${content#*\"video\":\"}"
		    feedVideo=""
		    [ "$contentVideo" != "$content" ] && feedVideo="${contentVideo%%\"*}"
		    hd=0
		else
		    hd=1
		fi
		contentUrl="${content#*\"url\":\"}"
		feedUrl=""
		[ "$contentUrl" != "$content" ] && feedUrl="${contentUrl%%\"*}"
		if [ "$feedVideo" != "" ]
		then
		    hd_str=""
		    [ "$hd" = "1" ] && hd_str=" HD!"
		    echo "<td width='33%'><center><a id=\"link$item_nr\" href=\"$feedVideo\" target=\"_parent\"><img src=\"$feedThumb\"/><br/><b>${feedDate}${hd_str}<br/>$feedTitle</b></a></center></td>" | sed -e 's#http//#http://#g' -e 's/\#\#/ /g' -e 's/u0\(...\)/\&\#x0\1\;/g' -e 's/u2\(...\)/\&\#x2\1\;/g' -e 's/\\//g'
		else
		    echo "<td width='33%'><center><a id=\"link$item_nr\" href=\"ipla.cgi?type=category2&url=$feedUrl\" target=\"_parent\"><img src=\"$feedThumb\"/><br/><b>$feedDate<br/>$feedTitle</b></a></center></td>" | sed -e 's#http//#http://#g' -e 's/\#\#/ /g' -e 's/u0\(...\)/\&\#x0\1\;/g' -e 's/u2\(...\)/\&\#x2\1\;/g' -e 's/\\//g'
		fi
		[ "$(($item_nr % 3))" = "0" ] && echo "</tr><tr>"
		item_nr=$(($item_nr+1))
	    done
    fi
    echo '</tr>'
    echo '</table>'
fi

?>
</font></center>
</BODY></HTML>

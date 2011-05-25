#!/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- ipla.cgi by xeros -->
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
<title>Ipla.tv alternative by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

document.onkeydown = check;
window.onload = OnLoadSetCurrent;
     
function check(e)
	{
	if (!e) var e = window.event;
	(e.keyCode) ? key = e.keyCode : key = e.which;
	try
		{

		if (key==404) 
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

	function OnLoadSetCurrent(element)
	{
	//top.frames["Keyboard"].focus();
	document.links['link1'].focus();
	}
	
document.defaultAction = true;


// -->
</script>


</HEAD>
<!-- BODY background="background.png" -->
<BODY bgcolor="green">

<?

useragent="tv_samsung/4"
menuLoc="http://getmedia.redefine.pl/tv/menu.json?login=common_user&passwdmd5="

#deviceid="`cat /mnt/user/ywe/deviceid`"

if [ "$FORM_url" != "" ]
then
    url="$FORM_url"
    type="$FORM_type"
    log_file=/tmp/$type.log
else
    url="$menuLoc"
    type=menu
    log_file=/tmp/$type.log
fi

#url="$menuLoc"
?>


<?

#log_file=$RANDOM

wget -q -U "$useragent" -O - "$url" > $log_file

#echo "$url $log_file <br/>"

if [ "$type" = "menu" ]
then
    echo '<img src="http://www.ipla.tv/images/logo.png"/><font size="+3"> alternative</font><br/>by xeros<br/><br/>'
    echo '<font size="+3">'
    #for content in `cat $log_file | grep "\"feed" | tr '\n' ' ' | sed -e 's/\(\"feedUrl\"\)/\n\1/g' -e 's/ *//g' -e '/^$/d' -e 's/\"feedUrl\"://g' -e 's/,\"feedTitle\":/;/g' | grep "/category/"`
    for content in `cat $log_file | grep "\"feed" | tr '\n' ' ' | sed -e 's/\(\"feedUrl\"\)/\n\1/g' -e 's/ */ /g' -e 's/ "/"/g' -e 's/\"feedUrl\"://g' -e 's/,\"feedTitle\":/;/g' | grep "/category/"`
    do
	feedUrl=`echo $content | awk -F\; '{print $1}' | tr -d '\"'`
	feedTitle=`echo $content | awk -F\; '{print $2}' | tr -d '\"' | sed -e 's/\\\u\(....\)/\&#x\1;/g'`
	echo "<a href=\"ipla.cgi?type=category&url=$feedUrl\">$feedTitle</a><br/>"
    done
else
    echo '<font size="+1">'
    echo '<Table id="items" name="items" class="items" Border=0 cellspacing=0 width="100%">'
    echo '<tr>'
    item_nr=1
    if [ "$type" = "category" ]
    then
	#for content in `cat $log_file | egrep '\"thumb\"|\"url\"|\"title\"|{|}' | tr '\n' ' ' | tr '{}' '\n' | sed -e 's/ *//g' -e '/^$/d' -e 's/\"url\"://g' -e 's/,\"thumb\":/;/g' -e 's/,\"title\":/;/g' | grep "/category/"`
	for content in `cat $log_file | egrep '\"thumb\"|\"url\"|\"title\"|\{|\}' | tr '\n' ' ' | tr '{}' '\n' | sed -e 's/ */ /g' -e 's/ "/"/g' -e 's/\"url\"://g' -e 's/,\"thumb\":/;/g' -e 's/,\"title\":/;/g' -e 's/ /\#\#/g' | grep "/category/"`
	do
	    feedUrl=`echo $content | awk -F\; '{print $1}' | tr -d '\"'`
	    feedThumb=`echo $content | awk -F\; '{print $2}' | tr -d '\"'`
	    # v- better works on PC
	    #feedTitle=`echo $content | awk -F\; '{print $3}' | tr -d '\"' | sed -e 's/\\\u\(....\)/\&#x\1;/g'`
	    # v- better work in TV
	    #feedTitle=`echo $content | awk -F\; '{print $3}' | tr -d '\"' | sed 's/\\u\(....\)/\&\#x\1\;/g'`
	    # v- not proper regex code but looks like backslash (in "\uXXXX") is being lost somewhere with BusyBox tools
	    feedTitle=`echo $content | awk -F\; '{print $3}' | tr -d '\"' | sed -e 's/\#\#/ /g' -e 's/u0\(...\)/\&\#x0\1\;/g'`
	    echo "<td>"
	    echo "<a href=\"ipla.cgi?type=category2&url=$feedUrl\" target=\"_parent\"><img src=\"$feedThumb\"/></td><td>$feedTitle</a><br/>"
	    echo "</td>"
	    if [ "$(($item_nr % 3))" = "0" ]
	    then
		echo "</tr><tr>"
	    fi
	    item_nr=$(($item_nr+1))
	done
    else
	if [ "$type" = "category2" ]
	then
	    #for content in `cat $log_file | egrep '\"date\"|\"video\"|\"thumb\"|\"url\"|\"title\"|{|}' | tr '\n' ' ' | tr '{}' '\n' | sed -e 's/ *//g' -e '/^$/d' -e 's/\"date\"://g' -e 's/,\"thumb\":/;/g' -e 's/,\"title\":/;/g' -e 's/,\"video\":/;/g' | grep "/movies/"`
	    for content in `cat $log_file | egrep '\"date\"|\"video\"|\"thumb\"|\"url\"|\"title\"|\{|\}' | tr '\n' ' ' | tr '{}' '\n' | sed -e 's/ */ /g' -e 's/ "/"/g' -e 's/\"date\"://g' -e 's/,\"thumb\":/;/g' -e 's/,\"title\":/;/g' -e 's/,\"video\":/;/g' -e 's/ /\#\#/g' | grep "/movies/"`
	    do
		feedDate=`echo $content | awk -F\; '{print $1}' | tr -d '\"'`
		feedThumb=`echo $content | awk -F\; '{print $2}' | tr -d '\"'`
		feedTitle=`echo $content | awk -F\; '{print $3}' | tr -d '\"' | sed -e 's/\#\#/ /g' -e 's/u0\(...\)/\&\#x0\1\;/g'`
		feedVideo=`echo $content | awk -F\; '{print $4}' | tr -d '\"'`
		echo "<td>"
		echo "<a href=\"$feedVideo\" target=\"_parent\"><img src=\"$feedThumb\"/><br/>$feedDate<br/>$feedTitle</a><br/>"
		echo "</td>"
		if [ "$(($item_nr % 3))" = "0" ]
		then
		    echo "</tr><tr>"
		fi
		item_nr=$(($item_nr+1))
	    done
	fi
    fi
    echo '</tr>'
    echo '</table>'
    #echo "item_nr: $item_nr"
fi

?>
</font>
</BODY></HTML>

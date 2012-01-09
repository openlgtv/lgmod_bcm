#!/usr/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- tvn.cgi by xeros -->
<!-- Source code released under GPL License -->

<style type="text/css">
    body {
	font-family:"TiresiasScreenfont";
	font-color:white
    }
    a:link {
	color:white;
	text-decoration:bold;
    }
</style>
<title>TVNplayer alternative by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

<?

#useragent="Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"
useragent="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"

menuLoc="http://tvnplayer.pl"

if [ "$FORM_url" != "" ]
then
    url="$FORM_url"
    type="$FORM_type"
    log_file=/var/log/vod/tvn/$type.log
    echo "var col = 3; //number of 'cells' in a row"
else
    url="$menuLoc"
    type=menu
    log_file=/var/log/vod/tvn/$type.log
    echo "var col = 1; //number of 'cells' in a row"
fi

if [ ! -d "/var/log/vod/tvn" ]
then
    mkdir -p /var/log/vod/tvn
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
	//top.frames["Keyboard"].focus();
	document.links['link1'].focus();
	}
	
document.defaultAction = true;


// -->
</script>



<?

if [ "$type" != "playlist" ]
then
    echo "</HEAD>"
    echo "<BODY bgcolor="black">"
    echo '<center><img src="http://tvnplayer.pl/img/logo_menu.png"/><font color="white"><font size="+1"><br/>alternative</font><br/>by xeros</font><br/><br/>'
    #echo '<font size="+3">'
    echo '<Table id="items" name="items" class="items" Border=0 cellspacing=0 width="100%">'
fi

if [ "$type" = "menu" ]
then
    echo "<tr><td><center><font size='+3'><b><a id=\"link1\" href=\"tvn.cgi?type=category&url=$url/seriale.html\" target=\"_parent\">Seriale</a></b></font></center><br/></td></tr>"
    echo "<tr><td><center><font size='+3'><b><a id=\"link2\" href=\"tvn.cgi?type=category&url=$url/programy.html\" target=\"_parent\">Programy</a></b></font></center><br/></td></tr>"
    echo "<tr><td><center><font size='+3'><b><a id=\"link3\" href=\"tvn.cgi?type=category&url=$url/filmy.html\" target=\"_parent\">Filmy</a></b></font></center><br/></td></tr>"
    echo "<tr><td><center><font size='+3'><b><a id=\"link4\" href=\"tvn.cgi?type=category&url=$url/dla-dzieci.html\" target=\"_parent\">Dla dzieci</a></b></font></center><br/></td></tr>"
    echo "<tr><td><center><font size='+3'><b><a id=\"link5\" href=\"tvn.cgi?type=category&url=$url/ostatni-dzwonek.html\" target=\"_parent\">Ostatni dzwonek</a></b></font></center><br/></td></tr>"
    echo "</table></body></html>"
    exit 0
fi

if [ "$type" = "category" -o "$type" = "category2" ]
then
    new_type=category2
    [ "$type" = "category2" ] && new_type=playlist
    #wget -q -U "$useragent" -O - "$url" > $log_file
    wget -q -U "$useragent" "$url" -O $log_file
    item_nr=1
    #IFS=$(/bin/echo -e '\n')
    IFS=QQQXXQQQ
    echo "<tr>"
    for content in `grep -A3 '<div class="photoContainer">' $log_file | grep -v "^--$" | tr -d '\n' | sed -e 's#<div class="photoContainer">#\n#g' | sed -e s'#alt="tvn .layer -\(.*\)".*#alt="\1" /><br/>\1</td></a>QQQXXQQQ#g' -e 's/^\t*//g' -e 's/^ */<td><center>/g' | grep -v "^<td><center>$"`
    do
	if [ "$content" != "" ]
	then
	    echo "$content" | sed -e "s#<a href=\"/#<a id=\"link$item_nr\" href=\"tvn.cgi\?type=$new_type\&url=http://tvnplayer.pl/#g" -e 's/QQQXXQQQ//g'
	    if [ "$(($item_nr % 3))" = "0" ]
	    then
		echo "</tr><tr>"
	    fi
	    item_nr=$(($item_nr+1))
	fi
    done
    echo "</tr></table></body></html>"
    exit 0
fi

if [ "$type" = "playlist" -o "$type" = "video" ]
then
    new_type=video
    wget -q -U "$useragent" "$url" -O $log_file
    if [ "$type" = "playlist"
    then
	echo "`grep -i playlist $log_file | sed -e 's#.*playlist=#<meta HTTP-EQUIV=\"REFRESH\" content=\"1; url=tvp.cgi\?type=video\&url=http://tvnplayer.pl#g' -e 's/\.xml.*/\.xml\">/g'`"
    fi
fi

exit 0

?>
</font></center>
</BODY></HTML>

#!/usr/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- tvn.cgi by xeros -->
<!-- Source code released under GPL License -->

<!-- NOT FINISHED -->

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

useragent="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"

menuLoc="http://tvnplayer.pl"
# TODO: start from: "http://tvnplayer.pl/api/?platform=Mobile&terminal=Android&format=xml&type=recommended&id=0&limit=50&page=1&sort=newest&m=getItems"


if [ -n "$FORM_url" ]
then
    export url="$FORM_url"
    export type="$FORM_type"
    export log_file=/var/log/vod/tvn/$type.log
    echo "var col = 3; //number of 'cells' in a row"
else
    export url="$menuLoc"
    export type=menu
    export log_file=/var/log/vod/tvn/$type.log
    echo "var col = 1; //number of 'cells' in a row"
fi

[ ! -d "/var/log/vod/tvn" ] && mkdir -p /var/log/vod/tvn

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
		if (key==37|key==38|key==39|key==40)
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
	if (document.links['link1']) document.links['link1'].focus();
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
    echo '<Table id="items" name="items" class="items" Border=0 cellspacing=0 width="100%">'
fi

if [ "$type" = "menu" ]
then
    echo "<tr><td><center><font size='+3'><b><a id=\"link1\" href=\"tvn.cgi?type=category&url=$url/seriale-online/\" target=\"_parent\">Seriale</a></b></font></center><br/></td></tr>"
    echo "<tr><td><center><font size='+3'><b><a id=\"link2\" href=\"tvn.cgi?type=category&url=$url/programy-online/\" target=\"_parent\">Programy</a></b></font></center><br/></td></tr>"
    echo "<tr><td><center><font size='+3'><b><a id=\"link3\" href=\"tvn.cgi?type=category&url=$url/filmy-online/\" target=\"_parent\">Filmy</a></b></font></center><br/></td></tr>"
    echo "<tr><td><center><font size='+3'><b><a id=\"link4\" href=\"tvn.cgi?type=category&url=$url/dla-dzieci-online/\" target=\"_parent\">Dla dzieci</a></b></font></center><br/></td></tr>"
    echo "<tr><td><center><font size='+3'><b><a id=\"link5\" href=\"tvn.cgi?type=category&url=$url/ostatni-dzwonek/\" target=\"_parent\">Ostatni dzwonek</a></b></font></center><br/></td></tr>"
    echo "</table></body></html>"
    exit 0
fi

if [ "$type" = "category" -o "$type" = "category2" ]
then
    new_type=category2
    [ "$type" = "category2" ] && new_type=playlist
    wget -q -U "$useragent" "$url" -O "$log_file"
    item_nr=1
    #IFS=$(/bin/echo -e '\n')
    IFS=QQQXXQQQ
    echo "<tr>"
    for content in `grep -A3 '<div class="photoContainer">' $log_file | grep -v "^--$" | tr -d '\n' | sed -e 's#<div class="photoContainer">#\n#g' | sed -e s'#alt="tvn .layer - \(.*\)".*#alt="\1" /><br/>\1</td></a>QQQXXQQQ#g' -e 's/^\t*//g' -e 's/^ */<td><center>/g' | grep -v "^<td><center>$"`
    do
	if [ "$content" != "" ]
	then
	    echo "$content" | sed -e "s#<a href=\"/#<a id=\"link$item_nr\" href=\"tvn.cgi\?type=$new_type\&url=http://tvnplayer.pl/#g" -e 's/QQQXXQQQ//g'
	    [ "$(($item_nr % 3))" = "0" ] && echo "</tr><tr>"
	    item_nr=$(($item_nr+1))
	fi
    done
    echo "</tr></table></body></html>"
    exit 0
fi

if [ "$type" = "playlist" -o "$type" = "video" ]
then
    new_type=video
    wget -q -U "$useragent" "$url" -O "$log_file"
    if [ "$type" = "playlist" ]
    then
	echo "`grep -i playlist $log_file | sed -e 's#.*playlist=#<meta HTTP-EQUIV=\"REFRESH\" content=\"1; url=tvn.cgi\?type=video\&url=http://tvnplayer.pl#g' -e 's/\.xml.*/\.xml\">/g'`"
    else
	#grep http "$log_file" | sed -e 's/\(<movie>\)/\n\1/g' -e 's/.*<title><!\[CDATA\[//g' -e 's#\]\]></title><episode_name><!\[CDATA\[#|#g' -e 's#\]\]></episode_name><episode>#|#g' -e 's#</episode><season>#|#g' -e 's#</season>.*<splash_screen><url><!\[CDATA\[#|#g' -e 's#\]\]></url>.*<url><!\[CDATA\[#|#g' -e 's/\]\].*//g'
	grep http "$log_file" | sed -e 's#.*<url><!\[CDATA\[#<meta HTTP-EQUIV="REFRESH" content="1; url=#g' -e 's/\]\].*/">/g'
	# TODO: generate urls and join chunks for continous stream
	# http://dcs-34-55-222-43.atmcdn.pl/ss/o2/tvnplayer/vod/12_300_12350_0004/SMOOTH_HD/5d25b78e-e355-3b65-4389-5f375429335d/Manifest.ism/manifest
	# -v-
	# http://dcs-34-55-222-43.atmcdn.pl/ss/o2/tvnplayer/vod/12_300_12350_0004/Manifest.ism/QualityLevels(128000)/Fragments(audio=0)
	# http://dcs-34-55-222-43.atmcdn.pl/ss/o2/tvnplayer/vod/12_300_12350_0004/Manifest.ism/QualityLevels(128000)/Fragments(video=1200000)
	# and continue updating audio and video values
	# QualityLevels and Fragments values are in manifest file

    fi
fi

exit 0

?>
</font></center>
</BODY></HTML>

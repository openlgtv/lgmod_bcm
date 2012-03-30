#!/usr/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<head>

<!-- m3u.cgi by xeros -->
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
<title>M3U parser by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

var col = 1; //number of 'cells' in a row
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
	if (document.links['link1']) document.links['link1'].focus();
	}

document.defaultAction = true;


// -->
</script>
</head>
<body>

<center><font size="+3">M3U playlist parser</font><br/>by xeros<br/></center><br/>
<font size="+2">
<center>

<?
useragent="Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"

[ -z "$FORM_url" ] && exit 1

echo "Playlist loaded from: $FORM_url<br/>"

menuLoc="$FORM_url"
listDir="${menuLoc%/*}"
log_file=/var/log/vod/m3u.log.m3u
[ ! -d "/var/log/vod" ] && mkdir -p /var/log/vod

rm -f $log_file $log_file.html > /dev/null 2>&1

if [ "${menuLoc:0:1}" = "/" ]
then
    [ -f "$menuLoc" ] && cat "$menuLoc"
else
    #[ "${menuLoc#*://}" = "$menuLoc" ] # test for :// URL - would it be useful?
    wget -q -U "$useragent" "$menuLoc" -O -
fi | sed -e 's/\r//g' -e 's/.*EXTM3U.*//g' | grep -v "^$" > $log_file

cp -f $log_file $log_file.html

item_nr=1

#for ulink in `grep "://" $log_file`
SIFS="$IFS"
IFS=$'\n'
for ulink in `grep -v "#EXTINF:" $log_file`
do
    ulink2="$ulink"
    [ "${ulink:0:1}" != "/" -a "${ulink#*://}" = "$ulink" ] && ulink2="$listDir/$ulink"
    sed -i -e "s#^\($ulink\)#<a id=\"link$item_nr\" href=\"$ulink2\">\1</a><br/>#g" $log_file.html
    item_nr=$(($item_nr+1))
done
IFS="$SIFS"

cat $log_file.html | sed -e 's/#EXTINF://g' -e 's#\(href=\"\)/#\1/root/#g'
?>

</center></font>
</body>
</HTML>

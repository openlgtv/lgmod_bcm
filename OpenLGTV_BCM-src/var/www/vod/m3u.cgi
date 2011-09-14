#!/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

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
<!-- meta HTTP-EQUIV='REFRESH' content="30; url=m3u.cgi" -->
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
</head>
<body>

<!-- center><img src="http://...png"/><font size="+3"><br/>parser</font><br/>by xeros<br/></center><br/><br/ -->
<center><font size="+3">M3U playlist parser</font><br/>by xeros<br/></center><br/>
<font size="+2">
<center>

<?
useragent="Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"

[ -z "$FORM_url" ] && exit 1

echo "Playlist loaded from: $FORM_url<br/>"

menuLoc="$FORM_url"
log_file=/tmp/log/vod/m3u.log.m3u
if [ ! -d "/tmp/log/vod" ]
then
    mkdir -p /tmp/log/vod
fi

rm -f $log_file $log_file.html > /dev/null 2>&1

wget -q -U "$useragent" "$menuLoc" -O - | sed -e 's/\r//g' -e 's/.*EXTM3U.*//g' -e 's/#EXTINF:/<br>/g' | grep -v "^$" > $log_file
cp -f $log_file $log_file.html

item_nr=1

for ulink in `cat $log_file | grep "://"`
do
    sed -i -e "s#^\($ulink\)#<a id=\"link$item_nr\" href=\"\1\">\1</a>#g" $log_file.html
    item_nr=$(($item_nr+1))
done

cat $log_file.html

#wget -q -U "$useragent" "$menuLoc" -O - | \
#    sed -e 's/\r//g' -e 's/.*EXTM3U.*//g' -e 's/#EXTINF:/<br>/g' -e 's#\(.*://.*\)#<a href="\1">\1</a>#g' | \
#    grep -v "^$"
?>

</center></font>
</body>
</HTML>

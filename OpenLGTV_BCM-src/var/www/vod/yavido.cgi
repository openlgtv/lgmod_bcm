#!/usr/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- yavido.cgi by xeros -->
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
<title>YAVIDO alternative by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta HTTP-EQUIV='REFRESH' content="15">
<script type="text/javascript">
<!--

var col = 1; //number of 'cells' in a row
var current = 1;
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
	if (document.links['link1']) document.links['link1'].focus();
	}
	
document.defaultAction = true;

// -->
</script>
</head>
<body>

<center><img src="http://www.yavido.tv/sites/default/files/yaml_2col_31_logo.png"/><font size="+3"><br/>alternative</font><br/>by xeros<br/></center><br/><br/>
<font size="+3">
<center>

<?
log_dir=/var/log/vod/yavido
list_file="$log_dir/list.html"
mkdir -p "$log_dir"

useragent="Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
menuLoc="http://lge.yavido.tv/ajax/portal/getPlaylist.php?action=home"

wget -q -U "$useragent" "$menuLoc" -O - | \
    sed -e 's/\(\.mp4"\)/\1<\/a>\n/g' | \
    sed -e 's/"AUTHOR":"\(.*\)","TITLE":"\(.*\)","URL":"\(.*mp4\)"/\n<a href="\3">\1 - \2<\/a><br><br>\n/g' -e 's/\\//g' | \
    grep "^<a" | grep -n "href" | sed 's/^\(.*\):<a/<a id="link\1"/g' | tee "$list_file"

[ "$FORM_autoplay" = "1" ] && head -n1 "$list_file" | sed -e 's/.*href="/<script type="text\/javascript">window.location="/g' -e 's/\.mp4.*/.mp4";<\/script>/g'
?>

<br><font size="+4"><a id="link5" href="yavido.cgi?autoplay=1">Play Continuosly</a></font>
</center></font>
</body>
</HTML>

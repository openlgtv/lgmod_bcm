#!/bin/haserl
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
<meta HTTP-EQUIV='REFRESH' content="30; url="yavido.cgi">
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

<center><img src="http://www.yavido.tv/sites/default/files/yaml_2col_31_logo.png"/><font size="+3"><br/>alternative</font><br/>by xeros<br/></center><br/><br/>
<font size="+2">
<center>

<?
useragent="Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"

menuLoc="http://lge.yavido.tv/ajax/portal/getPlaylist.php?action=home"


wget -q -U "$useragent" "$menuLoc" -O - | \
    sed -e 's/\(\.mp4"\)/\1<\/a>\n/g' | \
    sed -e 's/"AUTHOR":"\(.*\)","TITLE":"\(.*\)","URL":"\(.*mp4\)"/\n<a href="\3">\1 - \2<\/a><br>\n/g' -e 's/\\//g' | \
    grep "^<a"
?>

</center></font>
</body>
</HTML>

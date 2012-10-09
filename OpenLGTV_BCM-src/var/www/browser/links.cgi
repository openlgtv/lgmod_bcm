#!/usr/bin/haserl
content-type: text/html

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>

<!-- Code for OpenLGTV BCM Browser by Nicola Ottomano -->
<!-- Modified by xeros -->
<!-- Source code released under GPL License -->

<title>NetCast web-based services links</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

<script type="text/javascript">
<!--

// TODO: separate links by countries into CSV files
//       and replace this HTML with CGI script that would sort icons
//       based on country/language chosen in TV menu as first ones, then the rest of icons
//       and add missing icons

<?
    export col=6
    //export row=6
    export row=8
    export max_pages=6 # 6*8*6=288

    echo "var col = $col; //number of 'cells' in a row"
    echo "var row = $row; //number of rows to jump with channel up/down"
    if [ "$GET_page" != "" ]
    then
	page_prev="$(($GET_page-1))"
	page_next="$(($GET_page+1))"
	[ "$GET_page" = "1" ] && page_prev=1
	[ "$GET_page" = "$max_pages" ] && page_next="$max_pages"
    fi
?>
var current;
var next;
document.onkeydown = check;
//window.onload = OnLoadSetCurrent;

function check(e)
	{
	if (!e) var e = window.event;
	(e.keyCode) ? key = e.keyCode : key = e.which;
	try
		{
			switch(key)
			{
<?
    if [ "$GET_page" != "" ]
    then
	echo "			case 33: window.location.replace('links.cgi?page=$page_prev'); break; //ch up"
	echo "			case 34: window.location.replace('links.cgi?page=$page_next'); break; //ch down"
    else
        echo "			case 33: next = (1*current) - (row*col); break; //ch up"
	echo "			case 34: next = (1*current) + (row*col); break; //ch down"
    fi
?>
			case 37: next = current - 1; break; //left
			case 38: next = current - col; break; //up
			case 39: next = (1*current) + 1; break; //right
			case 40: next = (1*current) + col; break; //down
			}
		if (key==33|key==34|key==37|key==38|key==39|key==40)
			{
			//Move to the next key on the keyboard
			//Check if new link exists, if not then go to previous one until finds the one that exists
			if (next<=0)
			{
			    do {
				next = next + col;
			    } while (next<=0);
			}
			currentLink=document.links['c' + next];
			if (!currentLink)
			{
			    do {
				next = next - col;
				currentLink=document.links['c' + next];
			    } while ((!currentLink)&&(next >= 1));
			}
			var code=currentLink.name;
			currentLink.focus();
			current = next;
			//Prevent scrolling
			return false;
			}
		else if (key==461) 
			{
			//the back button on the remote control have been pressed
			//NetCastBack API
			//window.NetCastBack();
			history.go(-1);
			//window.location='../browser.cgi';
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
	current = string.slice(1,string.length);
	}

function OnLoadSetCurrent()
	{
	current = 1;
	document.links['c1'].focus();
	}

document.defaultAction = true;

// -->
</script>

<style type="text/css">
    a:link,
    a:visited {
	background-color: #000000;
	color: #000000;
    }
    a:hover,
    a:focus,
    a:active {
	color: #FFFF00;
	background-color: #000000;
    }
    font {
	color: white;
    }
</style>

</head>

<body bgcolor="#000000">
<center>
<table border=0>
<tr>
<?
    id=1
    head=1000
    tail=1000
    [ "$GET_page" != "" ] && export head="$(($col*$row*$GET_page))" && export tail="$(($col*$row))"
    SIFS="$IFS" IFS=$'\n'
    for item in `grep -v "^#" /var/www/browser/links.csv | head -n "$head" | tail -n "$tail"`
    do
	it_lang="${item%%|*}" item="${item#*|}"
	it_name="${item%%|*}" item="${item#*|}"
	it_url="${item%%|*}"  item="${item#*|}"
	it_icon="${item%%|*}" item="${item#*|}"
	it_overlay="${item%%|*}"
	[ "$it_overlay" != "" ] && it_icon="$it_overlay\" style=\"background:url($it_icon)"
	#echo "$it_lang $it_name $it_url $it_icon $it_overlay"
	echo "<td align=\"center\"><a id=\"c$id\" onKeyPress=\"javascript:setCurrent(this);return false\" href=\"$it_url\" target=\"_parent\"><img src=\"$it_icon\" alt=\"$it_name\" border=2></a></td>"
	[ "$id" = "1" ] && echo "<script type=\"text/javascript\">OnLoadSetCurrent();</script>"
	[ "$(($id % $col))" = "0" ] && echo "</tr><tr>"
	id="$(($id+1))"
    done
    IFS="$SIFS"
    echo "</tr>"
?>
</table>
</center>
</body>
</html>

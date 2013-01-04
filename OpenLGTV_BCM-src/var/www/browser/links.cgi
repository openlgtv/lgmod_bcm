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
//       - add keypad

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
var dialog_displayed = 0;
var dialog_win;
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
	echo "			case 33: window.location.replace('links.cgi?page=$page_prev'); return false; break; //ch up"
	echo "			case 34: window.location.replace('links.cgi?page=$page_next'); return false; break; //ch down"
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
		else if (key==406|key==118)
			{
			//the BLUE button on the remote control or F7 have been pressed
			//Open directory creation dialog
			if (dialog_displayed==0)
			    gotoDialog();
			else
			    removeDialog();
			e.preventDefault();
			return false;
			}
		else if (key==461|key==27) 
			{
			//the BACK button on the remote control or ESC have been pressed
			if (dialog_displayed==0)
			    {
			    //NetCastBack API
			    //window.NetCastBack();
			    //lets get back to previous page instead of closing NetCast service
			    history.go(-1);
			    //window.location='../browser.cgi';
			    }
			else
			    dialogRemove();
			//Prevent default action
			e.preventDefault();
			return false;
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

function gotoDialog()
	{
	var newdiv = document.createElement("div");
	var newdivWidth=716;
	var newdivHeight=176;
	var newdivLeft=(window.innerWidth/2)-(newdivWidth/2)-10;
	var newdivTop=(window.innerHeight/2)-(newdivHeight/2)-5;
	newdiv.setAttribute('style', 'background: #efef00; position:absolute; padding:20px 10px 0 10px; top:' + newdivTop + 'px; left:' + newdivLeft + 'px; width:' + newdivWidth + 'px; height:' + newdivHeight + 'px; border:2px solid black;');
	newdiv.id = "dialogWin";
	document.body.appendChild(newdiv);
	var kb = '<FONT color="black" style="color:black;" size="+3"> \
	    <center><b>Type URL to go to:</b></center><br/> \
	    <!-- form id="text" name="text" action="fm.cgi" method="GET" --> \
	    <input id="txtName" name="txtName" type="textarea" style="width:710px"> \
	    <!-- input type="hidden" name="page" value="' + row + '" --> \
	    <table width="100%"><tr valign="middle"><td align="right" valign="middle"><span onClick="javascript:window.location=document.getElementById(\'txtName\').value;"><img src="/Images/Keyboard/ok_button.png" border="0" /><font size="+3" style="color:black;"> OK</font></span></td><td align="center" valign="middle"><span onClick="javascript:dialogRemove();"><img src="/Images/Keyboard/back_button.png" border="0" /><font size="+3" style="color:black;"> Cancel</font></span></td></tr></table><!-- /form --></font>';
	newdiv.innerHTML = kb;
	document.getElementById('txtName').focus();
	dialog_displayed = 1;
	}

function dialogRemove()
	{
        document.body.removeChild(document.getElementById("dialogWin"));
	dialog_displayed = 0;
	dialog_win = '';
	OnLoadSetCurrent();
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
    links_file=/var/www/browser/links.csv
    [ -f "/mnt/user/etc/lang" ] && lang="`cat /mnt/user/etc/lang`" || lang=NONE
    [ "$GET_page" != "" ] && export head="$(($col*$row*$GET_page))" && export tail="$(($col*$row))"
    SIFS="$IFS" IFS=$'\n'
    for item in `( grep "^[^#|]*$lang[^|]*|" "$links_file"; grep "^[^#|]*ALL[^|]*|" "$links_file"; egrep -v "^#|^[^\|]*$|^[^#\|]*$lang[^\|]*\||^[^#\|]*ALL[^\|]*\|" "$links_file" ) | head -n "$head" | tail -n "$tail"`
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

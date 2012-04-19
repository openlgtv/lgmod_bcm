#!/usr/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- OpenLGTV BCM FileManager by xeros -->
<!-- fm.cgi script for directory tree navigation and invoking operations on fm-action.cgi -->
<!-- Source code released under GPL License -->

<!-- tested on builtin GTK Browser, Firefox 5-10, Chromium 14 and reKonq 0.7.90 (problems with F5 on reKonq) -->

<? killall df stat 2>/dev/null & ?>

<style type="text/css">
    body {
	font-family:monospace;
	//height: 710px;
	//font-family:"TiresiasScreenfont";
	overflow-x: hidden;
	overflow-y: hidden;
    }
    a:link, a:visited, a:active {
	color:black;
	text-decoration:none;
    }
    a:hover {
	text-decoration:underline;
    }
    table.fulltable, #fulltable {
	height:690px;
    }
    tbody.main, #main {
	width: 95%;
	height: 95%;
	overflow-y:auto;
	overflow-x: hidden;
	min-height:690px;
    }
    tbody.scrollable, #scrollable {
	display: block;
	height: 100%;
	overflow-y: auto;
	overflow-x: hidden;
    }
    td.lpanelpath, .rpanelpath, #lpanelpath, #rpanelpath {
	overflow:hidden;
	white-space:nowrap;
	width:43%;
	min-width:300px;
    }
    td.filename, #filename {
	width: 700px;
	width: 100%;
	overflow:hidden;
	white-space:nowrap;
    }
    td.size, #size {
	min-width: 70px;
    }
    td.date, #date {
	overflow:hidden;
	white-space:nowrap;
    }
    td {
	//border: 1px black solid;
    }
    input.uploadhide {
	position:absolute;
	left:-1000px;
	top: -1000px;
    }
    input.upload {
	background-color:#cc0000;
	font-weight:bold;
	color:#ffffff;
	width:37px;
	height:15px;
	font-size:7.5px;
    }
</style>

<title>CGI FileManager by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

//TODO: if filenameSize < 440 (from 1280/2-200) then cut filename characters earlier
//var filenameSize=(window.innerWidth/2)-255;
//var filenameSize=(window.innerWidth/2)-200;
// static value bigger than the needed one is even better - cell width is being resized without need to refresh page
document.write('<style type="text/css">td.filename {width:800px;}</style>');

<?

log_dir=/var/log/fm

[ ! -d "$log_dir" ] && mkdir -p "$log_dir" 2>/dev/null &
[ -f "$log_dir/last_played.info" ] && rm -f "$log_dir/last_played.info" 2>/dev/null &
paths_file="$log_dir/last_paths.log"

if [ "$FORM_type" = "restore_last" ]
then
    [ -f "$paths_file" ] && source "$paths_file"
else
    echo -e "FORM_side='${FORM_side}'\nFORM_lpth='${FORM_lpth}'\nFORM_rpth='${FORM_rpth}'\nFORM_select='${FORM_select}'\nFORM_lselected='${FORM_lselected}'\nFORM_rselected='${FORM_rselected}'\n" > "$paths_file" &
fi

[ "$FORM_side" != "" ] && export side="$FORM_side" || export side="l"
[ "$FORM_lpth" != "" ] && export lpth="$FORM_lpth"
[ "$FORM_rpth" != "" ] && export rpth="$FORM_rpth"

if [ "$side" = "l" -a "$lpth" != "" ]
then
    cpth="$lpth"
    opth="$rpth"
    selected="$FORM_lselected"
    oside=r
else
    if [ "$side" = "r" -a "$rpth" != "" ]
    then
	cpth="$rpth"
	opth="$lpth"
	selected="$FORM_rselected"
	oside=l
    fi
fi

localhost="127.0.0.1:88"

echo "var side  = '$side';"
echo "var oside = '$oside';"
echo "var lpth  = '$lpth';"
echo "var rpth  = '$rpth';"
echo "var cpth  = '$cpth';"
echo "var opth  = '$opth';"

if [ -f "$cpth" ]
then
    echo "var cpth = '$cpth';"
    echo "var dest='fm-action.cgi?action=play&amp;side=$side&amp;${side}pth=$cpth&amp;${oside}pth=$opth&amp;select=${selected}';"
    echo "window.location.replace(dest);"
fi

if [ -n "$FORM_select" ]
then
    [ "$FORM_select" -gt 0 ] && echo "var current=${FORM_select};" || echo "var current=1;"
else
    echo "var current=1;"
fi

[ "$FORM_movieinforefresh" = "1" ] && echo "var movieInfoRefresh=1;" || echo "var movieInfoRefresh=0;"

colspan=2 # span columns for filemanager
fnamewidth="43%" # filename field width

if [ "$HTTP_HOST" != "$localhost" ]
then
    lupload="<form action='cgi-bin/tmp/lupload.cgix?upload_dir=$lpth' method='post' enctype='multipart/form-data'><td id='lupload' valign='top' align='center' bgcolor='yellow' width='3%' style='min-width: 32px; max-width: 32px;'><input type='button' class='upload' id='lpseudobutton' value='Upload' onclick=\"document.getElementById('luploadbutton').click();\" ><input type='file' onchange=\"document.getElementById('luploadsubmit').click();\" class='uploadhide' name='uploadfile' id='luploadbutton'><input class='uploadhide' id='luploadsubmit' type='submit' value='Upload'></td></form>"
    rupload="<form action='cgi-bin/tmp/rupload.cgix?upload_dir=$rpth' method='post' enctype='multipart/form-data'><td id='rupload' valign='top' align='center' bgcolor='yellow' width='3%' style='min-width: 32px; max-width: 32px;'><input type='button' class='upload' id='rpseudobutton' value='Upload' onclick=\"document.getElementById('ruploadbutton').click();\" ><input type='file' onchange=\"document.getElementById('ruploadsubmit').click();\" class='uploadhide' name='uploadfile' id='ruploadbutton'><input class='uploadhide' id='ruploadsubmit' type='submit' value='Upload'></td></form>"
    colspan=3
    fnamewidth="33%"
fi

?>

var col = 1; //number of 'cells' in a row
//var current = 1;

var currentLink;
var next = current;
//var side = 'l';
var nside = side;
var dialog_displayed = 0;

//******** MOBILE PHONE-STYLE KEYPAD *********
var keys = new Array();

keys['0'] = new Object();
keys['0'].ctr = 0;
keys['0'].char = [' ','0','+','*','-','\\','=','<','>'];

keys['1'] = new Object();
keys['1'].ctr = 0;
keys['1'].char = ['.',':',',','/','1','@','(',')','[',']','$','%','#','&'];

keys['2'] = new Object();
keys['2'].ctr = 0;
keys['2'].char = ['a','b','c','2','à'];

keys['3'] = new Object();
keys['3'].ctr = 0;
keys['3'].char = ['d','e','f','3','è','é'];

keys['4'] = new Object();
keys['4'].ctr = 0;
keys['4'].char = ['g','h','i','4','ì'];

keys['5'] = new Object();
keys['5'].ctr = 0;
keys['5'].char = ['j','k','l','5'];

keys['6'] = new Object();
keys['6'].ctr = 0;
keys['6'].char = ['m','n','o','6','ò','ó'];

keys['7'] = new Object();
keys['7'].ctr = 0;
keys['7'].char = ['p','q','r','s','7'];

keys['8'] = new Object();
keys['8'].ctr = 0;
keys['8'].char = ['t','u','v','8','ù'];

keys['9'] = new Object();
keys['9'].ctr = 0;
keys['9'].char = ['w','x','y','z','9'];

var append=false;
var upper=false;
var key_char='';
var str='';
var timer;
var prevNum=null;
var currElementName='txtName';
var dialog_win;

function keypad(num)
{
  var currFocusedElement = document.forms['text'].elements[currElementName];
  if (prevNum!=null && prevNum!=num) append=true;
  if (keys[num].ctr>keys[num].char.length-1 || append) keys[num].ctr=0; //go back to first item in keypad
  if (upper) key_char=keys[num].char[keys[num].ctr].toUpperCase(); else key_char=keys[num].char[keys[num].ctr];
  if (append)
	str=currFocusedElement.value+key_char;
  else
	str=(currFocusedElement.value.length==0) ? currFocusedElement.value=key_char:currFocusedElement.value.substring(0,currFocusedElement.value.length-1)+key_char;
  currFocusedElement.value=str;
  keys[num].ctr++;
  prevNum=num;
  //reset
  append=false;
  clearTimeout(timer);
  timer=setTimeout(function(){append=true;}, 2000);
}

//******** END OF MOBILE PHONE-STYLE KEYPAD *********

//Attach the function with the event
if(document.addEventListener)
    {
    document.addEventListener('keydown', check, false);
    window.addEventListener('resize', windowResize, false);
    }
else if(document.attachEvent)
    {
    document.attachEvent('onkeydown', func);
    window.attachEvent('onresize', func);
    }
else
    {
    document.onkeydown = check;
    window.onresize = windowResize;
    }

//window.onload = OnLoadSetCurrent;

function check(e)
	{
	if (!e) var e = window.event;
	(e.keyCode) ? key = e.keyCode : key = e.which;
	//workaround to check for 'enter' on WebKit/KHTML which doesnt want to work in 'try' block
	if (key==10|key==13|key==32) 
		{   //ENTER/OK and SPACE
		    if (dialog_displayed==0)
			{
			document.getElementById('link_' + side + current).click();
			}
		    else if (dialog_win=='copy'|dialog_win=='move'|dialog_win=='delete')
			{
			document.forms["action"].submit();
			e.preventDefault();
			}
		    return false;
		}
	try
		{
		switch(key)
			{
			case  9: next = current; if (side=='l') { nside = 'r'; cpth=rpth; opth=lpth; } else { nside = 'l'; cpth=lpth; opth=rpth; }; break; //FAV/TAB
			case 33: next = (1*current) - 10; break;                           //CH UP
			case 34: next = (1*current) + 10; break;                           //CH DOWN
			case 37: next = current; nside = 'l'; cpth=lpth; opth=rpth; break; //LEFT
			case 38: next = current - col; break;                              //UP
			case 39: next = current; nside = 'r'; cpth=rpth; opth=lpth; break; //RIGHT
			case 40: next = (1*current) + col; break;                          //DOWN
			}
		if (key==9|key==33|key==34|key==37|key==38|key==39|key==40)
		    {
		    if (dialog_displayed==0)
			{
			selectItem();
			//Prevent default action (ie. scrolling)
			e.preventDefault();
			return false;
			}
		    }
		else if (key==19|key==220) 
			{
			//the PAUSE button on the remote control have been pressed or '\' on keyboard
			if (dialog_displayed==1&&dialog_win!='movieinfo')
			    if (upper) upper=false; else upper=true;
			else 
			    {
			    //Set the same panel location path as current on other panel
			    var dest='fm.cgi?amp;type=related&amp;side=' + side + '&amp;lpth=' + opth + '&amp;rpth=' + opth;
			    window.location=dest;
			    }
			//Prevent default action
			e.preventDefault();
			return false;
			}
		//else if (key==19) 
		//	{
		//	if (dialog_displayed==1&movieInfoRefresh==0)
		//	    movieInfoRefresh=1;
		//	else
		//	    movieInfoRefresh=0;
		//	movieInfo();
		//	e.preventDefault();
		//	return false;
		//	}
		else if (key==48) 
			{
			//the 0 on the remote control have been pressed
			//use the keypad function
			if (dialog_displayed==1)
			    {
			    keypad('0');
			    //return false;
			    } else { status(); }
			}
		else if (key==49|key==457) 
			{
			//the 1 or INFO button on the remote control have been pressed
			//use the keypad function
			if (dialog_displayed==1&&dialog_win!='movieinfo')
			    {
			    keypad('1');
			    //return false;
			    } else {
				if (dialog_displayed==1&&movieInfoRefresh==0)
				    movieInfoRefresh=1;
				else
				    movieInfoRefresh=0;
				movieInfo();
			    }
			}
		else if (key==50) 
			{
			//the 2 on the remote control have been pressed
			//use the keypad function
			if (dialog_displayed==1)
			    {
			    keypad('2');
			    //return false;
			    }
			}
		else if (key==51) 
			{
			//the 3 on the remote control have been pressed
			//use the keypad function
			if (dialog_displayed==1)
			    {
			    keypad('3');
			    //return false;
			    }
			}
		else if (key==52) 
			{
			//the 4 on the remote control have been pressed
			//use the keypad function
			if (dialog_displayed==1)
			    {
			    keypad('4');
			    //return false;
			    }
			}
		else if (key==53) 
			{
			//the 5 on the remote control have been pressed
			//use the keypad function
			if (dialog_displayed==1)
			    {
			    keypad('5');
			    //return false;
			    }
			}
		else if (key==54) 
			{
			//the 6 on the remote control have been pressed
			//use the keypad function
			if (dialog_displayed==1)
			    {
			    keypad('6');
			    //return false;
			    }
			}
		else if (key==55) 
			{
			//the 7 on the remote control have been pressed
			//use the keypad function
			if (dialog_displayed==1)
			    {
			    keypad('7');
			    //return false;
			    }
			}
		else if (key==56) 
			{
			//the 8 on the remote control have been pressed
			//use the keypad function
			if (dialog_displayed==1)
			    {
			    keypad('8');
			    //return false;
			    }
			}
		else if (key==57) 
			{
			//the 9 on the remote control have been pressed
			//use the keypad function
			if (dialog_displayed==1)
			    {
			    keypad('9');
			    //return false;
			    }
			}
		else if (key==403|key==119) 
			{
			//the RED button on the remote control or F8 have been pressed
			//Delete file or directory
			// lpath and rpath variables are wrong - but the right ones lpth and rpth are gathered from link
			var dest='fm-action.cgi?amp;action=delete' + '&amp;side=' + side + '&amp;link=' + document.getElementById('link_' + side + current).href;
			deleteDialog();
			//Prevent default action
			e.preventDefault();
			return false;
			}
		else if (key==404|key==116) 
			{
			//the GREEN button on the remote control or F5 have been pressed
			//Copy file or directory
			var dest='fm-action.cgi?action=copy' + '&amp;side=' + side + '&amp;link=' + document.getElementById('link_' + side + current).href;
			copyDialog();
			//Prevent default action
			e.preventDefault();
			return false;
			}
		else if (key==405|key==117) 
			{
			//the YELLOW button on the remote control or F6 have been pressed
			//Move file or directory
			var dest='fm-action.cgi?action=move' + '&amp;side=' + side + '&amp;link=' + document.getElementById('link_' + side + current).href;
			moveDialog();
			//Prevent default action
			e.preventDefault();
			return false;
			}
		//else if (key==406|key==415) 
		else if (key==406|key==118)
			{
			//the BLUE button on the remote control or F7 have been pressed
			//Open directory creation dialog
			if (dialog_displayed==0)
			    {
			    mkdirDialog();
			    e.preventDefault();
			    }
			else
			    {
			    BackSpace();
			    }
			return false;
			}
		else if (key==413|key==120)
			{
			//the STOP button on the remote control or F9 have been pressed
			//Open rename dialog
			if (dialog_displayed==0)
			    {
			    renameDialog();
			    e.preventDefault();
			    }
			return false;
			}
		else if (key==415) 
			{
			//the PLAY button on the remote control have been pressed
			//Play the media file
			play();
			}
		else if (key==461|key==27) 
			{
			//the BACK button on the remote control or ESC have been pressed
			if (dialog_displayed==0)
			    {
			    //NetCastBack API
			    //window.NetCastBack();
			    //lets get back to WebUI instead of closing NetCast service
			    history.go(-1);
			    }
			else
			    {
			    dialogRemove();
			    }
			//Prevent default action
			return false;
			}
		else if (key==1001) 
			{
			//the EXIT button on the remote control have been pressed
			//NetCastExit API
			window.NetCastExit();
			//Prevent default action
			return false;
			}
		}catch(Exception){}
	if ((dialog_displayed==0)|(dialog_win=='move')|(dialog_win=='copy')|(dialog_win=='delete')|((key>=48)&&(key<=57)))
	    {
	    if (e.stopPropagation)
		{
		e.stopPropagation();
		e.preventDefault();
		}
	    }
	}

function ChangeBgColor()
	{
	//Change the TD element BgColor.
	// TODO: experiment with childNodes of table, for example:
	// Get your row by finding the TBODY, and find your cell using
	// childNodes[row].childNodes[col]
	// ^- that should improve performance comparing to getElementById()
	document.getElementById('tr_' + side + current).bgColor = '#FFFFFF';
	//currentLink.bgColor = '#FFFFFF';
	document.getElementById('tr_' + nside + next).bgColor = '#D3D3D3';
	}

function BackSpace()
	{
	//Send a backspace on the currFocusedElement field
	var Text = document.forms['text'].elements[currElementName].value;
	document.forms['text'].elements[currElementName].value = Text.slice(0,Text.length-1);
	}

function setCurrent(element)
	{
	var string = element.id;
	//cut number after 'link' name
	current = string.slice(4,string.length);
	}
	

function OnLoadSetCurrent(element)
	{
	document.links['link_' + side + current].focus();
	ChangeBgColor();
	windowResize();
	}

function mkdirDialog()
	{
	var newdiv = document.createElement("div");
	var newdivWidth=716;
	var newdivHeight=176;
	var newdivLeft=(window.innerWidth/2)-(newdivWidth/2)-10;
	var newdivTop=(window.innerHeight/2)-(newdivHeight/2)-5;
	newdiv.setAttribute('style', 'background: #efef00; position:absolute; padding:20px 10px 0 10px; top:' + newdivTop + 'px; left:' + newdivLeft + 'px; width:' + newdivWidth + 'px; height:' + newdivHeight + 'px; border:2px solid black;');
	newdiv.id = "dialogWin";
	document.body.appendChild(newdiv);
	var kb = '<FONT color="black" size="+3"> \
	    <center><b>Type name for directory to be created:</b></center><br/> \
	    <form id="text" name="text" action="fm.cgi" method="GET"> \
	    <input id="txtName" name="txtName" type="textarea" style="width:710px"> \
	    <input type="hidden" name="side" value="' + side + '"> \
	    <input type="hidden" name="lpth" value="' + lpth + '"> \
	    <input type="hidden" name="rpth" value="' + rpth + '"> \
	    <input type="hidden" name="select" value="' + current + '"> \
	    <input type="hidden" name="action" value="mkdir"> \
	    <table width="100%"><tr valign="middle"><td align="right" valign="middle"><span onClick="javascript:document.forms[\'text\'].submit();"><img src="/Images/Keyboard/ok_button.png" border="0" /><font size="+3"> OK</font></span></td><td align="center" valign="middle"><span onClick="javascript:dialogRemove();"><img src="/Images/Keyboard/back_button.png" border="0" /><font size="+3"> Cancel</font></span></td></tr></table></form></font>';
	newdiv.innerHTML = kb;
	document.getElementById('txtName').focus();
	dialog_displayed = 1;
	}

function copyDialog()
	{
	dialog_win='copy';
	var newdiv = document.createElement("div");
	var newdivWidth=916;
	var newdivHeight=276;
	var newdivLeft=(window.innerWidth/2)-(newdivWidth/2)-10;
	var newdivTop=(window.innerHeight/2)-(newdivHeight/2)-5;
	newdiv.setAttribute('style', 'background: #efef00; position:absolute; padding:20px 10px 0 10px; top:' + newdivTop + 'px; left:' + newdivLeft + 'px; width:' + newdivWidth + 'px; height:' + newdivHeight + 'px; border:2px solid black;');
	newdiv.id = "dialogWin";
	document.body.appendChild(newdiv);
	src=cpth + '/' + document.getElementById('link_' + side + current).name;
	if (side=='l')
	    {
		var lpth_fix=src;
		var rpth_fix=rpth;
	    }
	else
	    {
		var lpth_fix=lpth;
		var rpth_fix=src;
	    }
	var kb = '<FONT color="brown" size="+3"> \
	    <center><b>Are you sure you want to copy?</b><br/><br/> \
	    <font size="+2" color="black">' + src + '<br/><br/><b>to:</b><br/><br/>' + opth + '/<br/></font> \
	    <form id="action" name="action" action="fm-action.cgi" method="GET"> \
	    <input type="hidden" name="side" value="' + side + '"> \
	    <input type="hidden" name="lpth" value="' + lpth_fix + '"> \
	    <input type="hidden" name="rpth" value="' + rpth_fix + '"> \
	    <input type="hidden" name="select" value="' + current + '"> \
	    <input type="hidden" name="action" value="copy"> \
	    <input type="hidden" name="confirm" value="yes"><br/> \
	    <table width="100%"><tr valign="middle"><td align="right" valign="middle"><span onClick="javascript:document.forms[\'action\'].submit();"><img src="/Images/Keyboard/ok_button.png" border="0" /><font size="+3"> OK</font></span></td><td align="center" valign="middle"><span onClick="javascript:dialogRemove();"><img src="/Images/Keyboard/back_button.png" border="0" /><font size="+3"> Cancel</font></span></td></tr></table></form></center></font>';
	newdiv.innerHTML = kb;
	dialog_displayed = 1;
	}

function moveDialog()
	{
	dialog_win='move';
	var newdiv = document.createElement("div");
	var newdivWidth=916;
	var newdivHeight=276;
	var newdivLeft=(window.innerWidth/2)-(newdivWidth/2)-10;
	var newdivTop=(window.innerHeight/2)-(newdivHeight/2)-5;
	newdiv.setAttribute('style', 'background: #efef00; position:absolute; padding:20px 10px 0 10px; top:' + newdivTop + 'px; left:' + newdivLeft + 'px; width:' + newdivWidth + 'px; height:' + newdivHeight + 'px; border:2px solid black;');
	newdiv.id = "dialogWin";
	document.body.appendChild(newdiv);
	src=cpth + '/' + document.getElementById('link_' + side + current).name;
	if (side=='l')
	    {
		var lpth_fix=src;
		var rpth_fix=rpth;
	    }
	else
	    {
		var lpth_fix=lpth;
		var rpth_fix=src;
	    }
	var previous=current-1;
	var kb = '<FONT color="brown" size="+3"> \
	    <center><b>Are you sure you want to move?</b><br/><br/> \
	    <font size="+2" color="black">' + src + '<br/><br/><b>to:</b><br/><br/>' + opth + '/<br/></font> \
	    <form id="action" name="action" action="fm-action.cgi" method="GET"> \
	    <input type="hidden" name="side" value="' + side + '"> \
	    <input type="hidden" name="lpth" value="' + lpth_fix + '"> \
	    <input type="hidden" name="rpth" value="' + rpth_fix + '"> \
	    <input type="hidden" name="select" value="' + previous + '"> \
	    <input type="hidden" name="action" value="move"> \
	    <input type="hidden" name="confirm" value="yes"><br/> \
	    <table width="100%"><tr valign="middle"><td align="right" valign="middle"><span onClick="javascript:document.forms[\'action\'].submit();"><img src="/Images/Keyboard/ok_button.png" border="0" /><font size="+3"> OK</font></span></td><td align="center" valign="middle"><span onClick="javascript:dialogRemove();"><img src="/Images/Keyboard/back_button.png" border="0" /><font size="+3"> Cancel</font></span></td></tr></table></form></center></font>';
	newdiv.innerHTML = kb;
	dialog_displayed = 1;
	}

function renameDialog()
	{
	var newdiv = document.createElement("div");
	var newdivWidth=716;
	var newdivHeight=176;
	var newdivLeft=(window.innerWidth/2)-(newdivWidth/2)-10;
	var newdivTop=(window.innerHeight/2)-(newdivHeight/2)-5;
	newdiv.setAttribute('style', 'background: #efef00; position:absolute; padding:20px 10px 0 10px; top:' + newdivTop + 'px; left:' + newdivLeft + 'px; width:' + newdivWidth + 'px; height:' + newdivHeight + 'px; border:2px solid black;');
	newdiv.id = "dialogWin";
	document.body.appendChild(newdiv);
	var kb = '<FONT color="black" size="+3"> \
	    <center><b>Type new name for renamed file or directory:</b></center><br/> \
	    <form id="text" name="text" action="fm.cgi" method="GET"> \
	    <input id="txtName" name="txtName" type="textarea" style="width:710px" value="' + document.getElementById('link_' + side + current).name + '"> \
	    <input id="txtOldName" name="txtOldName" type="hidden" value="' + document.getElementById('link_' + side + current).name + '"> \
	    <input type="hidden" name="side" value="' + side + '"> \
	    <input type="hidden" name="lpth" value="' + lpth + '"> \
	    <input type="hidden" name="rpth" value="' + rpth + '"> \
	    <input type="hidden" name="select" value="' + current + '"> \
	    <input type="hidden" name="action" value="rename"> \
	    <table width="100%"><tr valign="middle"><td align="right" valign="middle"><span onClick="javascript:document.forms[\'text\'].submit();"><img src="/Images/Keyboard/ok_button.png" border="0" /><font size="+3"> OK</font></span></td><td align="center" valign="middle"><span onClick="javascript:dialogRemove();"><img src="/Images/Keyboard/back_button.png" border="0" /><font size="+3"> Cancel</font></span></td></tr></table></form></font>';
	newdiv.innerHTML = kb;
	document.getElementById('txtName').focus();
	dialog_displayed = 1;
	}

function deleteDialog()
	{
	dialog_win='delete';
	var newdiv = document.createElement("div");
	var newdivWidth=716;
	var newdivHeight=176;
	var newdivLeft=(window.innerWidth/2)-(newdivWidth/2)-10;
	var newdivTop=(window.innerHeight/2)-(newdivHeight/2)-5;
	newdiv.setAttribute('style', 'background: #efef00; position:absolute; padding:20px 10px 0 10px; top:' + newdivTop + 'px; left:' + newdivLeft + 'px; width:' + newdivWidth + 'px; height:' + newdivHeight + 'px; border:2px solid black;');
	newdiv.id = "dialogWin";
	document.body.appendChild(newdiv);
	src=cpth + '/' + document.getElementById('link_' + side + current).name;
	if (side=='l')
	    {
		var lpth_fix=src;
		var rpth_fix=rpth;
	    }
	else
	    {
		var lpth_fix=lpth;
		var rpth_fix=src;
	    }
	var previous=current-1;
	var kb = '<FONT color="brown" size="+3"> \
	    <center><b>Are you sure you want to delete?</b><br/><br/> \
	    <font size="+2" color="black">' + src + '<br/></font> \
	    <form id="action" name="action" action="fm-action.cgi" method="GET"> \
	    <input type="hidden" name="side" value="' + side + '"> \
	    <input type="hidden" name="lpth" value="' + lpth_fix + '"> \
	    <input type="hidden" name="rpth" value="' + rpth_fix + '"> \
	    <input type="hidden" name="select" value="' + previous + '"> \
	    <input type="hidden" name="action" value="delete"> \
	    <input type="hidden" name="confirm" value="yes"><br/> \
	    <table width="100%"><tr valign="middle"><td align="right" valign="middle"><span onClick="javascript:document.forms[\'action\'].submit();"><img src="/Images/Keyboard/ok_button.png" border="0" /><font size="+3"> OK</font></span></td><td align="center" valign="middle"><span onClick="javascript:dialogRemove();"><img src="/Images/Keyboard/back_button.png" border="0" /><font size="+3"> Cancel</font></span></td></tr></table></form></center></font>';
	newdiv.innerHTML = kb;
	dialog_displayed = 1;
	}

function dialogRemove()
	{
        document.body.removeChild(document.getElementById("dialogWin"));
	dialog_displayed = 0;
	dialog_win = '';
	OnLoadSetCurrent();
        }

function movieInfo()
	{
	src=cpth + '/' + document.getElementById('link_' + side + current).name;
	dest='fm.cgi?side=' + side + '&amp;lpth=' + lpth + '&amp;rpth=' + rpth + '&amp;select=' + current + '&amp;action=movieinfo&amp;movieinforefresh=' + movieInfoRefresh + '&amp;file=' + src;
	if (movieInfoRefresh==1)
	    window.location.replace(dest);
	else
	    window.location=dest;
	}

function windowResize()
	{
	var filenameSize=(window.innerWidth/2)-200;
	var fulltablestyle=document.getElementById('fulltable').style;
	fulltablestyle.height=window.innerHeight-32;
	document.getElementById('lpaneltbody').style.maxHeight=window.innerHeight-70;
	document.getElementById('rpaneltbody').style.maxHeight=window.innerHeight-70;
	document.body.style.height=window.innerHeight-20;
	}

function selectItem()
	{
	//Check if new link exists, if not then go to previous one until finds the one that exists
	if (next<=0) next = 1;
	currentLink=document.links['link_' + nside + next];
	if (!currentLink)
	{
	    do {
		next = next - 1;
		currentLink=document.links['link_' + nside + next];
	    } while ((!currentLink)&&(next >= 1));
	}

	currentLink=document.links['link_' + nside + next];
	if (!currentLink)
	{
	    do {
		next = next - 1;
		currentLink=document.links['link_' + nside + next];
	    } while ((!currentLink)&&(next >= 1));
	}
	ChangeBgColor();
	//Move to the next link
	currentLink.focus();
	current = next;
	side = nside;
	}

function play()
	{
	var dest='fm-action.cgi?action=play' + '&amp;side=' + side + '&amp;lpath=' + lpth + '&amp;rpath=' + rpth + '&amp;link=' + document.getElementById('link_' + side + current).href + '&amp;skip=next&amp;imgzoom=0&amp;timeout=7000';
	window.location=dest;
	}

function status()
	{
	<? echo "var dest='fm-action.cgi?action=status&amp;side=' + side + '&amp;lpth=${lpth}&amp;rpth=${rpth}&amp;select=' + current;" ?>
	window.location=dest;
	}

document.defaultAction = true;

// -->
</script>

</HEAD>
<BODY bgcolor="black">

<?

# TODO: make error handling with error message
if [ "$FORM_action" = "mkdir" -a "$cpth" != "" -a "$FORM_txtName" != "" ]
then
    mkdir -p "$cpth/$FORM_txtName"
fi
if [ "$FORM_action" = "rename" -a "$cpth" != "" -a "$FORM_txtOldName" != "" -a "$FORM_txtName" != "" ]
then
    mv "$cpth/$FORM_txtOldName" "$cpth/$FORM_txtName"
fi
if [ "$FORM_action" = "movieinfo" -a "$cpth" != "" -a "$FORM_file" != "" ]
then
    movieinfo="`dirname "$FORM_file"`/.MovieInfo"
    mkdir -p "$movieinfo" > /dev/null 2>&1 || movieinfo="$log_dir/.MovieInfo" && mkdir -p "$movieinfo" > /dev/null 2>&1
    movieinfo_file="`basename "$FORM_file"`"
    movieinfo_fileimg="${movieinfo}/${movieinfo_file}.jpg"
    echo "<center><b><font size='+4' color='yellow'><br/>Loading movie info for file:<br/><font size='+3'><br/>$movieinfo_file</font></font></b></center>"
    echo "FORM_file=\"$FORM_file\" outdir=\"$movieinfo\" movieinfo_fileimg=\"$movieinfo_fileimg\"" >> "$log_dir/imdb.log"
    [ ! -f "$movieinfo_fileimg" -o "$FORM_movieinforefresh" = "1" ] && /scripts/imdb.sh "$FORM_file" outdir="$movieinfo" >> "$log_dir/imdb.log" && sleep 0.5
    echo -e "<script type='text/javascript'> \n\
	    document.body.innerHTML = '';"
    if [ -f "$movieinfo_fileimg" ]
    then
	#sleep 1
	movieinfo_fileimg="${movieinfo_fileimg//'/\\'}"
	#    newdiv.setAttribute('style', 'background: #000000; position:absolute; padding:0px 0px 0 0px; top: 0px; left: 0px; width:' + newdivWidth + 'px; height:' + newdivHeight + 'px; border:0px solid black;'); \n\
	echo -e "\
	    var dialog_win='movieinfo'; \n\
	    var newdiv = document.createElement('div'); \n\
	    var newdivWidth=window.innerWidth; \n\
	    var newdivHeight=window.innerHeight; \n\
	    newdiv.setAttribute('style', 'background: #000000; position:absolute; padding:0px 0px 0 0px; top: 0px; left: 0px; width:' + newdivWidth + 'px; height:' + newdivHeight + 'px;'); \n\
	    newdiv.id = 'dialogWin'; \n\
	    document.body.appendChild(newdiv); \n\
	    var kb='<img src=\"root$movieinfo_fileimg\" alt=\"$movieinfo_fileimg\"/>'; \n\
	    newdiv.innerHTML = kb; \n\
	    dialog_displayed = 1;"
    fi
	#    var kb='<img src=\"root$movieinfo_fileimg\" alt=\"$movieinfo_fileimg\"/><div style='opacity:0.6; filter:alpha(opacity=60); position:absolute; padding:0px 0px 0 0px; top: 400px; left: 400px; width: 110px; height: 30px;'><img src='Images/Keyboard/ok_button.png'/></div>; \
    echo "</script>"
fi

mountpoints="`egrep -v '^/dev/mtdblock| / |^proc|^tmp|^sysfs|^usbfs|^devpts| /usr/etc |^bt|^lgapp_xip' /proc/mounts | cut -d' ' -f2 | tr '\n' ' '`"
mountpoints_length="${#mountpoints}"

    echo "<table id='fulltable' width='100%' border='1' bordercolor='blue' cellspacing='5' bgcolor='white' padding='0' cellpadding='0px'>"
    lpth_crop="$lpth"
    rpth_crop="$rpth"
    # static size to cut path at 77 chars to fit 1280 width on most web browsers that respect monotype font style
    [ "${#lpth}" -gt "77" ] && lpth_crop="${lpth:0:63} ~~ ${lpth:$((${#lpth}-10))}"
    [ "${#rpth}" -gt "77" ] && rpth_crop="${rpth:0:63} ~~ ${rpth:$((${#rpth}-10))}"
    #[ "$HTTP_HOST" != "$localhost" ] && lupload="<form action='cgi-bin/firmware-upgrade.cgix' method='post' enctype='multipart/form-data' ><td id='lupload' valign='top' bgcolor='yellow' width='1%' style='max-width: 37px;'><input type='button' class='upload' id='pseudobutton' value='Upload' onclick=\"document.getElementById('uploadbutton').click();\"><input type='file' class='uploadhide' name='uploadfile' id='uploadbutton' onmousedown=\"buttonPush('depressed');\" onmouseup=\"buttonPush('normal');\" onmouseout=\"buttonPush('phased');\"></td></form>"
    #echo "<thead><tr border='1' height='18px'>$lupload<td id='lpanelpath' valign='top' align='center' bgcolor='yellow' width='$fnamewidth'><b>$lpth_crop/</b></td><td valign='top' align='center' bgcolor='yellow' width='7%' style='min-width:7%;width:7%;max-width:7%;'><b><span id='ldf' name='ldf'>??/??</span></b></td><td id='rpanelpath' valign='top' align='center' bgcolor='yellow' width='43%'><b>$rpth_crop/</b></td><td valign='top' align='center' bgcolor='yellow' width='7%' style='min-width:7%;width:7%;max-width:7%;'><b><span id='rdf' name='rdf'>??/??</span></b></td></tr></thead>"
    echo "<thead><tr border='1' height='18px'>$lupload<td id='lpanelpath' valign='top' align='center' bgcolor='yellow' width='$fnamewidth'><b>$lpth_crop/</b></td><td valign='top' align='center' bgcolor='yellow' width='7%' style='min-width:7%;width:7%;max-width:7%;'><b><span id='ldf' name='ldf'>??/??</span></b></td>$rupload<td id='rpanelpath' valign='top' align='center' bgcolor='yellow' width='$fnamewidth'><b>$rpth_crop/</b></td><td valign='top' align='center' bgcolor='yellow' width='7%' style='min-width:7%;width:7%;max-width:7%;'><b><span id='rdf' name='rdf'>??/??</span></b></td></tr></thead>"
    echo "<tbody id='main'><tr><td valign='top' width='50%' class='panel' colspan='$colspan'>"
    echo '<Table id="lpanel" name="items" class="items" Border="0" cellspacing="0" width="100%"><tbody class="scrollable" id="lpaneltbody">'
    if [ "$lpth" != "" ]
    then
	lpth_up="${lpth%/*}"
	echo "<tr id=\"tr_l1\" onClick=\"javascript:cpth=lpth;opth=rpth;nside='l';next=1;selectItem();\"><td><img src=\"/Images/file_icons/dir.png\"/></td><td class='filename'><a id=\"link_l1\" href=\"fm.cgi?type=related&amp;side=l&amp;lpth=$lpth_up&amp;rpth=$rpth&amp;select=${FORM_lselected}\" target=\"_parent\"><font size='+1'><b>..</b></font><br/></a></td><td class=\"size\" align=\"right\">---&nbsp;&nbsp;</td><td align=\"center\" class=\"date\">---- -- -- ------</td></tr>"
	litem_nr=2
    else
	litem_nr=1
    fi
    SIFS="$IFS"
    IFS=$'\n'
    for lcontent in `stat -c "%F@%n@%z@%A@%s" "$lpth"/* | sort | sed -e "s#@.*/#@#g" -e 's# #\&nbsp;#g'`
    do
	ltype="${lcontent%%@*}"
	lcontent_2x="${lcontent#*@}" # from 2nd columnt up to end
	lfilename="${lcontent_2x%%@*}"
	lfilename_space="${lfilename//&nbsp;/ }"
	lfilename_ext_full="${lfilename_space##*.}"
	lfilename_ext="${lfilename_ext_full:0:5}"
	if [ "${#lfilename_space}" -gt "53" ]
	then
	    if [ "$ltype" = "directory" ]
	    then
		lfilename="${lfilename_space:0:53}~"
		lfilename="${lfilename// /&nbsp;}"
	    else
		lfilename="${lfilename_space:0:47}~.${lfilename_ext}"
		lfilename="${lfilename// /&nbsp;}"
	    fi
	fi
	lcontent_3x="${lcontent_2x#*@}" # from 3rd columnt up to end
	ldate="${lcontent_3x%%@*}"
	ldate_cut="${ldate%%.*}"
	lcontent_4x="${lcontent_3x#*@}" # from 4th columnt up to end
	lperm="${lcontent_4x%%@*}"
	lcontent_5x="${lcontent_4x#*@}" # from 5th columnt up to end
	lsize="${lcontent_5x%%@*}"
	if [ "$ltype" = "directory" ]
	then
	    limage="dir.png"
	    dlink="fm.cgi?type=related&amp;side=l&amp;lpth=$lpth/$lfilename_space&amp;rpth=$rpth"
	else
	    if [ "$ltype" = "symbolic&nbsp;link" ]
	    then
		limage="link.png"
	    else
		limage="generic.gif"
	    fi
	    if [ "${lfilename_ext}" != "" ]
	    then
		#    avi ) dlink="fm-action.cgi?action=play&side=$side&lpath=$lpth/$lfilename_space&rpath=$rpth&link=$lpth/$lfilename_space";;
		case "${lfilename_ext}" in
		    m3u) dlink="vod/m3u.cgi?type=related&amp;side=l&amp;lpth=$lpth/$lfilename_space&amp;rpth=$rpth&amp;url=$lpth/$lfilename_space";;
		    *) dlink="fm.cgi?type=related&amp;side=l&amp;lpth=$lpth/$lfilename_space&amp;rpth=$rpth";;
		esac
	    else
		dlink="fm.cgi?type=related&amp;side=l&amp;lpth=$lpth/$lfilename_space&amp;rpth=$rpth"
	    fi
	fi
	# TODO?: check if file/dir is mountpoint - all methods are slow - paradoxally grep is fastest when the list is long
	# string length comparision is good for not too long strings matchings - few mount points
	check_mountpoints="${mountpoints#*$lpth/$lfilename }"
	#if [ "${mountpoints#*$lpth/$lfilename }" != "${mountpoints}" ]
	#if [ -n "`grep \" $lpth/$lfilename \" /proc/mounts`" ]
	file_color=black
	[ "${#check_mountpoints}" != "${mountpoints_length}" ] && file_color=brown
	echo "<tr id=\"tr_l${litem_nr}\" onClick=\"javascript:cpth=lpth;opth=rpth;nside='l';next=${litem_nr};selectItem();\"><td><img src=\"/Images/file_icons/$limage\"/></td><td class='filename'><a id=\"link_l${litem_nr}\" href=\"${dlink}&amp;lselected=${litem_nr}\" name=\"$lfilename_space\" target=\"_parent\"><font size='+0' color='$file_color'><b>$lfilename</b></font></a></td><td class=\"size\" align=\"right\">$lsize&nbsp;&nbsp;</td><td align=\"center\" class=\"date\">$ldate_cut</td></tr>"
	litem_nr=$(($litem_nr+1))
    done
    IFS="$SIFS"
    echo "</tbody></table></td><td valign='top' width='50%' class='panel' colspan='$colspan'>"
    echo '<Table id="rpanel" name="items" class="items" Border=0 cellspacing=0 width="100%"><tbody class="scrollable" id="rpaneltbody">'
    if [ "$rpth" != "" ]
    then
	rpth_up="${rpth%/*}"
	echo "<tr id=\"tr_r1\" onClick=\"javascript:cpth=rpth;opth=lpth;nside='r';next=1;selectItem();\"><td><img src=\"/Images/file_icons/dir.png\"/></td><td class='filename'><a id=\"link_r1\" href=\"fm.cgi?type=related&amp;side=r&amp;rpth=$rpth_up&amp;lpth=$lpth&amp;select=${FORM_rselected}\" target=\"_parent\"><font size='+1'><b>..</b></font><br/></a></td><td class=\"size\" align=\"right\">---&nbsp;&nbsp;</td><td align=\"center\" class=\"date\">---- -- -- ------</td></tr>"
	ritem_nr=2
    else
	ritem_nr=1
    fi
    SIFS="$IFS"
    IFS=$'\n'
    for rcontent in `stat -c "%F@%n@%z@%A@%s" "$rpth"/* | sort | sed -e "s#@.*/#@#g" -e 's# #\&nbsp;#g'`
    do
	rtype="${rcontent%%@*}"
	rcontent_2x="${rcontent#*@}" # from 2nd columnt up to end
	rfilename="${rcontent_2x%%@*}"
	rfilename_space="${rfilename//&nbsp;/ }"
	rfilename_ext_full="${rfilename_space##*.}"
	rfilename_ext="${rfilename_ext_full:0:5}"
	if [ "${#rfilename_space}" -gt "53" ]
	then
	    if [ "$rtype" = "directory" ]
	    then
		rfilename="${rfilename_space:0:53}~"
		rfilename="${rfilename// /&nbsp;}"
	    else
		rfilename="${rfilename_space:0:47}~.${rfilename_ext}"
		rfilename="${rfilename// /&nbsp;}"
	    fi
	fi
	rcontent_3x="${rcontent_2x#*@}"
	rdate="${rcontent_3x%%@*}"
	rdate_cut="${rdate%%.*}"
	rcontent_4x="${rcontent_3x#*@}"
	rperm="${rcontent_4x%%@*}"
	rcontent_5x="${rcontent_4x#*@}"
	rsize="${rcontent_5x%%@*}"
	if [ "$rtype" = "directory" ]
	then
	    rimage="dir.png"
	else
	    if [ "$rtype" = "symbolic&nbsp;link" ]
	    then
		rimage="link.png"
	    else
		rimage="generic.gif"
	    fi
	fi
	dlink="fm.cgi?type=related&amp;side=r&amp;rpth=$rpth/$rfilename_space&amp;lpth=$lpth"
	file_color=black
	check_mountpoints="${mountpoints#*$rpth/$rfilename }"
	[ "${#check_mountpoints}" != "${mountpoints_length}" ] && file_color=brown
	echo "<tr id=\"tr_r${ritem_nr}\" onClick=\"javascript:cpth=rpth;opth=lpth;nside='r';next=${ritem_nr};selectItem();\"><td><img src=\"/Images/file_icons/$rimage\"/></td><td class='filename'><a id=\"link_r${ritem_nr}\" href=\"${dlink}&amp;rselected=${ritem_nr}\" name=\"$rfilename_space\" target=\"_parent\"><font size='+0' color='$file_color'><b>$rfilename</b></font></a></td><td class=\"size\" align=\"right\">$rsize&nbsp;&nbsp;</td><td align=\"center\" class=\"date\">$rdate_cut</td></tr>"
	ritem_nr=$(($ritem_nr+1))
    done
    IFS="$SIFS"
    echo -n '</tbody></table></td></tr></tbody></table>'
?>
<!-- center><table border="0" cellpadding="0" width="100%"><tr align="center"><td><span onClick="javascript:play();"><font color="white" size="+1">[<img src="/Images/Keyboard/play_button.png" width="22" height="12" border="0" />/OK]</font><font size="+1" color="yellow">PLAY</font></span></td><td><span onClick="javascript:movieInfo();"><font color="white" size="+1">[<img src="/Images/Keyboard/info_button.png" width="22" height="12" border="0" />/1]</font><font size="+1" color="yellow">IMDB</font></span></td><td><span onClick="javascript:renameDialog();"><font color="white" size="+1">[<img src="/Images/Keyboard/stop_button.png" width="22" height="12" border="0" />/F9]</font><font color="yellow" size="+1">RENAME</font></span></td><td><span onClick="javascript:deleteDialog();"><font color="FF3333" size="+1">[<img src="/Images/Keyboard/red_button.png" width="22" height="12" border="0" />/F8]ERASE</font></span></td><td><span onClick="javascript:copyDialog();"><font color="#00FF00" size="+1">[<img src="/Images/Keyboard/green_button.png" width="22" height="12" border="0" />/F5]COPY</font></span></td><td><font color="yellow" size="+1"><b>OpenLGTV BCM FileManager</b> by xeros</font></td><td><span onClick="javascript:moveDialog();"><font color="yellow" size="+1">[<img src="/Images/Keyboard/yellow_button.png" width="22" height="12" border="0" />/F6]MOVE</font></span></td><td><span onClick="javascript:mkdirDialog();"><font color="lightblue" size="+1">[<img src="/Images/Keyboard/blue_button.png" width="22" height="12" border="0" />/F7]MKDIR</font></span></td><td><font color="white" size="+1"><span onClick="javascript:var dest='fm.cgi?type=related&amp;side=' + side + '&amp;lpth=' + opth + '&amp;rpth=' + opth;window.location=dest;">[<img src="/Images/Keyboard/pause_button.png" width="22" height="12" border="0" />/"\"]</font><font color="yellow" size="+1">SAME PATH</font></span></td><td><span onClick="javascript:status();"><font color="white" size="+1">[0]</font><font color="yellow" size="+1">COPY STATUS</font></span></td></tr></table></center -->
<center><table border="0" cellpadding="0" width="100%" style="letter-spacing: -0.2px;"><tr align="center"><td><span onClick="javascript:play();"><font color="white" size="+1">[<img src="/Images/Keyboard/play_button.png" width="22" height="12" border="0" />/OK]</font> <font size="+1" color="yellow">PLAY</font></span></td><td><span onClick="javascript:movieInfo();"><font color="white" size="+1">[<img src="/Images/Keyboard/info_button.png" width="22" height="12" border="0" />/1]</font> <font size="+1" color="yellow">IMDB</font></span></td><td><span onClick="javascript:renameDialog();"><font color="white" size="+1">[<img src="/Images/Keyboard/stop_button.png" width="22" height="12" border="0" />/F9]</font><font color="yellow" size="+1"> RENAME</font></span></td><td><span onClick="javascript:deleteDialog();"><font color="FF3333" size="+1">[<img src="/Images/Keyboard/red_button.png" width="22" height="12" border="0" />/F8] ERASE</font></span></td><td><span onClick="javascript:copyDialog();"><font color="#00FF00" size="+1">[<img src="/Images/Keyboard/green_button.png" width="22" height="12" border="0" />/F5] COPY</font></span></td><td><font color="yellow" size="+1"><b>OpenLGTV BCM FileManager</b> by xeros</font></td><td><span onClick="javascript:moveDialog();"><font color="yellow" size="+1">[<img src="/Images/Keyboard/yellow_button.png" width="22" height="12" border="0" />/F6] MOVE</font></span></td><td><span onClick="javascript:mkdirDialog();"><font color="lightblue" size="+1">[<img src="/Images/Keyboard/blue_button.png" width="22" height="12" border="0" />/F7] MKDIR</font></span></td><td><font color="white" size="+1"><span onClick="javascript:var dest='fm.cgi?type=related&amp;side=' + side + '&amp;lpth=' + opth + '&amp;rpth=' + opth;window.location=dest;">[<img src="/Images/Keyboard/pause_button.png" width="22" height="12" border="0" />/"\"]</font><font color="yellow" size="+1"> SAME PATH</font></span></td><td><span onClick="javascript:status();"><font color="white" size="+1">[0]</font> <font color="yellow" size="+1">COPY STATUS</font></span></td></tr></table></center>
<!-- center><table border="0" cellpadding="0" width="100%" style="word-spacing:-5px;"><tr align="center"><td><span onClick="javascript:play();"><font color="white" size="+1">[<img src="/Images/Keyboard/play_button.png" width="22" height="12" border="0" />/OK]</font> <font size="+1" color="yellow">PLAY</font></span></td><td><span onClick="javascript:movieInfo();"><font color="white" size="+1">[<img src="/Images/Keyboard/info_button.png" width="22" height="12" border="0" />/1]</font> <font size="+1" color="yellow">IMDB</font></span></td><td><span onClick="javascript:renameDialog();"><font color="white" size="+1">[<img src="/Images/Keyboard/stop_button.png" width="22" height="12" border="0" />/F9]</font><font color="yellow" size="+1"> RENAME</font></span></td><td><span onClick="javascript:deleteDialog();"><font color="FF3333" size="+1">[<img src="/Images/Keyboard/red_button.png" width="22" height="12" border="0" />/F8] ERASE</font></span></td><td><span onClick="javascript:copyDialog();"><font color="#00FF00" size="+1">[<img src="/Images/Keyboard/green_button.png" width="22" height="12" border="0" />/F5] COPY</font></span></td><td><font color="yellow" size="+1"><b>OpenLGTV BCM FileManager</b> by xeros</font></td><td><span onClick="javascript:moveDialog();"><font color="yellow" size="+1">[<img src="/Images/Keyboard/yellow_button.png" width="22" height="12" border="0" />/F6] MOVE</font></span></td><td><span onClick="javascript:mkdirDialog();"><font color="lightblue" size="+1">[<img src="/Images/Keyboard/blue_button.png" width="22" height="12" border="0" />/F7] MKDIR</font></span></td><td><font color="white" size="+1"><span onClick="javascript:var dest='fm.cgi?type=related&amp;side=' + side + '&amp;lpth=' + opth + '&amp;rpth=' + opth;window.location=dest;">[<img src="/Images/Keyboard/pause_button.png" width="22" height="12" border="0" />/"\"]</font><font color="yellow" size="+1"> SAME PATH</font></span></td><td><span onClick="javascript:status();"><font color="white" size="+1">[0]</font> <font color="yellow" size="+1">COPY STATUS</font></span></td></tr></table></center -->

</BODY></HTML>
<script type='text/javascript'>OnLoadSetCurrent();</script>
<script type='text/javascript'>
<?
    spaceinfo=`df -P -h "$lpth/" "$rpth/" | tail -n +2 | sed 's/^[^ ]* *\([^ ]*\) *[^ ]* *\([^ ]*\) */\2\/\1 /g'`
    # $1 - free/total space, $2 - %, $3 - mount path (can have spaces)
    lspcinfo=`echo "${spaceinfo}" | head -n 1`
    rspcinfo=`echo "${spaceinfo}" | tail -n 1`
    ldf="${lspcinfo%% *}"
    rdf="${rspcinfo%% *}"
    lpthmnt="/${lspcinfo#*/*/}"
    rpthmnt="/${rspcinfo#*/*/}"
    #echo "document.getElementById('ldf').innerHTML ='`df -h \"$lpth/\" | tail -n 1 | sed 's/^[^ ]* *\([^ ]*\) *[^ ]* *\([^ ]*\) *.*/\2\/\1/g'`';"
    #echo "document.getElementById('rdf').innerHTML ='`df -h \"$rpth/\" | tail -n 1 | sed 's/^[^ ]* *\([^ ]*\) *[^ ]* *\([^ ]*\) *.*/\2\/\1/g'`';"
    echo "document.getElementById('ldf').innerHTML ='$ldf';"
    echo "document.getElementById('rdf').innerHTML ='$rdf';"
    if [ "$HTTP_HOST" != "$localhost" ]
    then
	lfree="${ldf%/*}"
	rfree="${rdf%/*}"
	lfreeq="${lfree/,/}"
	lfreeq="${lfreeq/./}"
	rfreeq="${rfree/,/}"
	rfreeq="${rfreeq/./}"
	#echo "lfree $lfree lfreeq $lfreeq rfree $rfree rfreeq $rfreeq"
	if [ "${lfree/K/}" != "$lfree" ]
	then
	    lmulti="1"
	    lfreeq="${lfree%,*}"
	    lfreeq="${lfreeq%.*}"
	    lfreeq="${lfreeq/K/}"
	else
	    [ "$lfreeq" != "$lfree" ] && lmulti="100" || lmulti="1000"
	    lfreeq="${lfreeq/M/}"
	    lfreeq="${lfreeq/G/}"
	    lfreeq="${lfreeq/T/}"
	fi
	[ "${lfree/G/}" != "$lfree" ] && lmulti="$lmulti*1000"
	[ "${lfree/T/}" != "$lfree" ] && lmulti="$lmulti*1000*1024"
	lfreek="$((${lfreeq}*${lmulti}))"
	if [ "${rfree/K/}" != "$rfree" ]
	then
	    rmulti="1"
	    rfreeq="${rfree%,*}"
	    rfreeq="${rfreeq%.*}"
	    rfreeq="${rfreeq/K/}"
	else
	    [ "$rfreeq" != "$rfree" ] && rmulti="100" || rmulti="1000"
	    rfreeq="${rfreeq/M/}"
	    rfreeq="${rfreeq/G/}"
	    rfreeq="${rfreeq/T/}"
	fi
	[ "${rfree/G/}" != "$rfree" ] && rmulti="$rmulti*1000"
	[ "${rfree/T/}" != "$rfree" ] && rmulti="$rmulti*1000*1024"
	rfreek="$((${rfreeq}*${rmulti}))"
	[ "$lpthmnt" = "/" ] && lpthmnt="/tmp"
	[ "$rpthmnt" = "/" ] && rpthmnt="/tmp"
	#echo "$lfree $lfreek $rfree $rfreek"
	echo "#!/usr/bin/haserl --upload-limit=$lfreek --upload-dir=$lpthmnt --accept-all /var/www/cgi-bin/upload.cgix" > /var/www/cgi-bin/tmp/lupload.cgix &
	echo "#!/usr/bin/haserl --upload-limit=$rfreek --upload-dir=$rpthmnt --accept-all /var/www/cgi-bin/upload.cgix" > /var/www/cgi-bin/tmp/rupload.cgix &
	chmod +x /var/www/cgi-bin/tmp/* &
    fi
?></script>

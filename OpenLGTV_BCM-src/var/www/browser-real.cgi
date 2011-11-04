#!/bin/haserl
content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>

<!-- Code for OpenLGTV BCM Browser by Nicola Ottomano -->
<!-- Source code released under GPL License -->

<title>OpenLGTV BCM Browser</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<meta http-equiv="Content-Style-Type" content="text/css">
<meta http-equiv="Content-Script-Type" content="text/javascript">

<link rel="stylesheet" type="text/css" href="css/keyboard.css"/>
	
<script type="text/javascript">

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
keys['2'].char = ['a','b','c','2','�'];

keys['3'] = new Object();
keys['3'].ctr = 0;
keys['3'].char = ['d','e','f','3','�','�'];

keys['4'] = new Object();
keys['4'].ctr = 0;
keys['4'].char = ['g','h','i','4','�'];

keys['5'] = new Object();
keys['5'].ctr = 0;
keys['5'].char = ['j','k','l','5'];

keys['6'] = new Object();
keys['6'].ctr = 0;
keys['6'].char = ['m','n','o','6','�','�'];

keys['7'] = new Object();
keys['7'].ctr = 0;
keys['7'].char = ['p','q','r','s','7'];

keys['8'] = new Object();
keys['8'].ctr = 0;
keys['8'].char = ['t','u','v','8','�'];

keys['9'] = new Object();
keys['9'].ctr = 0;
keys['9'].char = ['w','x','y','z','9'];

var append=false;
var str='';
var timer;
var prevNum=null;
var currElementName='txtURL';

function keypad(num)
{
  var currFocusedElement = document.forms['URL'].elements[currElementName];
  if (prevNum!=null && prevNum!=num) 
	{
     append=true;
	}
  if (keys[num].ctr>keys[num].char.length-1) keys[num].ctr=0; //go back to first item in keypad
  if (append) 
	{
	keys[num].ctr=0; //go back to first item in keypad
     str=currFocusedElement.value+keys[num].char[keys[num].ctr]; 
	 
	}
  else 
	{
     str=(currFocusedElement.value.length==0) ? currFocusedElement.value=keys[num].char[keys[num].ctr]:currFocusedElement.value.substring(0,currFocusedElement.value.length-1)+keys[num].char[keys[num].ctr];
	}
  currFocusedElement.value=str;
  keys[num].ctr++;
  prevNum=num;
  //reset
  append=false;
  clearTimeout(timer);
  timer=setTimeout(function(){append=true;}, 2000);
}


//******** END OF MOBILE PHONE-STYLE KEYPAD *********

var col = 8; //number of 'cells' in a row
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
			//Move to the next key on the keyboard
			var code=document.links['c' + next].name;
			document.links['c' + next].focus();
			document.images['i' + next].src = 'Images/Keyboard/bt_focus.png';
			document.images['i' + current].src = 'Images/Keyboard/bt_nofocus.png';
			current = next;
			} 
		else if (key==13) 
			{
			//Simulate click on button elements for OK remote button
			document.forms['URL'].elements[currElementName].click();
			// v- using .click() above as this code makes problems with TV remote buttons ('OK' button makes both keyboard '13' code and click() at the same time, so the character is type twice)
			//Write the letter on the currFocusedElement field
			//var URLText = document.forms['URL'].elements[currElementName].value;
			//URLText = URLText + document.links['c' + next].name;
			//document.forms['URL'].elements[currElementName].value = URLText;
			} 
		else if (key==32) 
			{
			//spacebar
			if (!elem.focused)
				{
				//Write the letter on the currFocusedElement field
				var URLText = document.forms['URL'].elements[currElementName].value;
				URLText = URLText + document.links['c' + next].name;
				document.forms['URL'].elements[currElementName].value = URLText;
				}
			}
		else if (key==48) 
			{
			//the 0 on the remote control have been pressed
			//use the keypad function
			if (!elem.focused)
			    {
			    keypad('0');
			    }
			} 
		else if (key==49) 
			{
			//the 1 on the remote control have been pressed
			//use the keypad function
			if (!elem.focused)
			    {
			    keypad('1');
			    }
			}
		else if (key==50) 
			{
			//the 2 on the remote control have been pressed
			//use the keypad function
			if (!elem.focused)
			    {
			    keypad('2');
			    }
			}
		else if (key==51) 
			{
			//the 3 on the remote control have been pressed
			//use the keypad function
			if (!elem.focused)
			    {
			    keypad('3');
			    }
			}
		else if (key==52) 
			{
			//the 4 on the remote control have been pressed
			//use the keypad function
			if (!elem.focused)
			    {
			    keypad('4');
			    }
			}
		else if (key==53) 
			{
			//the 5 on the remote control have been pressed
			//use the keypad function
			if (!elem.focused)
			    {
			    keypad('5');
			    }
			}
		else if (key==54) 
			{
			//the 6 on the remote control have been pressed
			//use the keypad function
			if (!elem.focused)
			    {
			    keypad('6');
			    }
			}
		else if (key==55) 
			{
			//the 7 on the remote control have been pressed
			//use the keypad function
			if (!elem.focused)
			    {
			    keypad('7');
			    }
			}
		else if (key==56) 
			{
			//the 8 on the remote control have been pressed
			//use the keypad function
			if (!elem.focused)
			    {
			    keypad('8');
			    }
			}
		else if (key==57) 
			{
			//the 9 on the remote control have been pressed
			//use the keypad function
			if (!elem.focused)
			    {
			    keypad('9');
			    }
			}
		else if (key==403) 
			{
			//the red button on the remote control have been pressed
			//Search on google the content of currFocusedElement field
			SearchOnGoogle();
			}
		else if (key==405) 
			{
			//the yellow button on the remote control have been pressed
			//Load the page addressed by the currFocusedElement field
			GoToURL();
			}
		else if (key==406) 
			{
			//the blue button on the remote control have been pressed
			//I send a backspace on the currFocusedElement field
			BackSpace();
			}
		else if (key==404) 
			{
			//the green button on the remote control have been pressed
			//Switch to the MainPage
			ChangeBgColor();
			document.getElementById('MainPage').focus();
			}
		else if (key==457) 
			{
			//the info button on the remote control have been pressed
			//window.location='links.html';
			GoToNetCastLinks();
			}
		else if (key==461) 
			{
			//the back button on the remote control have been pressed
			//NetCastBack API (exits from NetCast portal menu)
			//window.NetCastBack();
			//let's get back to WebUI instead of closing NetCast service
			history.go(-1);
			}
		else if (key==1001) 
			{
			//the exit button on the remote control have been pressed
			//NetCastExit API (exits closes whole NetCast)
			window.NetCastExit();
			//different options to get back to NetCast portal menu
			//history.go(-100);
			//window.NetCastReturn(461);
			//window.NetCastBack();
			}
		}catch(Exception){}
	}
	
function DirectWriteKey(key)
	{
	//Write the letter on the currFocusedElement field
	var URLText = document.forms['URL'].elements[currElementName].value;
	URLText = URLText + key;
	document.forms['URL'].elements[currElementName].value = URLText;
	}	
	
function GoToNetCastLinks()
	{
	<?
		if [ -n "`pgrep -f run3556-proxy`" -a "$HTTP_HOST" = "127.0.0.1:88" ]
		then
		    echo "window.location='http://$HTTP_HOST/home.cgi?qURL=/mnt/browser/run3556+http://$HTTP_HOST/browser/links.html&run=Run&qUser=&qPassw=';"
		    #echo "window.location='http://127.0.0.1:88/home.cgi?qURL=%2Fmnt%2Fbrowser%2Frun3556+http%3A%2F%2F127.0.0.1%3A88%2Fbrowser%2Flinks.html&run=Run&qUser=&qPassw=';"
		else
		    echo "window.location='browser/links.html';"
		fi
	?>
	}
function GoToURL()
	{
	//Load the page addressed by the currFocusedElement field
	var URLText = document.forms['URL'].elements[currElementName].value;
	
	if (URLText == '')
		{
		//if the URL is empty, goes to the list of all Netcast Services
		document.getElementById('MainPage').src = 'http://www.nicolaottomano.it/public/lgtv/lg/links.html';
		}
	else if (URLText.slice(0,7) == 'http://' || URLText.slice(0,7) == 'file://')
		{
		document.getElementById('MainPage').src = URLText;
		}
	else
		{
		document.getElementById('MainPage').src = 'http://' + URLText;
		}
	}	


function ChangeBgColor()
	{
	//Change the page's BgColor.
	document.bgColor = '#D3D3D3';
	}
	
function BackSpace()
	{
	//I send a backspace on the currFocusedElement field
	var URLText = document.forms['URL'].elements[currElementName].value;
	document.forms['URL'].elements[currElementName].value = URLText.slice(0,URLText.length-1);
	}
	
function SearchOnGoogle()
	{
	//Search on google the content of currFocusedElement field
	var URLText = 'http://www.google.com/search?q=' + document.forms['URL'].elements[currElementName].value;
	document.getElementById('MainPage').src = URLText;
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
	
	//Resizing MainPage IFrame
	ResizeIFrame();
	
	//change page's BgColor
	document.bgColor = '#FFFFFF';
	document.getElementById('MainPage').bgColor = '#D3D3D3';
	
	elem=document.forms['URL'].elements[currElementName];
	elem.focused = false;
	elem.hasFocus = function()
	    {
	    return this.focused;
	    };
	elem.onfocus=function()
	    {
	    this.focused=true;
	    };
	    elem.onblur=function() {
		this.focused=false;
	    };
	}

	function ResizeIFrame()
		{
		 //change the height of the iframe
		 document.getElementById('MainPage').width = window.innerWidth - 270;
		 document.getElementById('MainPage').height = window.innerHeight - 20;
		}
	
	//windows.PostMessage management
	//it is necessary to bypass browsers block on cross-domain frames communication.
	window.addEventListener("message", receiveMessage, false);

	function receiveMessage(event)
		{
		if (event.data == 'FocusToYou')
			{
			//set focus on current document
			document.links['c1'].focus();
			//Change the page's BgColor.
			document.bgColor = '#FFFFFF';
			}
		return;
		}
		
	function SwitchFocusedPage()
		{
		//Change the page's BgColor.
		ChangeBgColor();
		
		//windows.PostMessage
		//it is necessary to bypass browsers block on cross-domain frames communication.
		document.getElementById('MainPage').contentWindow.postMessage('FocusToYou', '*');
		
		}
		
document.defaultAction = true;


</script>




</head>
<body bgcolor="#D3D3D3">

	<iframe id="MainPage" src="browser/mainpage.cgi" width="50%" height="100%" valign = "top" align="right" frameborder="0">
		<p>Your browser does not support iframes.</p>
	</iframe>

	<div style="position: absolute; left: 0px; top: 5px;">
		<form id="URL" name="URL">
			<font size="+2"><center><b>OpenLGTV BCM<br/>
			Internet Browser<br/></font><br/>
			Type URL or Text to Search:</b><br/></center>
			<input id="txtURL" type="textarea" style="width:263px" value=""/>
		</form>
	</div>	
	
	<div style="position: absolute; left: 0px; top: 145px;">
		<? cat include/keypad_table.html.inc ?>
	</div>
	<!-- div style="position: absolute; left: 400px; top: 480px;" -->
	<div style="position: absolute; left: -1px; top: 350px;">
		<Table Border=0 cellspacing=0>
			<tr>
				<td><img src="Images/Keyboard/tapkey.png" align="middle"></td>
			</tr>
		</Table>
	</div>
	
	<div style="position: absolute; left: 5px; top: 550px;">
		<Table Border=0 cellspacing=0>
			<tr>
				<td colspan=2>
					<a onClick="javascript:SearchOnGoogle();" href="#"><img src="Images/Keyboard/red_button.png" align="middle" Border="0" /></a>
					<b>Search on Google</b>
				</td>
			</tr>
			<tr>
				<td colspan=2>
					<a onClick='javascript:SwitchFocusedPage(); return false;' href="#"><img src="Images/Keyboard/green_button.png" align="middle" Border="0" /></a>
					<b>Switch Page</b>
				</td>
			</tr>
			<tr>
				<td>
					<a onClick="javascript:GoToURL();" href="#"><img src="Images/Keyboard/yellow_button.png" align="middle" Border="0" /></a>
					<b>Go to URL</b>
				</td>
				<td><img src="Images/Keyboard/back_button.png" align="middle" Border="0" /><b>Back</b></td>
			</tr>
			<tr>
				<td>
					<a onClick="javascript:BackSpace();" href="#"><img src="Images/Keyboard/blue_button.png" align="middle" Border="0" /></a>
					<b>Backspace</b>
				</td>
				<td><img src="Images/Keyboard/exit_button.png" align="middle" Border="0" /><b>Exit</b></td>
			</tr>
		</Table>
	</div>
</body>
</html>
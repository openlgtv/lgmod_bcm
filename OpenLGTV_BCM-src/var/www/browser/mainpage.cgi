#!/bin/haserl
content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>

<!-- Code for OpenLGTV BCM Browser by Nicola Ottomano -->
<!-- Source code released under GPL License -->

<style>
      td {
        background-repeat: no-repeat;
        background-position: center center;
        background-image: url(Images/EmptyBookmarkNoFocus.png);
      }
</style>

<script type="text/javascript">
<!--

var col = 5; //number of 'cells' in a row
var current;
var next;
document.onkeydown = check;

// ***** START BOOKMARKS MANAGEMENT *****

var Bookmark = new Array();
var txtFile = new XMLHttpRequest();
var ArrLines = new Array();
	

function CreateBookmark() {

	txtFile.open("GET", "http://<?= $HTTP_HOST ?>/user/bookmarks.inc", false);
	// v- onreadystatechange does not work on FireFox < 4.0
	txtFile.onreadystatechange = function()
		{	
		//alert(txtFile.readyState);
		//alert(txtFile.status);
		if (txtFile.readyState == 4) 
			{  // Makes sure the document is ready to parse.
			if (txtFile.status == 200 || txtFile.status == 0) 
				{  // Makes sure it's found the file.
				allText = txtFile.responseText;
				//alert(allText);
				// Split each line into an array
				ArrLines = txtFile.responseText.split("\n"); 
				}
			}
		}
	txtFile.send(null);

	for (i=0; i <= ArrLines.length; i++) 
		{ 
		Bookmark['a' + (i + 1)] = new Object();
		Bookmark['a' + (i + 1)].Address = ArrLines[i];
		}

	for (i=1; i <= ArrLines.length; i++) 
		{ 
		if (Bookmark['a' + i].Address.length != 0) 
			{ 
			var imageSrc = "http://open.thumbshots.org/image.aspx?url=" + Bookmark['a' + i].Address;
			document.getElementById('img' + i).src = imageSrc;
			var linkURL = Bookmark['a' + i].Address;
			document.getElementById('link' + i).href = linkURL;
			}
		}     
	//Set the focus on the 1st bookmark
	OnLoadSetCurrent();
}


function DeleteBookmark()
	{
	// delete bookmark replacing bookmarks.inc N row 
	top.frames["MainPage"].location = 'deletebookmark.cgi?bookmarkId=' + current;
	}
	
function SaveBookmark()
	{
	// save bookmark replacing bookmarks.inc N row 
	var URLText = top.frames["Keyboard"].document.forms['URL'].elements['txtURL'].value;
	
	if (URLText != '')
		{
		if (URLText.slice(0,7) != 'http://' && URLText.slice(0,8) != 'file:///')
			{
			URLText = 'http://' + URLText;
			}
			
		top.frames["MainPage"].location = 'savebookmark.cgi?bookmarkId=' + current + '&bookmarkURL=' + URLText;
		}
	}
	
// ***** END BOOKMARKS MANAGEMENT *****
     
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
			document.getElementById('td' + next).style.backgroundImage = 'url(Images/EmptyBookmarkFocus.png)';
			document.getElementById('td' + current).style.backgroundImage = 'url(Images/EmptyBookmarkNoFocus.png)';
			//set current=next
			current = next;
			}
		else if (key==403) 
			{
			//the red button on the remote control have been pressed
			window.location='links.html';
			}
		else if (key==404) 
			{
			//the green button on the remote control have been pressed
			//Switch to the Keyboard
			document.bgColor = '#D3D3D3';
			top.frames["Keyboard"].document.bgColor = '#FFFFFF';
			top.frames["Keyboard"].focus();
			}
		else if (key==405) 
			{
			//the yellow button on the remote control have been pressed
			//save the selected bookmark using URL written by the user
			SaveBookmark();
			}
		else if (key==406) 
			{
			//the blue button on the remote control have been pressed
			//Delete the selected bookmark
			DeleteBookmark();
			}
		else if (key==461) 
			{
			//the back button on the remote control have been pressed
			//NetCastBack API
			//window.NetCastBack();
			//let's get back to WebUI instead of closing NetCast service
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
	
function OnLoadSetCurrent()
	{
	current = 1;
	document.links['link1'].focus();
	//set TD background
	document.getElementById('td' + current).style.backgroundImage = 'url(Images/EmptyBookmarkFocus.png)';
	}	
	
document.defaultAction = true;

// -->
</script>

</head>

<!-- body bgcolor="#ffffff" onLoad="javascript:CreateBookmark();" -->
<body bgcolor="#d3d3d3" onLoad="javascript:CreateBookmark();">


<div align="center">
	<table border=0 id="BookmarksTable">
		<tr>
			<td id="td1" align="center" valign="middle" height="121px" width="160px" >
				<a id="link1" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img1" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td2" align="center" valign="middle" height="121px" width="160px" >
				<a id="link2" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img2" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td3" align="center" valign="middle" height="121px" width="160px" >
				<a id="link3" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img3" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td4" align="center" valign="middle" height="121px" width="160px" >
				<a id="link4" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img4" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td5" align="center" valign="middle" height="121px" width="160px" >
				<a id="link5" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img5" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
		</tr>
		<tr>
			<td id="td6" align="center" valign="middle" height="121px" width="160px" >
				<a id="link6" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img6" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td7" align="center" valign="middle" height="121px" width="160px" >
				<a id="link7" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img7" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td8" align="center" valign="middle" height="121px" width="160px" >
				<a id="link8" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img8" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td9" align="center" valign="middle" height="121px" width="160px" >
				<a id="link9" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img9" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td10" align="center" valign="middle" height="121px" width="160px" >
				<a id="link10" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img10" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
		</tr>
		<tr>
			<td id="td11" align="center" valign="middle" height="121px" width="160px" >
				<a id="link11" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img11" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td12" align="center" valign="middle" height="121px" width="160px" >
				<a id="link12" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img12" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td13" align="center" valign="middle" height="121px" width="160px" >
				<a id="link13" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img13" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td14" align="center" valign="middle" height="121px" width="160px" >
				<a id="link14" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img14" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td15" align="center" valign="middle" height="121px" width="160px" >
				<a id="link15" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img15" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
		</tr>
		<tr>
			<td id="td16" align="center" valign="middle" height="121px" width="160px" >
				<a id="link16" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img16" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td17" align="center" valign="middle" height="121px" width="160px" >
				<a id="link17" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img17" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td18" align="center" valign="middle" height="121px" width="160px" >
				<a id="link18" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img18" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td19" align="center" valign="middle" height="121px" width="160px" >
				<a id="link19" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img19" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td20" align="center" valign="middle" height="121px" width="160px" >
				<a id="link20" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img20" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
		</tr>
		<tr>
			<td id="td21" align="center" valign="middle" height="121px" width="160px" >
				<a id="link21" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img21" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td22" align="center" valign="middle" height="121px" width="160px" >
				<a id="link22" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img22" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td23" align="center" valign="middle" height="121px" width="160px" >
				<a id="link23" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img23" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td24" align="center" valign="middle" height="121px" width="160px" >
				<a id="link24" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img24" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td id="td25" align="center" valign="middle" height="121px" width="160px" >
				<a id="link25" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img25" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
		</tr>
	</table>
</div>
<br>
<div align="center">
		<Table Border=0 cellspacing=0>
			<tr>
				<td colspan=2>
					<a onClick="javascript:window.location='links.html';" href="#"><img src="Images/Keyboard/red_button.png" align="middle" Border="0" /></a>
					<b>NetCast services</b>
				</td>
				<td colspan=2>
					<a onClick='javascript:top.frames["Keyboard"].focus();' href="#"><img src="Images/Keyboard/green_button.png" align="middle" Border="0" /></a>
					<b>Switch Page</b>
				</td>
				<td>
					<a onClick="javascript:SaveBookmark();" href="#"><img src="Images/Keyboard/yellow_button.png" align="middle" Border="0" /></a>
					<b>Save Bookmark</b>
				</td>
				<td>
					<a onClick="javascript:DeleteBookmark();" href="#"><img src="Images/Keyboard/blue_button.png" align="middle" Border="0" /></a>
					<b>Delete Bookmark</b>
				</td>
			</tr>
		</Table>
	</div>

<body>
<html>


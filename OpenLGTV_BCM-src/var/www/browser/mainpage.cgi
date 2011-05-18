#!/bin/haserl
content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>

<!-- Code for OpenLGTV BCM Browser by Nicola Ottomano -->
<!-- Source code released under GPL License -->

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
	top.frames["MainPage"].location = 'savebookmark.cgi?bookmarkId=' + current + '&bookmarkURL=' + URLText;
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
			//Move to the next key on the keyboard
			var code=document.links['link' + next].name;
			document.links['link' + next].focus();
			current = next;
			//alert('key: '+key+' current: '+current);
			}
		else if (key==404) 
			{
			//the green button on the remote control have been pressed
			//Switch to the Keyboard
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
	}	
	
document.defaultAction = true;

// -->
</script>

</head>

<body bgcolor="#cccccc" onLoad="javascript:CreateBookmark();">


<div align="center">
	<table border=0>
		<tr>
			<td>
				<a id="link1" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img1" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link2" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img2" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link3" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img3" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link4" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img4" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link5" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img5" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
		</tr>
		<tr>
			<td>
				<a id="link6" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img6" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link7" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img7" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link8" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img8" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link9" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img9" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link10" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img10" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
		</tr>
		<tr>
			<td>
				<a id="link11" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img11" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link12" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img12" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link13" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img13" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link14" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img14" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link15" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img15" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
		</tr>
		<tr>
			<td>
				<a id="link16" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img16" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link17" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img17" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link18" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img18" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link19" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img19" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link20" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img20" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
		</tr>
		<tr>
			<td>
				<a id="link21" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img21" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link22" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img22" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link23" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img23" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
				<a id="link24" onKeyPress="javascript:setCurrent(this);return false" href="mainpage.cgi"><img id="img24" src="Images/EmptyBookmark.png" border="0" height="113px" width="150px"></a>
			</td>
			<td>
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
					<a onClick="javascript:SearchOnGoogle();" href="#"><img src="Images/Keyboard/red_button.png" align="middle" Border="0" /></a>
					<b>xxxxx</b>
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


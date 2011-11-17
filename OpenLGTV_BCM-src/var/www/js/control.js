//<!-- 
// control.js by Nicola Ottomano
// changed by xeros
// Source code released under GPL License


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
var txt_edit=0;

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

//******** MANAGING TEXTBOX INPUT AND FOCUS *********
var PageElements = new Array();

PageElements[0] = new Object();
PageElements[0].value = ['link1'];
//PageElements[0].type = ['button'];
PageElements[0].type = ['anchor'];

PageElements[1] = new Object();
PageElements[1].value = ['link2'];
PageElements[1].type = ['anchor'];

PageElements[2] = new Object();
PageElements[2].value = ['link3'];
PageElements[2].type = ['anchor'];

PageElements[3] = new Object();
PageElements[3].value = ['link4'];
PageElements[3].type = ['anchor'];

PageElements[4] = new Object();
PageElements[4].value = ['link5'];
PageElements[4].type = ['anchor'];

PageElements[5] = new Object();
PageElements[5].value = ['link6'];
PageElements[5].type = ['anchor'];

PageElements[6] = new Object();
PageElements[6].value = ['link7'];
PageElements[6].type = ['button'];

PageElements[7] = new Object();
PageElements[7].value = ['link8'];
PageElements[7].type = ['button'];

PageElements[8] = new Object();
PageElements[8].value = ['link9'];
PageElements[8].type = ['button'];

PageElements[9] = new Object();
PageElements[9].value = ['link10'];
PageElements[9].type = ['button'];

PageElements[10] = new Object();
PageElements[10].value = ['link11'];
PageElements[10].type = ['button'];

PageElements[11] = new Object();
PageElements[11].value = ['link12'];
PageElements[11].type = ['button'];

PageElements[12] = new Object();
PageElements[12].value = ['link13'];
PageElements[12].type = ['button'];

PageElements[13] = new Object();
PageElements[13].value = ['link14'];
PageElements[13].type = ['button'];

PageElements[14] = new Object();
PageElements[14].value = ['link15'];
PageElements[14].type = ['button'];

PageElements[15] = new Object();
PageElements[15].value = ['txtURL'];
PageElements[15].type = ['txt'];
PageElements[15].focused=false;

PageElements[16] = new Object();
PageElements[16].value = ['txtUser'];
PageElements[16].type = ['txt'];
PageElements[16].focused=false;

PageElements[17] = new Object();
PageElements[17].value = ['txtPassw'];
PageElements[17].type = ['txt'];
PageElements[17].focused=false;

PageElements[18] = new Object();
PageElements[18].value = ['txtPath'];
PageElements[18].type = ['txt'];
PageElements[18].focused=false;

PageElements[19] = new Object();
PageElements[19].value = ['radio1'];
PageElements[19].type = ['radio'];

PageElements[20] = new Object();
PageElements[20].value = ['check1'];
PageElements[20].type = ['checkbox'];

PageElements[21] = new Object();
PageElements[21].value = ['check2'];
PageElements[21].type = ['checkbox'];

PageElements[22] = new Object();
PageElements[22].value = ['check3'];
PageElements[22].type = ['checkbox'];

PageElements[23] = new Object();
PageElements[23].value = ['check4'];
PageElements[23].type = ['checkbox'];

PageElements[24] = new Object();
PageElements[24].value = ['check5'];
PageElements[24].type = ['checkbox'];

PageElements[25] = new Object();
PageElements[25].value = ['check6'];
PageElements[25].type = ['checkbox'];

PageElements[26] = new Object();
PageElements[26].value = ['check7'];
PageElements[26].type = ['checkbox'];

PageElements[27] = new Object();
PageElements[27].value = ['check8'];
PageElements[27].type = ['checkbox'];

PageElements[28] = new Object();
PageElements[28].value = ['check9'];
PageElements[28].type = ['checkbox'];

PageElements[29] = new Object();
PageElements[29].value = ['check10'];
PageElements[29].type = ['checkbox'];

PageElements[30] = new Object();
PageElements[30].value = ['check11'];
PageElements[30].type = ['checkbox'];

PageElements[31] = new Object();
PageElements[31].value = ['check12'];
PageElements[31].type = ['checkbox'];

PageElements[32] = new Object();
PageElements[32].value = ['check13'];
PageElements[32].type = ['checkbox'];

PageElements[33] = new Object();
PageElements[33].value = ['check14'];
PageElements[33].type = ['checkbox'];

PageElements[34] = new Object();
PageElements[34].value = ['check15'];
PageElements[34].type = ['checkbox'];

PageElements[35] = new Object();
PageElements[35].value = ['check16'];
PageElements[35].type = ['checkbox'];

PageElements[36] = new Object();
PageElements[36].value = ['check17'];
PageElements[36].type = ['checkbox'];

var currElementIndex;
var currElementName;

//Background color of current focused control parent.
//var ParentFocusColor = 'yellow';
//var ParentFocusColor = 'green';
var ParentFocusColor = '#00FF00';
var ParentUnfocusColor = 'white';
var ParentEditColor = 'cyan';
var ParentColor;

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
		if (PageElements[currElementIndex].type == 'txt')
			{
			switch(key)
				{
				case 37: next = current - 1; break; //left
				case 38: next = current - col; break; //up
				case 39: next = (1*current) + 1; break; //right
				case 40: next = (1*current) + col; break; //down
				}
			}
		if (key==37|key==38|key==39|key==40)
			{
			
			if (PageElements[currElementIndex].type == 'txt' & txt_edit == '1')
				{
				//Move to the next key on the keyboard
				var code=document.links['c' + next].name;
				document.links['c' + next].focus();
				//document.images['i' + next].src = 'Images/Keyboard/' + next + 'b.png';
				document.images['i' + next].src = 'Images/Keyboard/bt_focus.png';
				//document.images['i' + current].src = 'Images/Keyboard/' + current + 'n.png';
				document.images['i' + current].src = 'Images/Keyboard/bt_nofocus.png';
				current = next;
				}
			else
				{
				if (((key==37)&(PageElements[currElementIndex].type != 'radio'))|key==38)
					{
					    PrevControl();
					    return false;
					}
				if (((key==39)&(PageElements[currElementIndex].type != 'radio'))|key==40)
					{
					    NextControl();
					    return false;
					}
				}
			} 
		else if (key==13|key==10) 
			{
			//Simulate click on button elements for OK remote button
			currElementName=PageElements[currElementIndex].value;
			if ((PageElements[currElementIndex].type == 'button')|(PageElements[currElementIndex].type == 'checkbox'))
				{
				    //document.forms['URL'].elements[currElementName].click();
				    document.getElementById(currElementName).click();
				}
			else if (PageElements[currElementIndex].type == 'txt' & txt_edit == '0')
				{
				    d = document.getElementById(currElementName + 'Parent');
				    d.style.backgroundColor=ParentEditColor;
				    txt_edit=1;
				}
			else if (PageElements[currElementIndex].type == 'anchor')
				{
				    window.location=document.getElementById(currElementName).href;
				}
			//else if (PageElements[currElementIndex].type == 'checkbox')
			//	{
			//	    document.forms['URL'].elements[currElementName].click();
			//	}
			}
		else if (key==32) 
			{
			//spacebar
			if (!PageElements[currElementIndex].focused)
			    {
			    if (PageElements[currElementIndex].type == 'button')
				{
				    document.forms['URL'].elements[currElementName].click();
				} else { 
				    //Write the letter on the currFocusedElement field
				    var URLText = document.forms['URL'].elements[currElementName].value;
				    URLText = URLText + document.links['c' + next].name;
				    document.forms['URL'].elements[currElementName].value = URLText;
				}
			    }
			}
		else if (key==48) 
			{
			//the 0 on the remote control have been pressed
			//use the keypad function
			//check if the input field is has focus (dirty fix for typing numbers into textarea input fields from PC keyboard)
			if (!PageElements[currElementIndex].focused)
			    {
			    keypad('0');
			    }
			} 
		else if (key==49) 
			{
			//the 1 on the remote control have been pressed
			//use the keypad function
			if (!PageElements[currElementIndex].focused)
			    {
			    keypad('1');
			    }
			}
		else if (key==50) 
			{
			//the 2 on the remote control have been pressed
			//use the keypad function
			if (!PageElements[currElementIndex].focused)
			    {
			    keypad('2');
			    }
			}
		else if (key==51) 
			{
			//the 3 on the remote control have been pressed
			//use the keypad function
			if (!PageElements[currElementIndex].focused)
			    {
			    keypad('3');
			    }
			}
		else if (key==52) 
			{
			//the 4 on the remote control have been pressed
			//use the keypad function
			if (!PageElements[currElementIndex].focused)
			    {
			    keypad('4');
			    }
			}
		else if (key==53) 
			{
			//the 5 on the remote control have been pressed
			//use the keypad function
			if (!PageElements[currElementIndex].focused)
			    {
			    keypad('5');
			    }
			}
		else if (key==54) 
			{
			//the 6 on the remote control have been pressed
			//use the keypad function
			if (!PageElements[currElementIndex].focused)
			    {
			    keypad('6');
			    }
			}
		else if (key==55) 
			{
			//the 7 on the remote control have been pressed
			//use the keypad function
			if (!PageElements[currElementIndex].focused)
			    {
			    keypad('7');
			    }
			}
		else if (key==56) 
			{
			//the 8 on the remote control have been pressed
			//use the keypad function
			if (!PageElements[currElementIndex].focused)
			    {
			    keypad('8');
			    }
			}
		else if (key==57) 
			{
			//the 9 on the remote control have been pressed
			//use the keypad function
			if (!PageElements[currElementIndex].focused)
			    {
			    keypad('9');
			    }
			}
		else if (key==403) 
			{
			//the red button on the remote control have been pressed
			//Switch to the previous control
			PrevControl();
			}
		else if (key==404) 
			{
			//the green button on the remote control have been pressed
			//Switch to the next control
			NextControl();
			}
		else if (key==405) 
			{
			//the yellow button on the remote control have been pressed
			//Save form
			SaveForm();
			}
		else if (key==406) 
			{
			//the blue button on the remote control have been pressed
			//I send a backspace on the currFocusedElement field
			BackSpace();
			}
		else if (key==413) 
			{
			//the stop button on the remote control have been pressed
			//Reboot TV
			window.location='home.cgi?qURL=reboot&run=Run';
			}
		else if (key==457) 
			{
			//the info button on the remote control have been pressed
			//go to NetCast links
			    if(typeof GoToNetCastLinks == 'function')
			    {
				GoToNetCastLinks();
			    }
			    else
			    {
				window.location='browser/links.html';
			    }
			}
		else if (key==461|key==27) 
			{
			//the back button on the remote control or ESC have been pressed
			if (PageElements[currElementIndex].type == 'txt' & txt_edit == '1')
				{
				    d = document.getElementById(currElementName + 'Parent');
				    d.style.backgroundColor=ParentFocusColor;
				    txt_edit=0;
				}
			else
				{
				//NetCastBack API (exits from NetCast portal menu)
				//window.NetCastBack();
				history.go(-1);
				}
			}
		else if (key==1001) 
			{
			//the exit button on the remote control have been pressed
			//NetCastExit API (closes whole NetCast)
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
	if (PageElements[currElementIndex].type == 'txt')
		{
		var URLText = document.forms['URL'].elements[currElementName].value;
		URLText = URLText + key;
		document.forms['URL'].elements[currElementName].value = URLText;
		}
	}

function SaveForm()
	{
	//Save the settings in current page
	document.forms['URL'].submit();
	//alert("Save stub.");
	}

function BackSpace()
	{
	//alert(currElementIndex);
	if (PageElements[currElementIndex].type == 'txt')
		{
		//I send a backspace on the currFocusedElement field
		var URLText = document.forms['URL'].elements[currElementName].value;
		document.forms['URL'].elements[currElementName].value = URLText.slice(0,URLText.length-1);
		}
	else
		{
		if (window.location.pathname=='/mount.cgi')
			{
			var currentId=currElementIndex-9;
			if (currentId>0)
				{
				window.location='mount.cgi?action=remove&id=' + currentId;
				}
			}
		}
	}

function PrevControl()
	{
	//Function that move to previous control
	//move to last control index when current one is first
	if (currElementIndex == 0)
		currElementIndex=37;
	if (currElementIndex > 0)
		{
		//Change the background color of current control
		d = document.getElementById(currElementName + 'Parent');
		//d.style.backgroundColor=ParentUnfocusColor;
		d.style.backgroundColor=ParentColor;
		//move to previous control
		currElementIndex-=1;
		currElementName=PageElements[currElementIndex].value;
		checkElementMinus(currElementIndex);
		
		if (PageElements[currElementIndex].type == 'radio') 
			{
			//If we are on a radio button, set the focus on the current control.
			document.forms['URL'].elements[currElementName][0].focus();
			}
		else if (PageElements[currElementIndex].type == 'checkbox') 
			{
			//If we are on a checkbox, set the focus on the current control.
			document.forms['URL'].elements[currElementName].focus();
			}
			
		//Change the background color of selected control
		d = document.getElementById(currElementName + 'Parent');
		ParentColor=d.style.backgroundColor;
		d.style.backgroundColor=ParentFocusColor;
		}
	txt_edit=0;
	}

function NextControl()
	{
	//currElementName=PageElements[currElementIndex].value;
	
	//Function that move to next control
	if (currElementIndex < PageElements.length-1)
		{
		
		//Change the background color of current control
		d = document.getElementById(currElementName + 'Parent');
		//d.style.backgroundColor=ParentUnfocusColor;
		d.style.backgroundColor=ParentColor;
		//move to next control
		currElementIndex+=1;
		currElementName=PageElements[currElementIndex].value;
		checkElementPlus(currElementIndex);
		
		if (PageElements[currElementIndex].type == 'radio') 
			{
			//If we are on a radio button, set the focus on the current control.
			document.forms['URL'].elements[currElementName][0].focus();
			}
		else if (PageElements[currElementIndex].type == 'checkbox') 
			{
			//If we are on a checkbox, set the focus on the current control.
			document.forms['URL'].elements[currElementName].focus();
			}
			
		//Change the background color of selected control
		d = document.getElementById(currElementName + 'Parent');
		ParentColor=d.style.backgroundColor;
		d.style.backgroundColor=ParentFocusColor;
		}
	txt_edit=0;
	}

function setCurrent(element)
	{
	var string = element.id;
	current = string.slice(1,string.length);
	}

function checkElementPlus(elementIndex)
{
	currElementIndex=elementIndex;
	prevElementIndex=elementIndex-1;
	currElementName=PageElements[currElementIndex].value;
	//Check if currElement exists, if not then go to next one until finds the one that exists
	//document.getElementById(currElementName) works for elements which are not part of HTML form also
	//document.forms['URL'].elements[currElementName]) is needed for checkboxes and radio buttons as these do not have their own link* IDs
	if ((!document.getElementById(currElementName))&&(!document.forms['URL'].elements[currElementName])) {
		do {
		    currElementIndex+=1;
		    currElementName=PageElements[currElementIndex].value;
		} while ((!document.getElementById(currElementName))&&(!document.forms['URL'].elements[currElementName])&&(currElementIndex < PageElements.length-1));
	}
	if ((!document.getElementById(currElementName))&&(!document.forms['URL'].elements[currElementName])) {
	    currElementIndex=0;
	}
	currElementName=PageElements[currElementIndex].value;
}
function checkElementMinus(elementIndex)
{
	currElementIndex=elementIndex;
	currElementName=PageElements[currElementIndex].value;
	//Check if currElement exists, if not then go to previous one until finds the one that exists
	if ((!document.getElementById(currElementName))&&(!document.forms['URL'].elements[currElementName])&&(currElementIndex > 0)) {
		do {
		    currElementIndex-=1;
		    currElementName=PageElements[currElementIndex].value;
		} while ((!document.getElementById(currElementName))&&(!document.forms['URL'].elements[currElementName])&&(currElementIndex > 0));
	}
	//Check if currElement exists already, if not then go to 
	if ((!document.getElementById(currElementName))&&(!document.forms['URL'].elements[currElementName])) {
	    currElementIndex=0;
	    currElementName=PageElements[currElementIndex].value;
	    checkElementPlus(currElementIndex);
	}
	currElementName=PageElements[currElementIndex].value;
}
function sleep(milliseconds) 
{
	var startTime = new Date().getTime();
	for (var i = 0; i < 1e7; i++) {
	    if ((new Date().getTime() - startTime) > milliseconds){
		break;
	    }
	}
}
function OnLoadSetCurrent()
{
	//Setting the position of first button of the on-screen keyboard
	current = 1;
	document.links['c1'].focus();
	
	//Setting the current input control 
	//currElementIndex=0;
	currElementIndex=6;
	checkElementPlus(currElementIndex);
	currElementName=PageElements[currElementIndex].value;
	//Change the background color of selected control
	d = document.getElementById(currElementName + 'Parent');
	ParentColor=d.style.backgroundColor;
	d.style.backgroundColor=ParentFocusColor;
	if (document.getElementById('spanSAVED')) {
	    document.getElementById('spanSAVED').innerHTML='SETTINGS SAVED !!!';
	    //sleep(300);
	    //document.getElementById('spanSAVED').innerHTML='-';
	}
}

function hasFocus(elementIndex)
{
	return this.focused;
}
	document.defaultAction = true;
	//-->

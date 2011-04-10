<!-- Source code released under GPL License -->
<!-- Nicola Ottomano LG TV -->

<SCRIPT language="JavaScript">
	<!--
	// On-screen keyboard images preload
	if (document.images)
	{
	  preload_image_object = new Image();
	  // set image url
	  image_url = new Array();
	  image_url[0] = "Images/Keyboard/1b.png";
	  image_url[1] = "Images/Keyboard/2b.png";
	  image_url[2] = "Images/Keyboard/3b.png";
	  image_url[3] = "Images/Keyboard/4b.png";
	  image_url[4] = "Images/Keyboard/5b.png";
	  image_url[5] = "Images/Keyboard/6b.png";
	  image_url[6] = "Images/Keyboard/7b.png";
	  image_url[7] = "Images/Keyboard/8b.png";
	  image_url[8] = "Images/Keyboard/9b.png";
	  image_url[9] = "Images/Keyboard/10b.png";
	  image_url[10] = "Images/Keyboard/11b.png";
	  image_url[11] = "Images/Keyboard/12b.png";
	  image_url[12] = "Images/Keyboard/13b.png";
	  image_url[13] = "Images/Keyboard/14b.png";
	  image_url[14] = "Images/Keyboard/15b.png";
	  image_url[15] = "Images/Keyboard/16b.png";
	  image_url[16] = "Images/Keyboard/17b.png";
	  image_url[17] = "Images/Keyboard/18b.png";
	  image_url[18] = "Images/Keyboard/19b.png";
	  image_url[19] = "Images/Keyboard/20b.png";
	  image_url[20] = "Images/Keyboard/21b.png";
	  image_url[21] = "Images/Keyboard/22b.png";
	  image_url[22] = "Images/Keyboard/23b.png";
	  image_url[23] = "Images/Keyboard/24b.png";
	  image_url[24] = "Images/Keyboard/25b.png";
	  image_url[25] = "Images/Keyboard/26b.png";
	  image_url[26] = "Images/Keyboard/27b.png";
	  image_url[27] = "Images/Keyboard/28b.png";
	  image_url[28] = "Images/Keyboard/29b.png";
	  image_url[29] = "Images/Keyboard/30b.png";
	  image_url[30] = "Images/Keyboard/31b.png";
	  image_url[31] = "Images/Keyboard/32b.png";
	  image_url[32] = "Images/Keyboard/33b.png";
	  image_url[33] = "Images/Keyboard/34b.png";
	  image_url[34] = "Images/Keyboard/35b.png";
	  image_url[35] = "Images/Keyboard/36b.png";
	  image_url[36] = "Images/Keyboard/37b.png";
	  image_url[37] = "Images/Keyboard/38b.png";
	  image_url[38] = "Images/Keyboard/39b.png";
	  image_url[39] = "Images/Keyboard/40b.png";
	  image_url[40] = "Images/Keyboard/41b.png";
	  image_url[41] = "Images/Keyboard/42b.png";
	  image_url[42] = "Images/Keyboard/43b.png";
	  image_url[43] = "Images/Keyboard/44b.png";
	  image_url[44] = "Images/Keyboard/45b.png";
	  image_url[45] = "Images/Keyboard/46b.png";
	  image_url[46] = "Images/Keyboard/47b.png";
	  image_url[47] = "Images/Keyboard/48b.png";

	   var i = 0;
	   for(i=0; i<=47; i++) 
		 preload_image_object.src = image_url[i];
	}

	//-->
<!--

//******** MOBILE PHONE-STYLE KEYPAD *********
var keys = new Array();

keys['0'] = new Object();
keys['0'].ctr = 0;
keys['0'].char = [' ','0'];

keys['1'] = new Object();
keys['1'].ctr = 0;
keys['1'].char = ['.',':','/','1',',','@','\\','$','%','#'];

keys['2'] = new Object();
keys['2'].ctr = 0;
keys['2'].char = ['a','b','c','2'];

keys['3'] = new Object();
keys['3'].ctr = 0;
keys['3'].char = ['d','e','f','3'];

keys['4'] = new Object();
keys['4'].ctr = 0;
keys['4'].char = ['g','h','i','4'];

keys['5'] = new Object();
keys['5'].ctr = 0;
keys['5'].char = ['j','k','l','5'];

keys['6'] = new Object();
keys['6'].ctr = 0;
keys['6'].char = ['m','n','o','6'];

keys['7'] = new Object();
keys['7'].ctr = 0;
keys['7'].char = ['p','q','r','s','7'];

keys['8'] = new Object();
keys['8'].ctr = 0;
keys['8'].char = ['t','u','v','8'];

keys['9'] = new Object();
keys['9'].ctr = 0;
keys['9'].char = ['w','x','y','z','9'];

var append=false;
var str='';
var timer;
var prevNum=null;

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
PageElements[0].value = ['txtURL'];
PageElements[0].type = ['txt'];

PageElements[1] = new Object();
PageElements[1].value = ['txtUser'];
PageElements[1].type = ['txt'];

PageElements[2] = new Object();
PageElements[2].value = ['txtPassw'];
PageElements[2].type = ['txt'];

PageElements[3] = new Object();
PageElements[3].value = ['radio1'];
PageElements[3].type = ['radio'];

PageElements[4] = new Object();
PageElements[4].value = ['check1'];
PageElements[4].type = ['checkbox'];

PageElements[5] = new Object();
PageElements[5].value = ['check2'];
PageElements[5].type = ['checkbox'];

PageElements[6] = new Object();
PageElements[6].value = ['check3'];
PageElements[6].type = ['checkbox'];


var currElementIndex;
var currElementName;

//Background color of current focused control parent.
var ParentFocusColor = 'yellow';
var ParentUnfocusColor = 'white';


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
			
			if (PageElements[currElementIndex].type == 'txt')
				{
				//Move to the next key on the keyboard
				var code=document.links['c' + next].name;
				document.links['c' + next].focus();
				document.images['i' + next].src = 'Images/Keyboard/' + next + 'b.png';
				document.images['i' + current].src = 'Images/Keyboard/' + current + 'n.png';
				current = next;
				}
			}
		else if (key==13) 
			{
			//Write the letter on the currFocusedElement field
			/*
			var URLText = document.forms['URL'].elements[currElementName].value;
			URLText = URLText + document.links['c' + next].name;
			document.forms['URL'].elements[currElementName].value = URLText;
			*/
			} 
		else if (key==48) 
			{
			//the 0 on the remote control have been pressed
			//use the keypad function
			keypad('0');
			} 
		else if (key==49) 
			{
			//the 1 on the remote control have been pressed
			//use the keypad function
			keypad('1');
			}
		else if (key==50) 
			{
			//the 2 on the remote control have been pressed
			//use the keypad function
			keypad('2');
			}
		else if (key==51) 
			{
			//the 3 on the remote control have been pressed
			//use the keypad function
			keypad('3');
			}
		else if (key==52) 
			{
			//the 4 on the remote control have been pressed
			//use the keypad function
			keypad('4');
			}
		else if (key==53) 
			{
			//the 5 on the remote control have been pressed
			//use the keypad function
			keypad('5');
			}
		else if (key==54) 
			{
			//the 6 on the remote control have been pressed
			//use the keypad function
			keypad('6');
			}
		else if (key==55) 
			{
			//the 7 on the remote control have been pressed
			//use the keypad function
			keypad('7');
			}
		else if (key==56) 
			{
			//the 8 on the remote control have been pressed
			//use the keypad function
			keypad('8');
			}
		else if (key==57) 
			{
			//the 9 on the remote control have been pressed
			//use the keypad function
			keypad('9');
			}
		else if (key==403) 
			{
			//the red button on the remote control have been pressed
			//Switch to the previous control
			PrevControl();
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
		else if (key==404) 
			{
			//the green button on the remote control have been pressed
			//Switch to the next control
			NextControl();
			}
		else if (key==461) 
			{
			//the back button on the remote control have been pressed
			//NetCastBack API
			window.NetCastBack();
			}
		else if (key==1000) 
			{
			//the exit button on the remote control have been pressed
			//NetCastExit API
			window.NetCastExit();
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
	
function SaveForm()
	{
	//Save the settings in current page
	alert("Save stub.");
	}	

function BackSpace()
	{
	//I send a backspace on the currFocusedElement field
	var URLText = document.forms['URL'].elements[currElementName].value;
	document.forms['URL'].elements[currElementName].value = URLText.slice(0,URLText.length-1);
	}
		
	
function PrevControl()
	{
	//Function that move to previous control
	if (currElementIndex > 0)
		{
		
		//Change the background color of current control
		d = document.getElementById(currElementName + 'Parent');
		d.style.backgroundColor=ParentUnfocusColor;
		
		//move to previous control
		currElementIndex-=1;
		currElementName=PageElements[currElementIndex].value;
		
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
		d.style.backgroundColor=ParentFocusColor;
		}
	
	}	
	
function NextControl()
	{
	//Function that move to next control
	if (currElementIndex < PageElements.length-1)
		{
		
		//Change the background color of current control
		d = document.getElementById(currElementName + 'Parent');
		d.style.backgroundColor=ParentUnfocusColor;
		
		//move to next control
		currElementIndex+=1;
		currElementName=PageElements[currElementIndex].value;
		
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
		d.style.backgroundColor=ParentFocusColor;
		}
	
	}	

function setCurrent(element)
	{
	var string = element.id;
	current = string.slice(1,string.length);
	}
	
function OnLoadSetCurrent()
	{
	//Setting the position of first button of the on-screen keyboard
	current = 1;
	document.links['c1'].focus();
	
	//Setting the current input control 
	currElementIndex=0;
	currElementName=PageElements[currElementIndex].value;
	//Change the background color of selected control
	d = document.getElementById(currElementName + 'Parent');
	d.style.backgroundColor=ParentFocusColor;
	}	
	
	document.defaultAction = true;
	//-->
</script>

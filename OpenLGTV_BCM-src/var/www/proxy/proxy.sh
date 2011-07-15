#!/bin/ash
# OpenLGTV BCM script proxy.sh by xeros
# JavaScript code by nicola_12345
# Proxy script for JavaScript code injection
# Source code released under GPL License

# it's still better to set web browser max connections to 1 to minimalize risk of connection drops

export wait_time=4
export connect_port=80

for linex in request host line3 line4 line5 line6 line7 line8 line9 line10 line11 line12
do
    read -t 1 $linex
done

#connect_to=`echo $host | grep 'Host:' | awk '{print $2}' | sed -e 's#http://##g' -e 's#/##g' -e 's#?.*##g' | tr -d '\r'`
#connect_to=`echo $host | awk '{print $2}' | tr -d '\r'`
connect_to=`/bin/echo -e "$host\n$line3\n$line4" | grep 'Host:' | awk '{print $2}' | sed -e 's#http://##g' -e 's#/##g' -e 's#?.*##g' | tr -d '\r'`

echo "ID $id CONNECT $connect_to" >&2

#/bin/echo -e "$request\n$host\n$line3\n$line4\n$line5\n$line6\n$line7\n$line8\n$line9\n$line10\n$line11\n$line12\n\r\n" | sed -e 's#^GET http://[A-Za-z0-9\.\-]*/\(.*\)#GET /\1#g' -e 's/\(Accept-Encoding:\).*/\1/g' | tee -a $log | busybox nc -w2 $connect_to 80 | tee -a $log
/bin/echo -e "$request\n$host\n$line3\n$line4\n$line5\n$line6\n$line7\n$line8\n$line9\n$line10\n$line11\n$line12\n\r\n" | \
    busybox sed  \
	-e 's#^GET http://[A-Za-z0-9\.\-]*/\(.*\)#GET /\1#g' \
	-e 's#^POST http://[A-Za-z0-9\.\-]*/\(.*\)#POST /\1#g' \
	-e 's#HTTP/1.1#HTTP/1.0#g' \
	-e 's/\(Accept-Encoding:\).*/\1 identity/g' \
	-e 's/\(Connection:\).*/\1 close/g' | \
    busybox nc -w$wait_time $connect_to $connect_port | \
    busybox sed \
	-e 's/\(Content-Length:\).*/\1/' \
	-e 's#<[Ii][Nn][Pp][Uu][Tt]#<INPUT onKeyPress="return false;"#g' \
	-e "s#<[Hh][Ee][Aa][Dd]>#<HEAD>\n\
    	<script type='text/javascript'>\n\
	//******** MOBILE PHONE-STYLE KEYPAD *********\n\
	var keys = new Array();\n\
\n\
	keys['0'] = new Object();\n\
	keys['0'].ctr = 0;\n\
	keys['0'].char = [' ','0'];\n\
\n\
	keys['1'] = new Object();\n\
	keys['1'].ctr = 0;\n\
	keys['1'].char = ['.',':','/','1',',','@','\\\\\\\','\$','%','\#'];\n\
\n\
	keys['2'] = new Object();\n\
	keys['2'].ctr = 0;\n\
	keys['2'].char = ['a','b','c','2'];\n\
\n\
	keys['3'] = new Object();\n\
	keys['3'].ctr = 0;\n\
	keys['3'].char = ['d','e','f','3'];\n\
\n\
	keys['4'] = new Object();\n\
	keys['4'].ctr = 0;\n\
	keys['4'].char = ['g','h','i','4'];\n\
\n\
	keys['5'] = new Object();\n\
	keys['5'].ctr = 0;\n\
	keys['5'].char = ['j','k','l','5'];\n\
\n\
	keys['6'] = new Object();\n\
	keys['6'].ctr = 0;\n\
	keys['6'].char = ['m','n','o','6'];\n\
\n\
	keys['7'] = new Object();\n\
	keys['7'].ctr = 0;\n\
	keys['7'].char = ['p','q','r','s','7'];\n\
\n\
	keys['8'] = new Object();\n\
	keys['8'].ctr = 0;\n\
	keys['8'].char = ['t','u','v','8'];\n\
\n\
	keys['9'] = new Object();\n\
	keys['9'].ctr = 0;\n\
	keys['9'].char = ['w','x','y','z','9'];\n\
\n\
	var append=false;\n\
	var str='';\n\
	var timer;\n\
	var prevNum=null;\n\
\n\
	function keypad(num)\n\
	{\n\
	  var currFocusedElement = document.activeElement;\n\
	  if (currFocusedElement.type == 'text' || currFocusedElement.type == 'textarea')\n\
		  {\n\
		  if (prevNum!=null \&\& prevNum!=num)\n\
			{\n\
			 append=true;\n\
			}\n\
		  if (keys[num].ctr>keys[num].char.length-1) keys[num].ctr=0; //go back to first item in keypad\n\
		  if (append) \n\
			{\n\
			keys[num].ctr=0; //go back to first item in keypad\n\
			str=currFocusedElement.value+keys[num].char[keys[num].ctr];\n\
			\
			}\n\
		  else\n\
			{\n\
			 //str=(currFocusedElement.value.length==0) ? currFocusedElement.value=keys[num].char[keys[num].ctr]:currFocusedElement.value.substring(0,currFocusedElement.value.length-1)+keys[num].char[keys[num].ctr];\n\
			 str=(currFocusedElement.value.length==0) ? currFocusedElement.value=keys[num].char[keys[num].ctr]:currFocusedElement.value.substring(0,currFocusedElement.value.length-1)+keys[num].char[keys[num].ctr];\n\
			}\n\
		  currFocusedElement.value=str;\n\
		  keys[num].ctr++;\n\
		  prevNum=num;\n\
		  //reset\n\
		  append=false;\n\
		  clearTimeout(timer);\n\
		  timer=setTimeout(function(){append=true;}, 2000);\n\
		  }\n\
	}\n\
\n\
	//******** END OF MOBILE PHONE-STYLE KEYPAD *********\n\
\n\
	function check(e)\n\
		{\n\
		if (!e) var e = window.event;\n\
		(e.keyCode) ? key = e.keyCode : key = e.which;\n\
		try\n\
			{\n\
				switch(key)\n\
				{\n\
				/*\n\
				case 37: next = current - 1; break; //left\n\
				case 38: next = current - col; break; //up\n\
				case 39: next = (1*current) + 1; break; //right\n\
				case 40: next = (1*current) + col; break; //down\n\
				*/\n\
				}\n\
			if (key==37|key==38|key==39|key==40)\n\
				{\n\
			\n\
				//Move to the next key on the keyboard\n\
				/*\n\
				var code=document.links['c' + next].name;\n\
				document.links['c' + next].focus();\n\
				document.images['i' + next].src = 'Images/Keyboard/' + next + 'b.png';\n\
				document.images['i' + current].src = 'Images/Keyboard/' + current + 'n.png';\n\
				current = next;\n\
				*/\n\
				}\n\
			else if (key==13)\n\
				{\n\
				//Write the letter on the currFocusedElement field\n\
				/*\n\
				var URLText = document.forms['URL'].elements[currElementName].value;\n\
				URLText = URLText + document.links['c' + next].name;\n\
				document.forms['URL'].elements[currElementName].value = URLText;\n\
				*/\n\
				}\n\
			else if (key==48)\n\
				{\n\
				//the 0 on the remote control have been pressed\n\
				//use the keypad function\n\
				keypad('0');\n\
				}\n\
			else if (key==49)\n\
				{\n\
				//the 1 on the remote control have been pressed\n\
				//use the keypad function\n\
				keypad('1');\n\
				}\n\
			else if (key==50)\n\
				{\n\
				//the 2 on the remote control have been pressed\n\
				//use the keypad function\n\
				keypad('2');\n\
				}\n\
			else if (key==51)\n\
				{\n\
				//the 3 on the remote control have been pressed\n\
				//use the keypad function\n\
				keypad('3');\n\
				}\n\
			else if (key==52)\n\
				{\n\
				//the 4 on the remote control have been pressed\n\
				//use the keypad function\n\
				keypad('4');\n\
				}\n\
			else if (key==53)\n\
				{\n\
				//the 5 on the remote control have been pressed\n\
				//use the keypad function\n\
				keypad('5');\n\
				}\n\
			else if (key==54)\n\
				{\n\
				//the 6 on the remote control have been pressed\n\
				//use the keypad function\n\
				keypad('6');\n\
				}\n\
			else if (key==55)\n\
				{\n\
				//the 7 on the remote control have been pressed\n\
				//use the keypad function\n\
				keypad('7');\n\
				}\n\
			else if (key==56)\n\
				{\n\
				//the 8 on the remote control have been pressed\n\
				//use the keypad function\n\
				keypad('8');\n\
				}\n\
			else if (key==57)\n\
				{\n\
				//the 9 on the remote control have been pressed\n\
				//use the keypad function\n\
				keypad('9');\n\
				}\n\
			else if (key==403)\n\
				{\n\
				//the red button on the remote control have been pressed\n\
				//Search on google the content of currFocusedElement field\n\
				//SearchOnGoogle();\n\
				}\n\
			else if (key==405)\n\
				{\n\
				//the yellow button on the remote control have been pressed\n\
				//Load the page addressed by the currFocusedElement field\n\
				//GoToURL();\n\
				}\n\
			else if (key==406)\n\
				{\n\
				//the blue button on the remote control have been pressed\n\
				//I send a backspace on the currFocusedElement field\n\
				BackSpace();\n\
				}\n\
			else if (key==404)\n\
				{\n\
				//the green button on the remote control have been pressed\n\
				//Switch to the MainPage\n\
				top.frames[\"MainPage\"].focus();\n\
				}\n\
			else if (key==461)\n\
				{\n\
				//the back button on the remote control have been pressed\n\
				//NetCastBack API\n\
				window.NetCastBack();\n\
				}\n\
			else if (key==1001)\n\
				{\n\
				//the exit button on the remote control have been pressed\n\
				//NetCastExit API\n\
				window.NetCastExit();\n\
				}\n\
			}catch(Exception){}\n\
		}\n\
\n\
document.onkeydown = check;\n\
//window.onload = OnLoadSetCurrent;\n\
\n\
	function BackSpace()\n\
		{\n\
		//I send a backspace on the currFocusedElement field\n\
		var str = document.activeElement.value;\n\
		document.activeElement.value = str.slice(0,str.length-1);\n\
		}\n\
		\n\
		document.defaultAction = true;\n\
	</script>\n\
    #"

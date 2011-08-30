#!/bin/ash
# OpenLGTV BCM script proxy.sh by xeros
# JavaScript code by nicola_12345
# Proxy script for JavaScript code injection
# Source code released under GPL License

# those vars should be set by proxy-start.sh or via env var in cmdline for testing
#[ -z "$proxy_wait_time" ]   && proxy_wait_time=4
#[ -z "$proxy_wait_time" ]    && proxy_wait_time=8
[ -z "$proxy_wait_time" ]    && proxy_wait_time=6
[ -z "$proxy_connect_port" ] && proxy_connect_port=80
[ -z "$proxy_log_file" ]     && proxy_log_file=/var/log/proxy.log

# for proxy testing on PC
#[ -z "$awk" ]               && awk="busybox awk"
[ -z "$awk" ]                && awk=awk
[ -z "$sed" ]                && sed=sed
[ -z "$nc" ]                 && nc=nc

read_lines="request host line3 line4 line5 line6 line7 line8 line9 line10 line11 line12 line13 line14 line15 line16 line17 line18 line19 line20"

#for linex in request host line3 line4 line5 line6 line7 line8 line9 line10 line11 line12
for linex in `eval echo $read_lines`
do
    read -t 1 $linex
    content=$(eval echo "$`eval echo $linex`")
    if [ "$proxy_log_debug" -ge "2" ]
    then
	echo `echo $content` >&2
    fi
    if [ "`echo $content | $awk '{print $1}'`" = "Content-Length:" ]
    then
	content_length="`echo $content | $awk '{print $2}' | tr -d '\r'`"
	if [ "$proxy_log_debug" -ge "1" ]
	then
	    echo "ID $id CONTENT-LENGTH: $content_length" >&2
	fi
    fi
    if [ "`echo $content | wc -w`" = "0" ]
    then
	if [ "$content_length" != "" ]
	then
	    read -n $content_length content_post
	fi
	break
    fi
done

connect_to=`/bin/echo -e "$host\n$line3\n$line4" | grep 'Host:' | $awk '{print $2}' | $sed -e 's#http://##g' -e 's#/##g' -e 's#?.*##g' | tr -d '\r'`
connect_to_port_test=`echo $connect_to | $awk -F: '{print $2}'"`
connect_to=`echo $connect_to | $awk -F: '{print $1}'"`

if [ -n "$connect_to_port_test" ]
then
    connect_to_port="$connect_to_port_test"
else
    connect_to_port="$proxy_connect_port"
fi

if [ "$proxy_log_debug" -ge "1" ]
then
    echo "ID $id CONNECT $connect_to $connect_to_port" >&2
fi

# Inject JavaScript code only to non-localhost connections excluding extenstions listed below
if [ "$connect_to" != "127.0.0.1" -a -z "`echo $request | egrep -i '\.swf |\.jpg |\.png |\.ico |\.gif |\.js |\.css '`" ]
then
    inject=1
fi

/bin/echo -e $(for linex in `eval echo $read_lines`; do content=$(eval echo "$`eval echo $linex`"); if [ -n "$content" ]; then echo "$content\n"; fi; done; if [ -n "$content_post" ]; then /bin/echo -e "$content_post"; fi; /bin/echo -e "\r\n") | \
    $sed 's/^ //g' | \
    if [ "$proxy_log_debug" -ge "3" ]
    then
	tee -a $proxy_log_file
    else
	cat
    fi | \
    $sed  \
	-e 's#^GET http://[A-Za-z0-9\.\-\:]*/\(.*\)#GET /\1#g' \
	-e 's#^POST http://[A-Za-z0-9\.\-\:]*/\(.*\)#POST /\1#g' \
	-e 's/\(Connection:\).*/\1 close/g' | \
    if [ "$inject" = "1" ]
    then
	$sed \
	    -e 's#HTTP/1.1#HTTP/1.0#g' \
	    -e 's/\(Accept-Encoding:\).*/\1 identity/g'
    else
	cat
    fi | \
    if [ "$proxy_log_debug" -ge "3" ]
    then
	tee -a $proxy_log_file
    else
	cat
    fi | \
    $nc -w$proxy_wait_time $connect_to $connect_to_port | \
    if [ "$inject" = "1" ]
    then
      $sed \
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
			else if (key==404)\n\
				{\n\
				//the green button on the remote control have been pressed\n\
				//Switch to the Keyboard\n\
				SwitchFocusedPage();\n\
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
		\n\
	function BackSpace()\n\
		{\n\
		//I send a backspace on the currFocusedElement field\n\
		var str = document.activeElement.value;\n\
		document.activeElement.value = str.slice(0,str.length-1);\n\
		}\n\
		\n\
		\n\
	//windows.PostMessage management\n\
	//it is necessary to bypass browsers block on cross-domain frames communication.\n\
	window.addEventListener(\"message\", receiveMessage, false);\n\
	\n\
	function receiveMessage(event)\n\
		{\n\
		if (event.data == 'FocusToYou')\n\
			{\n\
			//set focus on current document\n\
			if (document.forms.length != 0)\n\
				{\n\
				document.forms[0].focus();\n\
				}\n\
			else\n\
				{\n\
				document.links[0].focus();\n\
				}\n\
			}\n\
		return;\n\
		}\n\
	\n\
	function SwitchFocusedPage()\n\
	{\n\
	//window.PostMessage\n\
	//it is necessary to bypass browsers block on cross-domain frames communication.\n\
	parent.postMessage('FocusToYou', '*');\n\
	}\n\
	\n\
	document.defaultAction = true;\n\
	</script>\n\
      #"
    else
	cat
    fi | \
if [ "$proxy_log_debug" -ge "3" ]
then
    tee -a $proxy_log_file
else
    cat
fi

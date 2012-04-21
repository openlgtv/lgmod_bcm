#!/bin/ash
# OpenLGTV BCM script proxy.sh by xeros
# JavaScript code by nicola_12345
# Proxy script for JavaScript code injection
# Source code released under GPL License

# Those vars should be set by proxy-start.sh or via env var in cmdline for testing
#[ -z "$proxy_wait_time" ]    && proxy_wait_time=8
[ -z "$proxy_wait_time" ]     && proxy_wait_time=4
[ -z "$proxy_wait_moretime" ] && proxy_wait_moretime=3
[ -z "$proxy_connect_port" ]  && proxy_connect_port=80
[ -z "$proxy_log_file" ]      && proxy_log_file=/var/log/proxy.log
[ -z "$proxy_inject_file" ]   && proxy_inject_file=/mnt/user/www/inject.js
[ -z "$proxy_inject_url" ]    && proxy_inject_url="http://127.0.0.1:88/user/inject.js"
[ -z "$proxy_adblock_flt" ]   && proxy_adblock_flt='doubleclick\.net|emediate\.eu|googleadservices\.com|/adserver\.|/googleads\.|://ads\.|/www/delivery/|media\.richrelevance.com/rrserver/js/|/advertising/|yieldmanager\.com|pagead2\.googlesyndication\.com|hit\.gemius\.pl'
[ -z "$proxy_useragent" ]     && proxy_useragent="Mozilla/5.0 (X11; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0"

[ "$netcast_webproxy_flashblock" = "1" ] && proxy_flash_flt='|\.swf' || proxy_flash_flt=""

# For proxy testing on PC
#[ -z "$nc" ]                 && nc="busybox nc"
[ -z "$nc" ]                  && nc=nc
[ -z "$awk" ]                 && awk=awk

read_lines="request host line3 line4 line5 line6 line7 line8 line9 line10 line11 line12 line13 line14 line15 line16 line17 line18 line19 line20"

# 'for' loop on each variable from read_lines
for linex in $read_lines
do
    # Read full request header - one by line
    read -t 1 $linex
    if [ "$linex" = "request" ]
    then
	# Adblock for common ads or flash content
	# TODO: change parser for content-type answers for flash and media
	if [ -n "`echo $request | egrep -i -m 1 "${proxy_adblock_flt}${proxy_flash_flt}"`" ]
	then
	    # Log reject if debug >= 1
	    [ "$proxy_log_debug" -ge "1" ] && echo "REJECT request: $request" >&2
	    exit 1
	fi
    fi
    content=$(eval echo $"$linex")
    # Log content if debug >= 2
    [ "$proxy_log_debug" -ge "2" ] && echo "$content" >&2
    # Check original Content-Length
    if [ "${content%% *}" = "Content-Length:" ]
    then
	content2="${content#* }"
	content_length="`echo $content2 | tr -d '\r'`"
	# Log Content-Length info if debug >= 1
	[ "$proxy_log_debug" -ge "1" ] && echo "ID $id CONTENT-LENGTH: $content_length" >&2
    fi
    # Check if content is empty
    if [ "$content" = "" -o -z "$content" ]
    then
	# After previous content (line) was empty, read number of bytes set of next content in Content-Length
	[ -n "$content_length" ] && read -n $content_length content_post
	break
    fi
done

# Check IP addres/DNS name and port number of host to connect to
connect_to=`echo -e "$request\n$host\n$line3\n$line4" | egrep -m 1 '^CONNECT |^Host:' | cut -d" " -f2 | sed -e 's#http://##' -e 's#/##g' -e 's#?.*##' -e 's/\r//'`
connect_to_port_test="${connect_to#*:}"

request_type=`echo -e "$request\n$host\n$line3\n$line4" | egrep -m 1 '^CONNECT |^GET |^POST ' | cut -d" " -f1`

if [ -n "$connect_to_port_test" -a "$connect_to_port_test" != "$connect_to" ]
then
    connect_to_port="$connect_to_port_test"
else
    connect_to_port="$proxy_connect_port"
fi

connect_to=${connect_to%:*}

# Log connection host and port if debug >= 1

if [ "$request_type" = "CONNECT" ]
then
    # when connection needs to be tunnelled via SSL/TLS then don't try to manipulate its content but make only pass-through connection instead
    [ "$proxy_log_debug" -ge "1" ] && echo "ID $id PASS-THROUGH CONNECTION WITH 'CONNECT' METHOD: $connect_to $connect_to_port" >&2
    echo -e "HTTP/1.0 200 Connection established\r\n\r\n"
    $nc $connect_to $connect_to_port
    exit 0
else
    [ "$proxy_log_debug" -ge "1" ] && echo "ID $id CONNECTION WITH '$request_type' METHOD: $connect_to $connect_to_port" >&2
fi

# Inject JavaScript code only to non-localhost connections excluding extenstions listed below
if [ "$connect_to" != "127.0.0.1" -a -z "`echo $request | egrep -i -m 1 '\.asf[ ?]|\.wmv[ ?]|\.mp3[ ?]|\.mp4[ ?]|\.swf[ ?]|\.jpg[ ?]|\.png[ ?]|\.ico[ ?]|\.gif[ ?]|\.js[ ?]|\.css[ ?]|\.xml[ ?]'`" ]
then
    inject=1
fi

# It would be better to pass-through 'HTTP/1.1' requests if content is not going to be modified but 'Connection: Keep-Alive' makes a problem with delay then and servers do not listen for 'Connection: Close' in 'HTTP/1.1' requests

# Substring of gathered full request header (up to 'nc') and of gathered output (after 'nc')
echo -e $(for linex in $read_lines
	do
	    content=$(eval echo $"$linex")
	    [ -n "$content" ] && echo "$content\n"
	done
	[ -n "$content_post" ] && echo -e "$content_post"
	echo -e "\r\n") | \
    sed \
	-e 's/^ //g' \
	-e 's#HTTP/1.1#HTTP/1.0#' \
	-e 's#^\([GP][EO][TS][T ]*\)http://[A-Za-z0-9\.\-\:]*/\(.*\)#\1/\2#' \
	-e 's/\(Connection:\).*/\1 close\r/' | \
    if [ "$inject" = "1" ]
    then
	sed \
	    -e 's/\(Accept-Encoding:\).*/\1 identity\r/' \
	    -e "s#\(User-Agent:\).*#\1 $proxy_useragent\r#"
	# DEBUG
	#    -e "s#\(User-Agent:\).*#\1 $proxy_useragent\r#" | \
	#if [ "$proxy_log_debug" -ge "3" ]
	#then
	#    tee -a $proxy_log_file
	#else
	#    cat
	#fi
    else
	cat
    fi | \
    if [ "$inject" = "1" ]
    then
      #tee -a /var/log/proxy-debug.log | $nc -w$(($proxy_wait_time+$proxy_wait_moretime)) $connect_to $connect_to_port | \
      $nc -w$proxy_wait_time $connect_to $connect_to_port | \
      if [ -f "$proxy_inject_file" ]
      then
        sed \
	    -e '/^Content-Length:/d' \
	    -e "s#\(<hea[^>]*>\)#\1<script type='text/javascript' language='JavaScript' src='$proxy_inject_url'></script>#I"
	    -e 's#<input#<INPUT onKeyPress="return false;"#gI' \
	    -e "s# target=[\'\"]_[^\'\"]*[\'\"]##gI"
	# DEBUG
	#    -e "s#<[Hh][Ee][Aa][Dd]>#<HEAD><script type='text/javascript' language='JavaScript' src='$proxy_inject_url'></script>#" | \
	#if [ "$proxy_log_debug" -ge "3" ]
	#then
	#    tee -a $proxy_log_file
	#else
	#    cat
	#fi
      else
        sed \
	    -e '/^Content-Length:/d' \
	    -e "s#\(<hea[^>]*>\)#\1\n\
	<script type='text/javascript'>\n\
	var keys = new Array();\n\
	keys['0'] = new Object();\n\
	keys['0'].ctr = 0;\n\
	keys['0'].char = [' ','0'];\n\
	keys['1'] = new Object();\n\
	keys['1'].ctr = 0;\n\
	keys['1'].char = ['.',':','/','1',',','@','\\\\\\\','\$','%','\#'];\n\
	keys['2'] = new Object();\n\
	keys['2'].ctr = 0;\n\
	keys['2'].char = ['a','b','c','2'];\n\
	keys['3'] = new Object();\n\
	keys['3'].ctr = 0;\n\
	keys['3'].char = ['d','e','f','3'];\n\
	keys['4'] = new Object();\n\
	keys['4'].ctr = 0;\n\
	keys['4'].char = ['g','h','i','4'];\n\
	keys['5'] = new Object();\n\
	keys['5'].ctr = 0;\n\
	keys['5'].char = ['j','k','l','5'];\n\
	keys['6'] = new Object();\n\
	keys['6'].ctr = 0;\n\
	keys['6'].char = ['m','n','o','6'];\n\
	keys['7'] = new Object();\n\
	keys['7'].ctr = 0;\n\
	keys['7'].char = ['p','q','r','s','7'];\n\
	keys['8'] = new Object();\n\
	keys['8'].ctr = 0;\n\
	keys['8'].char = ['t','u','v','8'];\n\
	keys['9'] = new Object();\n\
	keys['9'].ctr = 0;\n\
	keys['9'].char = ['w','x','y','z','9'];\n\
	var append=false;\n\
	var upper=false;\n\
	var key_char='';\n\
	var str='';\n\
	var timer;\n\
	var prevNum=null;\n\
	function keypad(num)\n\
	{\n\
	  var currFocusedElement = document.activeElement;\n\
	  if (currFocusedElement.type == 'text' || currFocusedElement.type == 'textarea')\n\
		  {\n\
		  if (prevNum!=null \&\& prevNum!=num) append=true;\n\
		  if (keys[num].ctr>keys[num].char.length-1 || append) keys[num].ctr=0;\n\
		  if (upper) key_char=keys[num].char[keys[num].ctr].toUpperCase(); else key_char=keys[num].char[keys[num].ctr];\n\
		  if (append) \n\
			str=currFocusedElement.value+key_char;\n\
		  else\n\
			str=(currFocusedElement.value.length==0) ? currFocusedElement.value=key_char:currFocusedElement.value.substring(0,currFocusedElement.value.length-1)+key_char;\n\
		  currFocusedElement.value=str;\n\
		  keys[num].ctr++;\n\
		  prevNum=num;\n\
		  append=false;\n\
		  clearTimeout(timer);\n\
		  timer=setTimeout(function(){append=true;}, 2000);\n\
		  }\n\
	}\n\
	function check(e)\n\
		{\n\
		if (!e) var e = window.event;\n\
		(e.keyCode) ? key = e.keyCode : key = e.which;\n\
		try\n\
			{\n\
			if (key==48) keypad('0');\n\
			else if (key==49) keypad('1');\n\
			else if (key==50) keypad('2');\n\
			else if (key==51) keypad('3');\n\
			else if (key==52) keypad('4');\n\
			else if (key==53) keypad('5');\n\
			else if (key==54) keypad('6');\n\
			else if (key==55) keypad('7');\n\
			else if (key==56) keypad('8');\n\
			else if (key==57) keypad('9');\n\
			else if (key==19|key==220)\n\
			{\n\
			if (upper) upper=false; else upper=true;\n\
			e.preventDefault();\n\
			return false;\n\
			}\n\
			else if (key==404) SwitchFocusedPage();\n\
			else if (key==406) BackSpace();\n\
			else if (key==415) parent.postMessage('ShowHideKeyboardTab', '*');\n\
			else if (key==461) history.back(-1);\n\
			else if (key==1001) window.NetCastExit();\n\
			}catch(Exception){}\n\
		}\n\
	document.onkeydown = check;\n\
	function BackSpace()\n\
		{\n\
		var str = document.activeElement.value;\n\
		document.activeElement.value = str.slice(0,str.length-1);\n\
		}\n\
	window.addEventListener(\"message\", receiveMessage, false);\n\
	function receiveMessage(event)\n\
		{\n\
		if (event.data == 'FocusToYou')\n\
			{\n\
			if (document.forms.length != 0) document.forms[0].focus();\n\
			else document.links[0].focus();\n\
			}\n\
		return;\n\
		}\n\
	function SwitchFocusedPage()\n\
	{\n\
	parent.postMessage('FocusToYou', '*');\n\
	}\n\
	document.defaultAction = true;\n\
	</script>\n\
        #I" \
	    -e 's#<[Ii][Nn][Pp][Uu][Tt]#<INPUT onKeyPress="return false;"#g' \
	    -e "s# target=[\'\"]_[^\'\"]*[\'\"]##gI"
	# DEBUG
	#    -e "s# target=[\'\"]_[^\'\"]*[\'\"]##gI"
	#if [ "$proxy_log_debug" -ge "3" ]
	#then
	#   tee -a $proxy_log_file
	#else
	#    cat
	#fi
      fi
else
      $nc -w$(($proxy_wait_time+$proxy_wait_moretime)) $connect_to $connect_to_port
      # DEBUG
      #$nc -w$(($proxy_wait_time+$proxy_wait_moretime)) $connect_to $connect_to_port | \
      #if [ "$proxy_log_debug" -ge "3" ]
      #then
      #	tee -a $proxy_log_file
      #else
      #	cat
      #fi
fi

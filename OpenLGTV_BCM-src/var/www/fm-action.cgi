#!/usr/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- OpenLGTV BCM FileManager by xeros -->
<!-- fm-action.cgi script for handling actions like copy/move/delete/play and confirm/cancel of operation -->
<!-- Source code released under GPL License -->

<style type="text/css">
    body {
	font-family:monospace;
	//height: 720px;
	//font-family:"TiresiasScreenfont";
    }
    a:link, a:visited {
	color:black;
	text-decoration:bold;
    }
    tbody.main {
	width: 95%;
	height: 95%;
	overflow-y:auto;
	overflow-x: hidden;
	max-height:700px;
    }
    tbody.scrollable {
	display: block;
	height: 100%;
	overflow-y: auto;
	overflow-x: hidden;
	max-height:700px;
    }
    td.panel {
	min-width: 410px;
    }
    pre{
	text-align: left;
	overflow: auto;
	height: 97%;
	width: 100%;
	white-space: pre-wrap;                 /* CSS3 browsers  */
	white-space: -moz-pre-wrap !important; /* 1999+ Mozilla  */
	white-space: -pre-wrap;                /* Opera 4 thru 6 */
	white-space: -o-pre-wrap;              /* Opera 7 and up */
	word-wrap: break-word;                 /* IE 5.5+ and up */
	z-index: 99;
	margin: 1 auto;
    }
    input.download {
	background-color:#cc0000;
	font-weight:bold;
	color:#ffffff;
	width:50px;
	height:15px;
	font-size:7.5px;
    }
</style>
<title>CGI FileManager by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<script type="text/javascript">
<!--

<?

#echo "START:`date`" > /tmp/log.log

export log_dir="/tmp/var/log/fm"
export log_file="$log_dir/fm.log"
play_enum="$log_dir/last_played.info"
[ ! -d "$log_dir"    ] && mkdir -p "$log_dir"

[ -n "$FORM_side"    ] && export side="$FORM_side" || export side="l"
[ -n "$FORM_skip"    ] && export skip="$FORM_skip" || export skip="next"
[ -n "$FORM_lpth"    ] && export lpth="$FORM_lpth"
[ -n "$FORM_rpth"    ] && export rpth="$FORM_rpth"
[ -n "$FORM_action"  ] && export action="$FORM_action"
[ -n "$FORM_link"    ] && export link="$FORM_link"

[ -z "$FORM_timeout" ] && FORM_timeout=7000
[ -z "$FORM_imgzoom" ] && FORM_imgzoom=0

if [ "$side" = "l" ]
then
    export spth="$lpth"
    export dpth="$rpth"
    export lpthx="$lpth"
    [ "$action" != "status" ] && export lpthx="`dirname \"$lpth\"`"
    export rpthx="$rpth"
    export xselect="$FORM_lselected"
else
    export spth="$rpth"
    export dpth="$lpth"
    export lpthx="$lpth"
    export rpthx="$rpth"
    [ "$action" != "status" ] && export rpthx="`dirname \"$rpth\"`"
    export xselect="$FORM_rselected"
fi
[ "$lpthx" = "/" -o "$lpthx" = "." ] && export lpthx=""
[ "$rpthx" = "/" -o "$rpthx" = "." ] && export rpthx=""

echo "var action = '$action';"
echo "var skip = '$skip';"
echo "var side = '$side';"
echo "var lpth = '$lpth';"
echo "var rpth = '$rpth';"
echo "var xselect = '$xselect';"
echo "var refreshTime = '$FORM_timeout';"
echo "var imgZoom = $FORM_imgzoom;"

?>

var col = 1; //number of 'cells' in a row
var current = 1;
var next = current;
//var side = 'l';
var side = 'r';
var nside = side;
var winWidth = window.innerWidth;
var winHeight = window.innerHeight;
//var imgZoom = 0;
var h = 0;
var w = 0;
var scroll = 0;
var regexpTimeout=/timeout=[0-9]+/gim;
var regexpImgZoom=/imgzoom=[0-9]+/gim;
var regexpSkip=/skip=[a-z]+/gim;
var winLoc=window.location.href;
var currentImage;
var refresh = 0;
var timer;

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
			case 33: scroll=-600; break; //ch up
			case 34: scroll=600; break; //ch up
			case 37: next = current; nside = 'l'; skip='prev'; break; //left
			case 38: scroll=-30; break; //up
			case 39: next = current; nside = 'r'; skip='next'; break; //right
			case 40: scroll=30; break; //down
			}
		if (key==33|key==34|key==37|key==38|key==39|key==40)
		{
		    if (imgZoom!=2)
		    {
			if (next==0) next = 1;
			if (action=='play' && refresh==1 && (key==37|key==39))
			{
			    adjustURL();
			} else {
			    //Check if new link exists, if not then go to previous one until finds the one that exists
			    if (!document.links['link_' + nside + next])
			    {
			    do {
				next = next - 1;
			    } while ((!document.links['link_' + nside + next])&&(next >= 1));
			    }
			    ChangeBgColor();
			    //Move to the next bookmark
			    if (document.links['link_' + nside + next])
			    {
				var code=document.links['link_' + nside + next].name;
				document.links['link_' + nside + next].focus();
				current = next;
				side = nside;
			    } else if (document.getElementById('run')) {
				document.getElementById('run').scrollTop=document.getElementById('run').scrollTop+(scroll);
			    }
			}
			//Prevent scrolling
			return false;
		    }
		}
		else if (key==13) 
			{
			switch(window.imgZoom)
				{
				case 0: window.imgZoom=1; break;
				case 1: window.imgZoom=2; break;
				case 2: window.imgZoom=0; break;
				}
			resizeImage('image',window.imgZoom);
			return false;
			}
		else if (key==19) 
			{
			// PAUSE - pause slideshow
			if (action == 'play') clearTimeout(window.timer);
			return false;
			}
		else if (key==32) 
			{
			if (document.links['link_' + side + current]) document.getElementById('link_' + side + current).click();
			if (action == 'play') clearTimeout(window.timer);
			return false;
			}
		else if ((key>47)&(key<60)) { window.refreshTime=(key-48)*2000; return false; }
		else if (key==415) 
			{
			// PLAY - resume slideshow
			if (action=='play' && refresh==1)
			    {
			    skip='next';
			    adjustURL();
			    }
			}
		else if (key==461|key==27) 
			{
			//the back button on the remote control or ESC have been pressed
			//NetCastBack API
			//window.NetCastBack();
			//lets get back to WebUI instead of closing NetCast service
			<? [ "$action" != "play" -o "${spth:0:7}" = "http://" ] && echo "history.go(-1);" || echo "backToFM();" ?>
			e.preventDefault();
			}
		else if (key==1001) 
			{
			//the exit button on the remote control have been pressed
			//NetCastExit API
			window.NetCastExit();
			}
		}catch(Exception){}
	}

function ChangeBgColor()
	{
	//Change the TD element BgColor.
	if (document.getElementById('tr_' + side + current)) document.getElementById('tr_' + side + current).bgColor = '#FFFFFF';
	if (document.getElementById('tr_' + nside + next)) document.getElementById('tr_' + nside + next).bgColor = '#D3D3D3';
	}

function setCurrent(element)
	{
	var string = element.id;
	//cut number after 'link' name
	current = string.slice(4,string.length);
	}

function OnLoadSetCurrent(element)
	{
	current=1;
	if (document.links['link_' + side + current]) document.links['link_' + side + current].focus();
	ChangeBgColor();
	}

function sleep(milliseconds)
	{
	var start = new Date().getTime();
	while ((new Date().getTime() - start) < milliseconds)
	    {
	    // Do nothing
	    }
	}

function resizeImage(imgId,zoomType)
	{
	var pic = document.getElementById(imgId);
	if (w==0) { w = pic.offsetWidth;  }
	if (h==0) { h = pic.offsetHeight; }
	var picAR = w/h;
	var winAR = winWidth/winHeight;
	switch(zoomType)
		{
		case 0: if (picAR < winAR) { pic.height = winHeight; pic.width=winHeight*picAR; } else { pic.width = winWidth; pic.height=winWidth/picAR; }; break; //fullscreen respect aspect ratio
		case 1: pic.width = winWidth; pic.height = winHeight; break; // stretch to fit the screen regardless aspect ratio
		case 2: pic.width = w; pic.height = h; break; // original image size
		}
		//case 2: pic.width = w*100; pic.height = h*100; break; // original image size
	}

function adjustURL()
	{
	winLoc=winLoc.replace(window.regexpTimeout, 'timeout='+window.refreshTime);
	winLoc=winLoc.replace(window.regexpImgZoom, 'imgzoom='+window.imgZoom);
	winLoc=winLoc.replace(window.regexpSkip, 'skip='+window.skip);
	window.location.replace(winLoc);
	}

function setRefresh()
	{ window.timer = setTimeout(adjustURL, window.refreshTime); }

document.defaultAction = true;

// break JS code for two contexts to make keyevent actions more responsive - to make them work even when rest part was not yet completed
// -->
</script><script type="text/javascript">

<?

echo "function backToFM(){ window.location.replace('fm.cgi?type=related&amp;side=${side}&amp;lpth=${lpthx}&amp;rpth=${rpthx}&amp;select=${xselect}'); }"

if [ "$action" = "play" ]
then
    # ugly workaround for getting script runned twice - simply kill previous stat command
    killall stat > /dev/null 2>&1 &
    ftype="`stat -c '%F' "${spth}"`"
    ext="${spth##*.}"
    [ -n "$ext" ] && ext="`echo $ext | tr [:upper:] [:lower:]`"
    #play_enum="${spth}/last_played.info"
    ##play_enum="$log_dir/last_played.info"
    play_enum_comment="OpenLGTV BCM FileManager: last played file number"
    if [ "$ftype" = "directory" -o "$ext" = "m3u" -o "$ext" = "pls" ]
    then
	refresh=1
	file_num=1
	echo "refresh = 1;"
	if [ "$ftype" = "directory" ]
	then
	    #content_all=`busybox stat -c "%F@%n" "$spth"/* | grep "regular file" | grep -v "$play_enum" | sort | sed -e "s/regular file@//g" -e 's# #\&nbsp;#g'`
	    content_all=`stat -c "%F@%n" "$spth"/* | grep "regular file" | sed -e "s/regular file@//g" -e 's# #\&nbsp;#g'`
	else
	    spthd="${spth%/*}"
	    playlist=1
	    content_all=`egrep -v "#|^$" "$spth" | awk -F'No_FiElD_DeLiM' -v spthd="$spthd" '{if (match($0,/^\//)) {print "root" $1} else {if (match($0,/:\/\//)) {print $1} else {print "root" spthd "/" $1}}}' | sed -e 's# #\&nbsp;#g' -e 's/\r//g'`
	    #echo "$content_all" > /tmp/content_all.log
	    #play_enum="${spth}.info"
	    spth="${spthd}"
	fi
	if [ ! -f "${play_enum}" ]
	then
	    echo -e "# $play_enum_comment\n1" > "${play_enum}"
	    start_playback=1
	else
	    #start_playback=$((`grep -v "#" "${play_enum}"`+1))
	    start_playback=`grep -v "#" "${play_enum}"`
	    [ "$skip" = "prev" ] && dif="(-1)" || dif="1" # TODO: skip=random handling
	    start_playback="$((${start_playback}+${dif}))"
	    [ "$start_playback" -lt "1" ] && start_playback=1
	    echo -e "# $play_enum_comment\n$start_playback" > "${play_enum}"
	fi
	file_num_max="`echo $content_all | wc -w`"
	[ "$start_playback" -gt "$file_num_max" ] && echo -e "# $play_enum_comment\n1" > "${play_enum}" && start_playback=1
	for content in $content_all
	do
	    #[ "$file_num" = "$start_playback" ] && spth="`echo $content | sed 's/\&nbsp;/ /g'`" && break
	    [ "$file_num" -eq "$start_playback" ] && spth="`echo $content | sed 's/\&nbsp;/ /g'`"
	    [ "$file_num" -gt "$start_playback" ] && spth_next="`echo $content | sed 's/\&nbsp;/ /g'`" && break
	    file_num=$((${file_num}+1))
	done
    fi
    ext="${spth##*.}"; ext="`echo $ext | tr [:upper:] [:lower:]`"
    [ -n "$spth_next" ] && ext_next="${spth_next##*.}" && ext_next="`echo $ext_next | tr [:upper:] [:lower:]`"
    #[ "$refresh" = "1" ] && [ "$ext" = "sh" -o "$ext" = "cgi" -o "$ext" = "htm" -o "$ext" = "html" ] && echo "<script type='text/javascript'>window.location.replace(window.location.href);</script></head><body></body></html>" && exit 0
    [ "$refresh" = "1" ] && [ "$ext" = "sh" -o "$ext" = "cgi" -o "$ext" = "htm" -o "$ext" = "html" ] && echo "window.location.replace(window.location.href);</script></head><body></body></html>" && exit 0
    full_spth="$spth"
    full_spth_next="$spth_next"
    [ -z "$playlist" ] && full_spth="root$spth" && [ -n "$spth_next" ] && full_spth_next="root$spth_next"
    [ "${full_spth:0:8}" = "roothttp" ] && full_spth="${full_spth:4}"
    [ "${full_spth_next:0:8}" = "roothttp" ] && full_spth_next="${full_spth_next:4}"
    if [ "$ext" = "cfg" -o "$ext" = "conf" -o "$ext" = "ini" -o "$ext" = "inf" -o "$ext" = "info" -o "$ext" = "log" -o "$ext" = "txt" -o "$ext" = "xml" ]
    then
	ftype=text
    else
	if [ "$ext" = "gif" -o "$ext" = "jpeg" -o "$ext" = "jpg" -o "$ext" = "png" ]
	then
	    ftype=image
	else
	    #echo "<script type='text/javascript'>"
	    if [ "$refresh" = "1" ]
	    then
		echo "window.timer = setTimeout(\"window.location='$full_spth'\",2000);"
	    else
		echo "window.timer = setTimeout(\"window.location.replace('$full_spth')\",2000);"
	    fi
	    # TODO: heh, what's that for???
	    echo "setTimeout(\"window.location.replace(window.location.href)\",4000);"
	    #echo "</script>"
	fi
    fi
    ############[ "$refresh" = "1" ] && [ "$ftype" = "text" -o "$ftype" = "image" ] && echo "<script type='text/javascript'>var regexp=/timeout=[0-9]*/; setTimeout('window.location.replace(window.location.href.replace(regexp, \"timeout=\"+window.refreshTime))',window.refreshTime);</script>"
fi

#echo "RUNNING:`date`" >> /tmp/log.log

echo "</script></HEAD><BODY bgcolor='black'>"

[ "$ftype" != "text" ] && echo '<br><center><font size="+4" color="yellow"><b>OpenLGTV BCM FileManager</b></font><br><font size="+3" color="yellow">by xeros<br><br></font>'
[ "$ftype" != "image" ] && echo '<div style="width:99%; margin: 0 auto; font-size:16px; background-color:white;">'

[ "$FORM_pid" != "" ] && pid="$FORM_pid"

if [ -n "$FORM_cancel" -a -n "$pid" ]
then
    process="`ps | grep \"^ *$pid \"`"
    if [ -n "$process" ]
    then
	echo "<font size='+3' color='red'><br><b>Cancelling process:</b></font><font size='+3' color='black'><br><br>$process<br><br>"
	kill "$pid" 2>&1
	sleep 1
	process="`ps | grep \"^ *$pid \"`"
	if [ -n "$process" ]
	then
	    kill -9 "$pid" 2>&1
	fi
    fi
    timeout=1000
    echo "<script type=\"text/javascript\">"
    echo "window.timer = setTimeout(\"backToFM()\",$timeout);"
    echo "</script>"
    echo "</font></div></center></body></html>"
    exit 0
fi

if [ "$action" = "play" ]
then
    [ "$refresh" = "1" ] && [ "$ftype" = "text" -o "$ftype" = "image" ] && echo '<font color="green" size="+2"><b><script>document.write("Refresh time set to: ", window.refreshTime/1000, " second[s] (use number buttons to change it [x2])");</script></b></font>'
    [ "$ftype" = "image" ] && echo "<br><br><font size='+2' color='yellow'><br>Loading Image</font>"
    if [ "$ftype" = "text" ]
    then
	echo "<pre align='left' class='run' id='run'>"
	cat "$spth" | sed -e 's/\&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g'
	echo "</pre>"
    else
	if [ "$ftype" = "image" ]
	then
	    if [ "$ext_next" = "jpg" ]
	    then
		# INFO: DOES IT REALLY MAKE SENSE TO DO SUCH PRELOADING? MAYBE WHOLE CODE SHOULD GET REWRITTEN WITH JAVASCRIPT AND GET RID OF PAGE REFRESHING?
		#echo -e "<div id='divImage' style='width:100%; height:100%; background-color:black; position:absolute; left:0px; top:0px; align:center; text-align:center;'>\n\
		echo -e "<div id='divImage' style='width:100%; background-color:black; position:absolute; left:0px; top:0px; align:center; text-align:center;'>\n\
			 <script>function preloadNextImage() { window.currentImage.style.display='inline'; resizeImage('image',window.imgZoom); preloadImageObject = new Image(); preloadImageObject.src='$full_spth_next'; preloadImageObject.style.visibility='hidden'; preloadImageObject.style.display='none'; preloadImageObject.onload=setRefresh; document.getElementById('divImage').appendChild(preloadImageObject); };\n\
			  currentImage = new Image(); currentImage.id = 'image'; currentImage.style.display='none'; currentImage.src = '$full_spth'; currentImage.onload = preloadNextImage; document.getElementById('divImage').appendChild(currentImage);\n\
			 </script>\n\
			 </div>"
		#echo -e "<div id='divImage' style='width:100%; background-color:black; position:absolute; left:0px; top:0px; align:center; text-align:center;'>\n\
		#	 <script>function preloadNextImage() { window.currentImage.style.display='inline'; resizeImage('image',window.imgZoom); setRefresh(); };\n\
		#	  currentImage = new Image(); currentImage.id = 'image'; currentImage.style.display='none'; currentImage.src = 'root$spth'; currentImage.onload = preloadNextImage; document.getElementById('divImage').appendChild(currentImage);\n\
		#	 </script>\n\
		#	 </div>"
	    else
		#echo "<div style='width:100%; height:100%; background-color:black; position:absolute; left:0px; top:0px; align:center; text-align:center;'><img id='image' onload=\"resizeImage('image',0);\" width='1%' src='root$spth'/></div>"
		#echo -e "<div id='divImage' style='width:100%; height:100%; background-color:black; position:absolute; left:0px; top:0px; align:center; text-align:center;'>\n\
		echo -e "<div id='divImage' style='width:100%; background-color:black; position:absolute; left:0px; top:0px; align:center; text-align:center;'>\n\
			 <script>function preloadNextImage() { window.currentImage.style.display='inline'; resizeImage('image',window.imgZoom); setRefresh(); };\n\
			  currentImage = new Image(); currentImage.id = 'image'; currentImage.style.display='none'; currentImage.src = '$full_spth'; currentImage.onload = preloadNextImage; document.getElementById('divImage').appendChild(currentImage);\n\
			 </script>\n\
			 </div>"
	    fi
	else
	    echo "<center><font size='+4' color='brown'><br><b>Starting playback of: </font><br><br><font size='+3' color='blue'>$spth<br><br>...<br><br></font>"
	fi
    fi
fi

[ -f "$log_file" -a "$action" = "status" ] && export FORM_confirm=yes

if [ "$FORM_confirm" != "yes" ]
then
    if [ "$action" != "play" ]
    then
	echo "<center><font size='+4' color='brown'><br><b>"
	if [ "$action" = "copy" -o "$action" = "move" ]
	then
	    echo "Are you sure you want to ${action}?<br><font size='+3' color='blue'><br>$spth<br><br><font color='black' size='+3'>to</font><font size='+3' color='blue'><br><br>$dpth/</font>"
	else
	    if [ "$action" = "delete" ]
	    then
		echo "Are you sure you want to ${action}?<br><font size='+2' color='black'><br>$spth</font>"
	    else
		echo "No copy/move actions have been executed yet!<br><br>"
		echo '<script type="text/javascript">window.timer = setTimeout("history.go(-1)",3000);</script>'
		exit 0
	    fi
	fi
	echo "</b><br><br></font>"
	echo "<table><tr><td id='tr_l1' width='200px' align='center'><b><a id='link_l1' href='${REQUEST_URI}&amp;confirm=yes'><font size='+4'>Yes</font></a></b></td><td id='tr_r1' width='200px' align='center'><b><a id='link_r1' href='javascript:history.go(-1);'><font size='+4'>No</font></a></b></td></tr></table></center><br><br>"
    fi
else
    if [ "$action" = "copy" -o "$action" = "move" -o "$action" = "status" ]
    then
	if [ "$action" = "status" -o "$FORM_onlystatus" = "1" ]
	then
	    # TODO TODO TODO TODO
	    if [ -n "${pid}" ]
	    then
		stats="`grep \"^${pid}#\" ${log_file}`"
	    else
		stats="`tail -n1 ${log_file}`"
		pid="${stats%%\#*}"
	    fi
	    FORM_onlystatus=1
	    stats="${stats#*\#}"
	    org_action="${action}"
	    action="${stats%%\#*}"
	    stats="${stats#*\#}"
	    spth="${stats%%\#*}"
	    stats="${stats#*\#}"
	    dpth="${stats%%\#*}"
	    stats="${stats#*\#}"
	    time_start="${stats%%\#*}"
	    #time_start="${stats##*\#}"
	    stats="${stats#*\#}"
	    time_stop="${stats%%\#*}"
	    # TODO: what to do in this case?
	    #[ -z "${lpthx}" ] && lpthx="${spth%/*}"
	    #[ -z "${rpthx}" ] && rpthx="${dpth}"
	    [ -z "${side}"  ] && side="l"
	fi
	echo "<font size='+5' color='brown' style='text-transform: uppercase;'><b>$action in progress</b></font><br><br>"
	echo "<table>"
	echo "<tr><td><font size='+3' color='green'>Source: </font></td><td><font size='+3' color='black'>$spth</font><td></tr>"
	echo "<tr><td><font size='+3' color='green'>Target: </font></td><td><font size='+3' color='black'>$dpth/</font><td></tr>"
	echo "</table><br>"
	echo "<br>"
	SIFS="$IFS" IFS=$'\n'
	ssize=$(for i in `find "$spth" ! -type d`; do stat -c "%s" "$i"; done | awk '{sum += $1} END{OFMT = "%.0f"; print sum}') # could have been done with '-printf "%s\n"' or '-exec stat -c "%s" {}' as find arguments but busybox find does not support properly both of them
	IFS="$SIFS"
	if [ "$FORM_onlystatus" != "1" ]
	then
	    export spth dpth log_dir action
	    #pattern=`echo "$spth $dpth/" | sed -e 's/\[/\\\[/g' -e 's/\]/\\\]/g' -e 's/\'/\\\'/g' -e 's/\"/\\\"/g' -e 's/\./\\\./g'`
	    pattern=`echo "$spth $dpth/" | sed -e 's/\[/\\\[/g' -e 's/\]/\\\]/g' -e 's/\"/\\\"/g' -e 's/\./\\\./g'`
	    running_pid="`pgrep -f " $pattern " | tail -n 1`"
	    [ -z "$running_pid" ] && if [ "$action" = "copy" ]
	    then
		cp -r "$spth" "$dpth/" > "${log_dir}/${action}.error.log" 2>&1 &
		export pid="$!"
		# INFO: lets assume we pids are increased, not randomized to get both output pipe with pid and grab pid number from it
		#cp -r "$spth" "$dpth/" 2>&1 | tee "${log_dir}/${action}.error.$!.log" &
		###cp -r "$spth" "$dpth/" > "${log_dir}/${action}.error.$!.log" 2>&1 &
	    else
		mv "$spth" "$dpth/" > "${log_dir}/${action}.error.log" 2>&1 &
		export pid="$!"
		###mv "$spth" "$dpth/" 2>&1 | tee "${log_dir}/${action}.error.$!.log" &
	    fi
	    [ -z "$pid" -a -n "$running_pid" ] && pid="$running_pid"
	    ###pid_n="${log_dir}/${action}.error"
	    ###busybox usleep 100
	    #pid_f=`ls ${pid_n}.* | tail -n1`
	    ###pid_f="`busybox stat -c \"%z#%n\" ${pid_n}.* | sort | tail -n1`"
	    ###pid="${pid_f#*error.}"
	    ###export pid="${pid%.log*}"
	    time_start="`date +'%s'`"
	    time_start_status="${time_start}"
	    echo "${pid}#${action}#${spth}#${dpth}#${time_start}##" >> "${log_file}"
	    # update time_stop as separate shell process checking if copy/move process is still running in background
	    (for i in `seq 3000`; do [ -z "`ps | grep \"^ *$pid \"`" ] && time_stop="`date +'%s'`" && sed -i -e "s/^\\(${pid}#.*\\)##\$/\\1#${time_stop}#/g" "${log_file}" && exit 0; sleep 3; done) &
	else
	    [ -z "${time_start}" ] && time_start="`grep '^${pid}#' '${log_file}' | cut -d# -f5`"
	    time_start_status="`date +'%s'`"
	fi
	echo "<div id='status' style='font-size: 30px;'><font color=\"blue\">Copied:</font> 0 / ???<br><br><font color=\"blue\">Progress:</font> 0% &nbsp; <font color=\"blue\">Average speed:</font> ??? KB/s<br><br><font color=\"blue\">Elapsed time:</font> 0 seconds &nbsp; &nbsp;<font color=\"blue\">Remaining time:</font> ???<br><br></div>"
	dfile="`basename "$spth"`"
	####echo "<table><tr><td id='tr_l1' width='500px' align='center'><b><a id='link_l1' href='fm.cgi?type=related&side=${side}&lpth=${lpthx}&rpth=${rpthx}&select=${FORM_select}'><font size='+4'>Continue in background</font></a></b></td><td id='tr_r1' width='300px' align='center'><b><a id='link_r1' href='${REQUEST_URI}&pid=${pid}&cancel=1'><font size='+4'>Cancel</font></a></b></td></tr></table></center><br><br>"
	echo "<table><tr><td id='tr_l1' width='500px' align='center'><b><a id='link_l1' href='fm.cgi?type=related&amp;side=${side}&amp;lpth=${lpthx}&amp;rpth=${rpthx}&amp;select=${FORM_select}'><font size='+4'>Continue in background</font></a></b></td><td id='tr_r1' width='300px' align='center'><b><a id='link_r1' href='${REQUEST_URI}&amp;pid=${pid}&amp;cancel=1'><font size='+4'>Cancel</font></a></b></td></tr></table><br><br>"
	echo "<div id='result'></div>"
	# TODO TODO TODO: end HTML code here, later create just new sub elements
	####echo "</div>"
	echo "</div></center></body></html>"
	counter=0
	[ -z "$ssize" ] && ssize=1
	[ "$FORM_onlystatus" != "1" ] && sleep 1
	for i in `seq 2000`
	do
	    SIFS="$IFS" IFS=$'\n'
	    dsize=$(for j in `find "$dpth/$dfile" ! -type d`; do stat -c "%s" "$j"; done | awk '{sum += $1} END{OFMT = "%.0f"; print sum}')
	    IFS="$SIFS"
	    [ -z "$dsize" ] && dsize=0
	    percent="$(($dsize * 100 / $ssize))"
	    time_now="$time_stop"
	    [ -z "$time_stop" ] && time_now="`date +'%s'`"
	    elapsed=$((${time_now}-${time_start}))
	    elapsed_status=$((${time_now}-${time_start_status}))
	    elapsed_f="$elapsed seconds"
	    [ -z "$elapsed" -o "$elapsed" = "0" ] && elapsed=1 # ugly workaround for divide by 0 error
	    [ "$elapsed" -gt 60 ] && elapsed_f="$(($elapsed/60)) min $(($elapsed-(($elapsed/60)*60))) sec"
	    [ "$elapsed" -gt 3600 ] && elapsed_f="$(($elapsed/3600)) hrs $((($elapsed/60)-(($elapsed/3600)*60))) min $(($elapsed-(($elapsed/60)*60))) sec"
	    #echo "test pid:$pid dsize:$dsize elapsed:$elapsed time_start:$time_start time_now:$time_now"
	    average_bps=$((${dsize}/${elapsed}))
	    [ "$average_bps" = "0" ] && average_bps=1
	    #echo "test2 pid:$pid dsize:$dsize elapsed:$elapsed time_start:$time_start time_now:$time_now average_bps:$average_bps"
	    average_kbps=$((${average_bps}/1024))
	    rsize=$((${ssize}-${dsize}))
	    remain=$((${rsize}/${average_bps}))
	    remain_f="$remain seconds"
	    [ "$remain" -gt 60 ] && remain_f="$(($remain/60)) min $(($remain-(($remain/60)*60))) sec"
	    [ "$remain" -gt 3600 ] && remain_f="$(($remain/3600)) hrs $((($remain/60)-(($remain/3600)*60))) min $(($remain-(($remain/60)*60))) sec"
	    if [ "${#dsize}" -lt "4" ]
	    then
		dsize_f="${dsize} B"
	    else
		if [ "${#dsize}" -lt "7" ]
		then
		    dsize_f="$((${dsize}/1024)) KB"
		else
		    if [ "${#dsize}" -lt "10" ]
		    then
			dsize_mb="$((${dsize}/(1024*1024)))"
			dsize_mb_m="$((((${dsize}/1024)-(${dsize_mb}*1024))/10))"
			[ "${#dsize_mb_m}" -lt "2" ] && dsize_mb_m="0${dsize_mb_m}"
			dsize_f="${dsize_mb}.${dsize_mb_m} MB"
		    else
			dsize_gb="$((${dsize}/(1024*1024*1024)))"
			dsize_gb_m="$((((${dsize}/1024/1024)-(${dsize_gb}*1024))/10))"
			[ "${#dsize_gb_m}" -lt "2" ] && dsize_gb_m="0${dsize_gb_m}"
			# ugly workaround for integer arithmetic calculation errors on non-integer (float) values
			[ "$dsize_gb_m" -gt "99" ] && dsize_gb_m=99
			dsize_f="${dsize_gb}.${dsize_gb_m} GB"
		    fi
		fi
	    fi
	    if [ "${#ssize}" -lt "4" ]
	    then
		ssize_f="${ssize} B"
	    else
		if [ "${#ssize}" -lt "7" ]
		then
		    ssize_f="$((${ssize}/1024)) KB"
		else
		    if [ "${#ssize}" -lt "10" ]
		    then
			ssize_mb="$((${ssize}/(1024*1024)))"
			ssize_mb_m="$((((${ssize}/1024)-(${ssize_mb}*1024))/10))"
			[ "${#ssize_mb_m}" -lt "2" ] && ssize_mb_m="0${ssize_mb_m}"
			ssize_f="${ssize_mb}.${ssize_mb_m} MB"
		    else
			ssize_gb="$((${ssize}/(1024*1024*1024)))"
			ssize_gb_m="$((((${ssize}/1024/1024)-(${ssize_gb}*1024))/10))"
			[ "${#ssize_gb_m}" -lt "2" ] && ssize_gb_m="0${ssize_gb_m}"
			[ "$ssize_gb_m" -gt "99" ] && ssize_gb_m=99
			ssize_f="${ssize_gb}.${ssize_gb_m} GB"
		    fi
		fi
	    fi
	    echo "<script type='text/javascript'>document.getElementById('status').innerHTML ='<font color=\"blue\">Copied:</font> $dsize_f / $ssize_f<br><br><font color=\"blue\">Progress:</font> $percent% &nbsp; <font color=\"blue\">Average speed:</font> $average_kbps KB/s<br><br><font color=\"blue\">Elapsed time:</font> $elapsed_f &nbsp; &nbsp;<font color=\"blue\">Remaining time:</font> $remain_f<br><br>';</script>"
	    [ -n "`ps | grep \"^ *$pid \"`" ] && sleep 2
	    if [ -z "`ps | grep \"^ *$pid \"`" ]
	    then
		SIFS="$IFS" IFS=$'\n'
		dsize=$(for i in `find "$dpth/$dfile" ! -type d`; do stat -c "%s" "$i"; done | awk '{sum += $1} END{OFMT = "%.0f"; print sum}') 
		IFS="$SIFS"
		if [ "$ssize" = "$dsize" ]
		then
		    echo "<script type='text/javascript'>document.getElementById('result').innerHTML ='Finished';</script>"
		    #[ -z "`grep '^${pid}#' '${log_file}' | cut -d# -f5`" ] && sed -i -e "s/^\\(${pid}#.*\\)##\$/\\1#${time_now}#/g" "${log_file}"
		    break
		else
		    ####echo "<font color='red' size='+3'><b>ERROR copying file!</b></font><br><br>"
		    msg="<font color=\"red\" size=\"+3\"><b>ERROR copying file!</b></font><br><br>"
		    ###if [ -f "${log_dir}/${action}.error.${pid}.log" ]
		    if [ -f "${log_dir}/${action}.error.log" ]
		    then
			####echo "<font color='red' size='+2'>"
			msg="$msg<font color=\"red\" size=\"+2\">"
			###cat "${log_dir}/${action}.error.${pid}.log"
			####cat "${log_dir}/${action}.error.log"
			msg="$msg`cat ${log_dir}/${action}.error.log`"
			####echo "</font>"
			msg="$msg</font>"
			###rm -f "${log_dir}/${action}.error.${pid}.log"
		    fi
		    [ -n "$msg" ] && echo "<script type='text/javascript'>document.getElementById('result').innerHTML ='$msg';</script>"
		    error=1
		    break
		fi
		# TODO: need to rethink that as other processes might have started in meantime
		#rm -f "${log_dir}/${action}.error.log" "${log_dir}/${action}.log" "${log_file}"
	    fi
	    #[ -n "$msg" ] && echo "<script type='text/javascript'>document.getElementById('result').innerHTML ='$msg';</script>"
	    #sleep 15
	    if [ "${elapsed_status}" -gt "120" ]
	    then
		if [ "$pid" != "" ]
		then
		    echo "<script type='text/javascript'>window.location='${REQUEST_URI}&amp;onlystatus=1&amp;pid=${pid}';</script>"
		else
		    echo "<script type='text/javascript'>window.location='${REQUEST_URI}';</script>"
		fi
	    fi
	    sleep 2
	    counter=$(($counter+1))
	done
    fi
    if [ "$action" = "delete" ]
    then
	if [ "$spth" != "" -a "$spth" != "/" ]
	then
	    echo "<center><font size='+4' color='brown'><br><b>Removing: </font><br><br><font size='+3' color='blue'>$spth<br><br>...<br></font>"
	    if [ -e "$spth" ]
	    then
		rm -r "$spth" 2>&1
		if [ "$?" -ne "0" ]
		then
		    echo "<br><br><font color='red' size='+4'><b>ERROR</b></font><br>"
		    error=1
		fi
	    fi
	fi
    fi
    if [ "$error" != "1" ]
    then
	echo "<br><br><center><font color='green' size='+4'><b>DONE</b></font></center>"
	timeout=2000
    else
	timeout=8000
    fi
    if [ "$action" != "play" ]
    then
	echo "<script type=\"text/javascript\">"
	echo "function backToFM(){ window.location.replace('fm.cgi?type=related&amp;side=${side}&amp;lpth=${lpthx}&amp;rpth=${rpthx}&amp;select=${FORM_select}'); }"
	echo "window.timer = setTimeout(\"backToFM()\",$timeout);"
	echo "</script>"
    fi
fi

if [ "$action" != "copy" -a "$action" != "move" -a "$action" != "status" ]
then
    [ "$ftype" != "image" ] && echo -n '</div>'
    [ "$ftype" = "text" ] && echo -n "<div style='position: relative; text-align: center; align: center; margin: 0 auto;' width:'100%'><table width='99%' align='center'><tr><td><font color='yellow' size='+1'><b>OpenLGTV BCM FileManager</b> by xeros</font></td><td align='right'><font color='white'>viewed file: </font><font color='#00FF00'>$spth</font>&nbsp;</td><td style='width: 40px;'><input type='button' class='download' id='lpseudobutton' value='Download' onclick=\"window.location='tools/download.cgi?file=$spth';\" ></td></tr></table></div>"
    echo "</BODY></HTML>"
fi
#echo "STOP:`date`" >> /tmp/log.log

?>

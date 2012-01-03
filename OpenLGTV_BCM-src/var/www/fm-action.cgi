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
	height: 720px;
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
    }
</style>
<title>CGI FileManager by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

<?
log_dir=/tmp/var/log/fm
log_file="$log_dir/fm.log"
play_enum="$log_dir/last_played.info"
[ ! -d "$log_dir" ] && mkdir -p "$log_dir"

if [ -n "$FORM_side" ]
then
    export side="$FORM_side"
else
    export side="l"
fi

[ -n "$FORM_lpth" ]   && export lpth="$FORM_lpth"
[ -n "$FORM_rpth" ]   && export rpth="$FORM_rpth"
[ -n "$FORM_action" ] && export action="$FORM_action"
[ -n "$FORM_link" ]   && export link="$FORM_link"

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

echo "var side = '$side';"
echo "var lpth = '$lpth';"
echo "var rpth = '$rpth';"
echo "var xselect = '$xselect';"
echo "var refreshTime = '$FORM_timeout';"

?>

var col = 1; //number of 'cells' in a row
var current = 1;
var next = current;
//var side = 'l';
var side = 'r';
var nside = side;
var winWidth = window.innerWidth;
var winHeight = window.innerHeight;
var imgZoom = 0;
var h = 0;
var w = 0;

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
			//case 33: next = (1*current) - 30; break; //ch up
			//case 34: next = (1*current) + 30; break; //ch down
			case 37: next = current; nside = 'l'; break; //left
			//case 38: next = current - col; break; //up
			case 39: next = current; nside = 'r'; break; //right
			//case 40: next = (1*current) + col; break; //down
			}
		if (key==33|key==34|key==37|key==38|key==39|key==40)
			{
			if (next==0)
			    {
				next = 1;
			    }
			//Check if new link exists, if not then go to previous one until finds the one that exists
			if (!document.links['link_' + nside + next])
			{
			    do {
				next = next - 1;
			    } while ((!document.links['link_' + nside + next])&&(next >= 1));
			}
			ChangeBgColor();
			//Move to the next bookmark
			var code=document.links['link_' + nside + next].name;
			document.links['link_' + nside + next].focus();
			current = next;
			side = nside;
			//Prevent scrolling
			return false;
			}
		else if (key==13) 
			{
			switch(imgZoom)
				{
				case 0: resizeImage('image',imgZoom); imgZoom=1; break;
				case 1: resizeImage('image',imgZoom); imgZoom=2; break
				case 2: resizeImage('image',imgZoom); imgZoom=0; break;
				}
			return false;
			}
		else if (key==32) 
			{
			document.getElementById('link_' + side + current).click();
			return false;
			}
		else if ((key>47)&(key<60)) { window.refreshTime=(key-48)*2000; return false; }
		else if (key==461|key==27) 
			{
			//the back button on the remote control or ESC have been pressed
			//NetCastBack API
			//window.NetCastBack();
			//lets get back to WebUI instead of closing NetCast service
			<? 
			if [ "$action" != "play" ]
			then
			    echo "history.go(-1);"
			else
			    echo "backToFM();"
			fi
			?>
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
	document.getElementById('tr_' + side + current).bgColor = '#FFFFFF';
	document.getElementById('tr_' + nside + next).bgColor = '#D3D3D3';
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
	document.links['link_' + side + current].focus();
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
		case 2: pic.width = w*100; pic.height = h*100; break; // original image size
		}
	}

document.defaultAction = true;

<? echo "function backToFM(){ window.location.replace('fm.cgi?type=related&side=${side}&lpth=${lpthx}&rpth=${rpthx}&select=${xselect}'); }" ?>

// -->
</script>

<?
if [ "$action" = "play" ]
then
    ftype="`busybox stat -c '%F' "${spth}"`"
    ext="${spth##*.}"
    [ -n "$ext" ] && ext="`echo $ext | tr [:upper:] [:lower:]`"
    #play_enum="${spth}/last_played.info"
    ##play_enum="$log_dir/last_played.info"
    play_enum_comment="OpenLGTV BCM FileManager: last played file number"
    if [ "$ftype" = "directory" -o "$ext" = "m3u" -o "$ext" = "pls" ]
    then
	refresh=1
	file_num=1
	if [ "$ftype" = "directory" ]
	then
	    content_all=`busybox stat -c "%F@%n" "$spth"/* | grep "regular file" | grep -v "$play_enum" | sort | sed -e "s/regular file@//g" -e 's# #\&nbsp;#g'`
	else
	    spthd="${spth%/*}"
	    content_all=`grep -v "#" "$spth" | awk -F\n -v spthd="$spthd" '{print spthd "/" $1}' | sed -e 's# #\&nbsp;#g' -e 's/\r//g'`
	    #play_enum="${spth}.info"
	    spth="${spthd}"
	fi
	if [ ! -f "${play_enum}" ]
	then
	    echo -e "# $play_enum_comment\n1" > "${play_enum}"
	    start_playback=1
	else
	    start_playback=$((`grep -v "#" "${play_enum}"`+1))
	    echo -e "# $play_enum_comment\n$start_playback" > "${play_enum}"
	fi
	file_num_max="`echo $content_all | wc -w`"
	[ "$start_playback" -gt "$file_num_max" ] && echo -e "# $play_enum_comment\n1" > "${play_enum}" && start_playback=1
	for content in $content_all
	do
	    [ "$file_num" = "$start_playback" ] && spth="`echo $content | sed 's/\&nbsp;/ /g'`" && break
	    file_num=$((${file_num}+1))
	done
    fi
    ext="${spth##*.}"
    ext="`echo $ext | tr [:upper:] [:lower:]`"
    [ "$refresh" = "1" ] && [ "$ext" = "sh" -o "$ext" = "cgi" -o "$ext" = "htm" -o "$ext" = "html" ] && echo "<script type='text/javascript'>window.location.replace(window.location.href);</script></head><body></body></html>" && exit 0
    if [ "$ext" = "txt" -o "$ext" = "log" -o "$ext" = "ini" -o "$ext" = "info" -o "$ext" = "cfg" -o "$ext" = "conf" ]
    then
	ftype=text
    else
	if [ "$ext" = "jpg" -o "$ext" = "jpeg" -o "$ext" = "png" -o "$ext" = "gif" ]
	then
	    ftype=image
	else
	    echo "<script type='text/javascript'>"
	    if [ "$refresh" = "1" ]
	    then
		echo "setTimeout(\"window.location='root$spth'\",2000);"
	    else
		echo "setTimeout(\"window.location.replace('root$spth')\",2000);"
	    fi
	    echo "setTimeout(\"window.location.replace(window.location.href)\",4000);"
	    echo "</script>"
	fi
    fi
    [ "$refresh" = "1" ] && [ "$ftype" = "text" -o "$ftype" = "image" ] && echo "<script type='text/javascript'>var regexp=/timeout=[0-9]000/; setTimeout('window.location.replace(window.location.href.replace(regexp, \"timeout=\"+window.refreshTime))',window.refreshTime);</script>"
fi

?>

</HEAD>
<BODY bgcolor="black">

<?

[ "$ftype" != "text" ] && echo '<br/><center><font size="+4" color="yellow"><b>OpenLGTV BCM FileManager</b></font><br/><font size="+3" color="yellow">by xeros<br/><br/></font>'

[ "$ftype" != "image" ] && echo '<div style="width:95%; margin:auto; font-size:16px; background-color:white;">'

[ "$FORM_pid" != "" ] && pid="$FORM_pid"

if [ -n "$FORM_cancel" -a -n "$pid" ]
then
    process="`ps | grep \"^ *$pid \"`"
    if [ -n "$process" ]
    then
	echo "<font size='+3' color='red'><br/><b>Cancelling process:</b></font><font size='+3' color='black'><br/><br/>$process<br/><br/>"
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
    echo "setTimeout(\"backToFM()\",$timeout);"
    echo "</script>"
    echo "</font></div></center></body></head></html>"
    exit 0
fi

if [ "$action" = "play" ]
then
    [ "$refresh" = "1" ] && [ "$ftype" = "text" -o "$ftype" = "image" ] && echo '<font color="green" size="+2"><b><script>document.write("Refresh time set to: ", window.refreshTime/1000, " second[s] (use number buttons to change it [x2])");</script></b></font>'
    [ "$ftype" = "image" ] && echo "<br/><br/><font size='+2' color='yellow'><br/>Loading Image</font>"
    if [ "$ftype" = "text" ]
    then
	echo "<pre align='left'>"
	cat "$spth"
	echo "</pre>"
    else
	if [ "$ftype" = "image" ]
	then
	    echo "<div style='width:100%; height=100%; background-color:black; position:absolute; left:0px; top:0px; align=center; text-align=center;'><img id='image' onload=\"resizeImage('image',0);\" width='1%' src='root$spth'/></div>"
	else
	    echo "<center><font size='+4' color='brown'><br/><b>Starting playback of: </font><br/><br/><font size='+3' color='blue'>$spth<br/><br/>...<br/><br/></font>"
	fi
    fi
fi

[ -f "$log_file" -a "$action" = "status" ] && export FORM_confirm=yes

if [ "$FORM_confirm" != "yes" ]
then
    if [ "$action" != "play" ]
    then
	echo "<center><font size='+4' color='brown'><br/><b>"
	if [ "$action" = "copy" -o "$action" = "move" ]
	then
	    echo "Are you sure you want to ${action}?<br/><font size='+3' color='blue'><br/>$spth<br/><br/><font color='black' size='+3'>to</font><font size='+3' color='blue'><br/><br/>$dpth/</font>"
	else
	    if [ "$action" = "delete" ]
	    then
		echo "Are you sure you want to ${action}?<br/><font size='+2' color='black'><br/>$spth</font>"
	    else
		echo "No copy/move actions have been executed yet!<br/><br/>"
		echo '<script type="text/javascript">setTimeout("history.go(-1)",3000);</script>'
		exit 0
	    fi
	fi
	echo "</b><br/><br/></font>"
	echo "<table><tr><td id='tr_l1' width='200px' align='center'><b><a id='link_l1' href='${REQUEST_URI}&confirm=yes'><font size='+4'>Yes</font></a></b></td><td id='tr_r1' width='200px' align='center'><b><a id='link_r1' href='javascript:history.go(-1);'><font size='+4'>No</font></a></b></td></tr></table></center><br/><br/>"
    fi
else
    if [ "$action" = "copy" -o "$action" = "move" -o "$action" = "status" ]
    then
	if [ "$action" = "status" ]
	then
	    # TODO TODO TODO TODO
	    if [ -n "${pid}" ]
	    then
		stats="`grep '^${pid}#' ${log_file}`"
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
	    #stats="${stats#*\#}"
	    #time_start="${stats%%\#*}"
	    time_start="${stats##*\#}"
	    # TODO: what to do in this case?
	    #[ -z "${lpthx}" ] && lpthx="${spth%/*}"
	    #[ -z "${rpthx}" ] && rpthx="${dpth}"
	    [ -z "${side}"  ] && side="l"
	fi
	echo "<font size='+5' color='brown' style='text-transform: uppercase;'><b>$action in progress</b></font><br/><br/>"
	echo "<table>"
	echo "<tr><td><font size='+3' color='green'>Source: </font></td><td><font size='+3' color='black'>$spth</font><td></tr>"
	echo "<tr><td><font size='+3' color='green'>Target: </font></td><td><font size='+3' color='black'>$dpth/</font><td></tr>"
	echo "</table><br/>"
	echo "<br/>"
	SIFS="$IFS" IFS=$'\n'
	ssize=$(for i in `find "$spth" ! -type d`; do stat -c "%s" "$i"; done | awk '{sum += $1} END{OFMT = "%.0f"; print sum}') # could have been done with '-printf "%s\n"' or '-exec stat -c "%s" {}' as find arguments but busybox find does not support properly both of them
	IFS="$SIFS"
	if [ "$FORM_onlystatus" != "1" ]
	then
	    if [ "$action" = "copy" ]
	    then
		cp -r "$spth" "$dpth/" > "${log_dir}/${action}.error.log" 2>&1 &
		pid="$!"
	    else
		mv "$spth" "$dpth/" > "${log_dir}/${action}.error.log" 2>&1 &
		pid="$!"
	    fi
	    time_start="`date +'%s'`"
	    time_start_status="${time_start}"
	    echo "${pid}#${action}#${spth}#${dpth}#${time_start}" >> "${log_file}"
	else
	    [ -z "${time_start}" ] && time_start="`grep '${pid}' '${log_file}'`" && time_start="${time_start##*\#}"
	    time_start_status="`date +'%s'`"
	fi
	echo "<div id='status' style='font-size: 30px;'></div>"
	dfile="`basename "$spth"`"
	echo "<table><tr><td id='tr_l1' width='500px' align='center'><b><a id='link_l1' href='fm.cgi?type=related&side=${side}&lpth=${lpthx}&rpth=${rpthx}&select=${FORM_select}'><font size='+4'>Continue in background</font></a></b></td><td id='tr_r1' width='300px' align='center'><b><a id='link_r1' href='${REQUEST_URI}&pid=${pid}&cancel=1'><font size='+4'>Cancel</font></a></b></td></tr></table></center><br/><br/>"
	counter=0
	[ -z "$ssize" ] && ssize=1
	sleep 1
	for i in `seq 2000`
	do
	    SIFS="$IFS" IFS=$'\n'
	    dsize=$(for i in `find "$dpth/$dfile" ! -type d`; do stat -c "%s" "$i"; done | awk '{sum += $1} END{OFMT = "%.0f"; print sum}')
	    IFS="$SIFS"
	    [ "$dsize" = "" ] && dsize=0
	    percent="$(($dsize * 100 / $ssize))"
	    time_now="`date +'%s'`"
	    elapsed=$((${time_now}-${time_start}))
	    elapsed_status=$((${time_now}-${time_start_status}))
	    average_bps=$((${dsize}/${elapsed}))
	    average_kbps=$((${average_bps}/1024))
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
	    echo "<script type='text/javascript'>document.getElementById('status').innerHTML ='<font color=\"blue\">Copied:</font> $dsize_f / $ssize_f<br/><br/><font color=\"blue\">Progress:</font> $percent% &nbsp; <font color=\"blue\">Average speed:</font> $average_kbps KB/s<br/><br/><font color=\"blue\">Elapsed time:</font> $elapsed seconds<br/><br/>';</script>"
	    [ -n "`ps | grep \"^ *$pid \"`" ] && sleep 2
	    if [ -z "`ps | grep \"^ *$pid \"`" ]
	    then
		SIFS="$IFS" IFS=$'\n'
		dsize=$(for i in `find "$dpth/$dfile" ! -type d`; do stat -c "%s" "$i"; done | awk '{sum += $1} END{OFMT = "%.0f"; print sum}') 
		IFS="$SIFS"
		if [ "$ssize" -eq "$dsize" ]
		then
		    echo "Finished"
		    break
		else
		    echo "<font color='red' size='+3'><b>ERROR copying file!</b></font><br/><br/>"
		    if [ -f "${log_dir}/${action}.error.log" ]
		    then
			echo "<font color='red' size='+2'>"
			cat "${log_dir}/${action}.error.log"
			echo "</font>"
		    fi
		    error=1
		    break
		fi
		# TODO: need to rethink that as other processes might have started in meantime
		#rm -f "${log_dir}/${action}.error.log" "${log_dir}/${action}.log" "${log_file}"
	    fi
	    if [ "${elapsed_status}" -gt "120" ]
	    then
		if [ "$pid" != "" ]
		then
		    echo "<script type='text/javascript'>window.location='${REQUEST_URI}&onlystatus=1&pid=${pid}';</script>"
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
	    echo "<center><font size='+4' color='brown'><br/><b>Removing: </font><br/><br/><font size='+3' color='blue'>$spth<br/><br/>...<br/></font>"
	    rm -r "$spth" 2>&1
	    if [ "$?" -ne "0" ]
	    then
		echo "<br/><br/><font color='red' size='+4'><b>ERROR</b></font><br/>"
		error=1
	    fi
	fi
    fi
    if [ "$error" != "1" ]
    then
	echo "<br/><br/><center><font color='green' size='+4'><b>DONE</b></font></center>"
	timeout=2000
    else
	timeout=8000
    fi
    if [ "$action" != "play" ]
    then
	echo "<script type=\"text/javascript\">"
	echo "function backToFM(){ window.location.replace('fm.cgi?type=related&side=${side}&lpth=${lpthx}&rpth=${rpthx}&select=${FORM_select}'); }"
	echo "setTimeout(\"backToFM()\",$timeout);"
	echo "</script>"
    fi
fi
[ "$ftype" != "image" ] && echo '</div>'

?>
</BODY></HTML>

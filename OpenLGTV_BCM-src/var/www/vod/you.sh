#!/bin/sh
cat << WEB
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- you.sh by xeros -->
<!-- parser code from you.cgi by Oscar      -->
<!-- based on rssEx (by Serge.A.Timchenko)  -->

<!-- Source code released under GPL License -->

<style type="text/css">
    body {
	font-family:"TiresiasScreenfont";
	background-color:black;
    }
    a:link,a:visited {
	color:white;
	text-decoration:bold;
    }
    img {
	max-width:300px;
    }
    font,p {
	color: white;
    }
    a:hover,
    a:focus,
    a:active,
    font:hover,
    font:focus,
    font:active {
	color: #FF6633;
    }
</style>
<title>YouTube player</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

var current;
var next;
var col=1;
var rows=1;

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
			case 33: next = (1*current) - (rows*col); break; //ch up
			case 34: next = (1*current) + (rows*col); break; //ch down
			case 37: next = current - 1; break; //left
			case 38: next = current - col; break; //up
			case 39: next = (1*current) + 1; break; //right
			case 40: next = (1*current) + col; break; //down
			}
		if (key==33|key==34|key==37|key==38|key==39|key==40)
			{
			//Move to the next bookmark
			var code=document.links['link' + next].name;
			document.links['link' + next].focus();
			current = next;
			}
		else if (key==461) 
			{
			//the back button on the remote control have been pressed
			//NetCastBack API
			//window.NetCastBack();
			//lets get back to WebUI instead of closing NetCast service
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

function OnLoadSetCurrent(element)
	{
	current=1;
	if (document.links['link1']) document.links['link1'].focus();
	}

document.defaultAction = true;

-->

</script>

</HEAD>
<BODY>
WEB

item_nr=1

useragent="Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"

generateLink()
{
    echo "<tr><td><a id='link$item_nr' href='$6'>$3</a></td></tr>"
    item_nr=$(($item_nr+1))
}

unescapeXML()
{
    if [ -z "$1" ]
    then 
	sed 's/&gt;/>/g;s/&lt;/</g;s/&quot;/"/g;s/&amp;/\&/g;'
    else
	echo -n "$1" | sed 's/&gt;/>/g;s/&lt;/</g;s/&quot;/"/g;s/&amp;/\&/g;'
    fi
}

urldecode()
{
  awk '
  BEGIN{
  	for(i = 0; i < 10; i++)
  		hex[i] = i
  	hex["A"] = hex["a"] = 10
  	hex["B"] = hex["b"] = 11
  	hex["C"] = hex["c"] = 12
  	hex["D"] = hex["d"] = 13
  	hex["E"] = hex["e"] = 14
  	hex["F"] = hex["f"] = 15
  }
  {
  	gsub(/\+/, " ")
  	i = $0
  	while(match(i, /%../)){
  		if(RSTART > 1)
  			printf "%s", substr(i, 1, RSTART-1)
  		printf "%c", hex[substr(i, RSTART+1, 1)] * 16 + hex[substr(i, RSTART+2, 1)]
  		i = substr(i, RSTART+RLENGTH)
  	}
  	print i
  }
  '
}

log_dir="/var/log/vod/you"
log_file="$log_dir/you.log"
mkdir -p "$log_dir"
[ -f "$log_file" ] && rm -f "$log_file"

echo "<center><img src='../Images/tmp/youtube.png'/><br/><br/><font size='+3'>"

wget -q -O "$log_file" 'http://www.youtube.com/get_video_info?&video_id='$QUERY_STRING'&el=vevo&ps=default&eurl=' --user-agent="$useragent"

#FORMATS="5 x-flv FLV-240p 240 flv/34 x-flv FLV-360p 360 flv/35 x-flv FLV-480p 480 flv/18 mp4 MP4-360p 360 mp4/22 mp4 MP4-720p 720 mp4/37 mp4 MP4-1080p 1080 mp4"
FORMATS="mp4 1080 MP4-1080p mp4 mp4/37 720 MP4-720p mp4 mp4/22 360 MP4-360p mp4 flv/18 480 FLV-480p x-flv flv/35 360 FLV-360p x-flv flv/34 240 FLV-240p x-flv 5"

if [ ! -e "$log_file" ] || [ "`stat -c %s "$log_file"`" -le "100" ] || [ "`grep "status=fail" "$log_file" 2>/dev/null`" ]
then
    echo "Invalid request:<br/><font size='+2' style='color:red;'>$QUERY_STRING</font>"
    [ -e "$log_file" ] && echo "<br/><br/>Reason:<br/><font size='+2' style='color:#ff6600;'>`cat "$log_file" | sed 's/^.*reason=//g' | urldecode`</font>"
    echo "<script type='text/javascript'>setTimeout(\"history.back(-1)\",4000);</script>"
    echo "</font></center></BODY></HTML>"
    exit 0
fi

fmt_url_map=`grep -i 'url_encoded_fmt_stream_map=' "$log_file" | sed -n '1p'`

if [ -z "$fmt_url_map" ]
then
	fmt_url_map=`grep -i 'fmt_url_map=' "$log_file" | sed '1p'`
	fmt_url_map=`unescapeXML "$fmt_url_map" | awk '{match($0, /&fmt_url_map=([^&]*)&/, arr);print arr[1];}' | urldecode`
else
	fmt_url_map=`unescapeXML "$fmt_url_map" | sed 's/.*\&url_encoded_fmt_stream_map=url%3D\([^&]*\)\&.*/\1/g' | urldecode | urldecode`
fi

echo "Select source:<br/><br/><table>"

s=1
if [ -n `echo "$fmt_url_map" | grep -qs ",url="` ]; 
then
    #for TYP in 5 34 35 18 22 37
    for TYP in 37 22 18 35 34 5
    do
	stream_url=`echo "$fmt_url_map"  | awk 'BEGIN{RS=",url="} /itag='$TYP'/{print $0}' | sed 's/;.*//' | sed "s/\&itag\=$TYP//2"`
	if [ -n "$stream_url" ]
	then
	    parameters="`echo $FORMATS | cut -d/ -f$s`"
	    generateLink $parameters "$stream_url"
	fi
	let s=$s+1
    done
else
    #for TYP in 5 34 35 18 22 37
    for TYP in 37 22 18 35 34 5
    do
	stream_url=`echo $fmt_url_map | awk '{match($0,/.*'$TYP'\|([^,]+),?/,arr);print arr[1]}'`
	if [ -n "$stream_url" ]
	then
	    parameters="`echo $FORMATS | cut -d/ -f$s`"
	    generateLink $parameters "$stream_url"
	fi
	let s=$s+1
    done
fi

echo "</font></table></center>"
echo "</BODY></HTML>"

#!/usr/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>

<!-- tvp.cgi by xeros -->
<!-- Source code released under GPL License -->

<style type="text/css">
    body {
	font-family:"TiresiasScreenfont";
    }
    a:link,
    a:visited {
	color: black;
	background-color: lightblue;
	text-decoration: bold;
    }
    a:hover,
    a:focus,
    a:active {
	color: #CC0000;
	background-color: lightblue;
	text-decoration: bold;
    }
</style>
<title>tvp.pl alternative by xeros</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript">
<!--

var col  = 4; //number of 'cells' in a row
var rows = 5; //number of rows to jump on ch up/down
var current;
var next;

document.onkeydown = check;
//window.onload = OnLoadSetCurrent;
     
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
			//Move to the next item
			//Check if new link exists, if not then go to previous one until finds the one that exists
			if (next<=0)
			{
			    do {
				next = next + col;
			    } while (next<=0);
			}
			currentLink=document.links['link' + next];
			if (!currentLink)
			{
			    do {
				next = next - col;
				currentLink=document.links['link' + next];
			    } while ((!currentLink)&&(next >= 1));
			}
			var code=currentLink.name;
			currentLink.focus();
			current = next;
			//Prevent scrolling
			return false;
			}
		else if (key==404) 
			{
			//the green button on the remote control have been pressed
			//Switch to the Keyboard
			top.frames["Keyboard"].focus();
			}
		else if (key==415) 
			{
			//the play button on the remote control have been pressed
			//Try to play stream using MSDL
			var dest='../tools/msdl.sh?' + document.getElementById('link' + current).href;
			window.location=dest;
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

<?

useragent="Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"

menuLoc=""
log_dir="/var/log/vod/tvp"
prv=tvp

menus=" \
5#menu#Dla_Dzieci \
2919829#menu#Seriale \
1649945#menu#Seriale_komediowe \
4190002#category#Filmy_fabularne \
1381#category#Boso_przez_świat \
1364#category#Makłowicz_w_podróży \
1358#category#Rok_w_ogrodzie \
1885#category#Przegapiłes"

# Styl Zycia:
# 1352#menu#Styl_Zycia \
#  197917#menu#Adrenalina \
#  1353#menu#Dom_i_ogrod \
#  1360#menu#Kuchnia \
#  3830380#menu#Ludzie \
#  800#menu#Magazyny_sniadaniowe \
#  1380#menu#Podroze \
# Rozrywka:
# 699#menu#Rozrywka \
#  700#menu#Festiwale_i_koncerty \
#  784#menu#Programy_muzyczne \
#  812#menu#Programy_rozrywkowe \
#  879#menu#Programy_satyryczne \
#  903#menu#Teleturnieje \
#  920#menu#Wydarzenia \
# Seriale:
# 1518#menu#Seriale \
#  2919829#menu#Seriale_1 \
#  1649945#menu#Seriale_komediowe \
#  1591#menu#Seriale_obyczajowe \
#  1663#menu#Seriale_sensacyjne \
#  1091726#menu#Seriale_archiwalne \
#  1552#menu#Seriale_ostatnio_dodane \
# Sport:
# 432775#menu#Sport \
# Informacje:
# 190485#menu#Informacje \
# Publicystyka:
# 981#menu#Publicystyka \
#  982#menu#Ekonomia_i_gospodarka \
#  1059#menu#Polityka \
#   2625476#category#Polityka_przy_kawie \
#   1072#category#Tomasz_Lis_na_zywo \
#  1021#menu#Magazyny_reporterskie \
#   1046#category#Sprawa_dla_reportera \
#   1052#category#Celownik \
#  1086#menu#Tematyka_spoleczna \
#   1028#category#Ktokolwiek_widzial_ktokolwiek_wie \
# Filmoteka:
# 1028#menu#Filmoteka \
#  123913#menu#Film_dokumentalny \
#  150009#menu#Cykle_filmowe \
#  145979#menu#Wywiady_i_wydarzenia \
# Kultura:
# 426#menu#Kultura \
#  436#menu#Magazyny_kulturalne \
#  537#menu#Muzyka_powazna \
#  557#menu#Teatr \
#  583#menu#Literatura \
#  197313#menu#Wydarzenia \
#  497#menu#Mloda_sztuka \


if [ "$FORM_url" != "" ]
then
    url=`echo "$FORM_url" | tr '@$' '?&'`
    type="$FORM_type"
else
    url=""
    type=mainmenu
fi
log_file="$log_dir/$type.log"

pageTitle="$FORM_title"
img="$FORM_img"

[ "$type" = "mainmenu" ] && echo "col = 1;"

echo "// --></script>"

[ ! -d "$log_dir" ] && mkdir -p "$log_dir"

[ -n "$url" ] && wget -q -U "$useragent" -O - "$url" > $log_file

if [ "$type" = "video-tvp" ]
then
    grep "video_url" $log_file | sed -e 's/.*video_url="/<meta HTTP-EQUIV="REFRESH" content="1; url=/g' -e 's/">.*/">/g'
fi

echo '</HEAD><BODY bgcolor="lightblue">'

[ "$type" = "video-tvp" ] && echo "<center><img src='../Images/tmp/tvppl.png'/><font size='+2'><br/>alternative</font><br/>by xeros<br/></center><br/><font size='+3'><b><center>Wczytywanie wideo...</center></b></font>"

if [ "$type" = "mainmenu" ]
then
    echo '<center><img src="../Images/tmp/tvppl.png"/><font size="+2"><br/>alternative</font><br/>by xeros<br/></center><br/>'
    echo '<Table id="items" name="items" class="items" Border=0 cellspacing=0 width="100%">'
    echo '<tr>'
    item_nr=1
    for mnu in $menus
    do
	m_obj_id="${mnu%%\#*}"
	m_type="${mnu#*\#}"
	m_type="${m_type%%\#*}"
	m_txt="${mnu##*\#}"
	m_txt="${m_txt//_/ }"
	if [ "$m_type" = "menu" ]
	then
	    feedUrl="http://www.$prv.pl/pub/stat/websitelisting@object_id=${m_obj_id}\$child_mode=SIMPLE\$rec_count=64\$with_subdirs=true\$link_as_copy=true\$xslt=internet-tv/samsung/websites_listing.xslt\$q=\$samsungwidget=1\$v=2\$5"
	else
	    feedUrl="http://www.$prv.pl/pub/sess/samsungvideolistingwrapper@object_id=${m_obj_id}\$play_mode=VOD\$sort_by=RELEASE_DATE\$rec_count=128\$with_subdirs=true\$child_mode=SIMPLE\$xslt=internet-tv/samsung/website_details_wrapper.xslt\$with_video=true"
	fi
	feedTitle="$m_txt"
	feedType="$m_type"
	feedThumb=""
	echo "<td style='vertical-align:top;' valign='top'><center><a id=\"link${item_nr}\" href=\"tvp.cgi?type=${feedType}&title=${feedTitle}&url=${feedUrl}\">${feedThumb}<font size='+3' style='font-weight: 900;'><b>${feedTitle}</b></font></a></center><br/></td>"
	#[ "$(($item_nr % 4))" = "0" ] && echo "</tr><tr>"
	echo "</tr><tr>"
	[ "$item_nr" = "1" ] && echo "<script>OnLoadSetCurrent();</script>"
	item_nr=$(($item_nr+1))
    done
    echo '</tr>'
    echo '</table>'
fi

if [ "$type" = "menu" ]
then
    echo '<center><img src="../Images/tmp/tvppl.png" width="50" height="20" /><br/><font size="-1">alternative</font><br/></center>'
    echo '<Table id="items" name="items" class="items" Border=0 cellspacing=4 width="100%">'
    echo '<tr>'
    item_nr=1
    for content in `egrep -v 'version=|^$' $log_file | tr '\n\t' '|' | sed 's/<object/\n<object/g' | sed -e 's/.*url="//g' -e 's/\&amp;/\$/g' | awk -F\| '{print "http://www.tvp.pl" $1 ";" $2 ";" $3}' | sed -e 's/" view="ProgramView">;<title>/;/g' -e 's#</title>##g' -e 's/ /|/g'`
    do
	if [ "$content" != "http://www.$prv.pl;;" ]
	then
	    feedUrl="${content%%\;*}"
	    #feedUrl="${feedUrl/\$sort_by=RELEASE_DATE/}"
	    content2x="${content#*\;}"
	    feedTitle="${content2x%%\;*}"
	    content3x="${content2x#*\;}"
	    feedThumb="${content3x%%\;*}"
	    img="${feedThumb/*http/http}"
	    img="${img/\"*/}"
	    echo "<td width='25%' style='vertical-align:top;'><center><a id=\"link$item_nr\" href=\"tvp.cgi?type=category&img=${img}&title=${feedTitle}&url=$feedUrl\">$feedThumb<br/><font size='+2'>$feedTitle</font></a></center></td>" | tr '|' ' '
	    [ "$item_nr" = "1" ] && echo "<script>OnLoadSetCurrent();</script>"
	    [ "$(($item_nr % 4))" = "0" ] && echo "</tr><tr>"
	    item_nr=$(($item_nr+1))
	fi
    done
    echo '</tr>'
    echo '</table>'
else
    #pageTitle=`grep '<object' $log_file | sed 's/<object/\n<object/g' | grep -m1 'type="website"' | sed -e 's/.*<title>//' -e 's#</title>.*##'`
    echo "<center><font size='+2'><b>$pageTitle</b></font><br/></center>"
    echo '<Table id="items" name="items" class="items" style="border-spacing: 10px 4px;" Border="0" width="100%">'
    echo '<tr>'
    item_nr=1
    if [ "$type" = "category" ]
    then
	for content in `cat $log_file | sed 's/<object/\n<object/g' | grep "VideoView" | sed -e 's#"/><img.*"/>#"/>#g' -e 's/></>|</g' -e 's/.*url="//g' -e 's/\&amp;/\$/g' | \
			awk -F\| '{print "http://www.tvp.pl" $1 ";" $2 ";" $3}' | sed -e 's/;<title>/;/g' -e 's#</title>##g' -e 's/ /|/g' -e 's/">;<img/;<img/g' -e 's/xslt">;/xslt;/g'`
	do
	    feedUrl="${content%%\;*}"
	    content2x="${content#*\;}"
	    feedThumb="${content2x%%\;*}"
	    content3x="${content2x#*\;}"
	    feedTitle="${content3x%%\;*}"
	    [ -z "$img" ] && img="/Images/tmp/unknown.png"
	    [ -z "$feedThumb" ] && feedThumb="<img src='$img' width='141px' height='106px'>"
	    echo "<td width='140px'><center>$feedThumb</center></td><td width='25%'><a id=\"link$item_nr\" href=\"tvp.cgi?type=video-tvp&url=$feedUrl\" target=\"_parent\"><b><font size=\"+1\">$feedTitle</font></b></a></td>" | tr '|' ' '
	    [ "$item_nr" = "1" ] && echo "<script>OnLoadSetCurrent();</script>"
	    [ "$(($item_nr % 4))" = "0" ] && echo "</tr><tr cellpadding='10'>"
	    item_nr=$(($item_nr+1))
	done
	url="`echo $url | sed -e 's/sess\/samsungvideolistingwrapper/stat\/videolisting/' -e 's/xslt=internet-tv\/samsung\/website_details_wrapper.xslt/object_type=video/' | tr '?&' '@$'`"
	if [ "$item_nr" = 1 ]
	then
	    echo "<td width='100%' style='text-align: center;'><br/><font size='+3'>Brak udostępnianych materiałów wideo w tej kategorii!<br/></font><font size='+2'>Za chwilę nastąpi próba dostępu do materiałów w innym formacie...</font></td>"
	    #echo "<script>setTimeout(window.location.replace('tvp.cgi?type=category2&title=$pageTitle&img=$img&url=$url'),3);</script>"
	    echo "<script>window.location.replace('tvp.cgi?type=category2&title=$pageTitle&img=$img&url=$url');</script>"
	else
	    echo "<td width='140px'><center><img src='$img' width='141px' height='106px'></center></td><td width='25%'><a id=\"link$item_nr\" href=\"tvp.cgi?type=category2&title=$FORM_title&img=$img&url=$url\" target=\"_parent\"><b><font size=\"+1\">Materiały w innym formacie</font></b></a></td>" | tr '|' ' '
	fi
	#echo "$content" > "$log_file.txt"
    else
	# category2
	for content in `cat "$log_file" | sed 's/\(<video\)/\n\1/g' | grep "<video" | \
	    sed -e 's/<\(video\) .*zone_restriction_id="."><title>/|\1|/g' -e 's#</title><original_title.*"\([0-9a-z]*.jpg\)".*#|\1|#g' \
		-e 's#</title><original_title.*#|#g' -e 's/<video_format.*temp_sdt_url="//g' -e 's/" unique_id=.*"\([0-9a-f]*.jpg\)".*/|\1/g' \
		-e 's/" unique_id=.*//g' -e 's/^\(http:.*\)|\(.*\)/\2|\1/g' | grep -v "^<" | tr -d '\n' | \
	    sed -e 's/\(|video\)/\n\1/g' | sed -e 's/\([0-9a-f]*\.jpg\)[|0-9a-f]*\.jpg/\1/g' -e 's/http:.*\(http:[^|]*\)/\1/g' \
		-e 's/^\(|[^|]*|[^|]*|\)\(http\)/\1|\2/g' -e 's/^|video|//g' | grep -v '^$' | tr ' ' '#'`
	do
	    feedTitle="${content%%\|*}"
	    content2x="${content#*\|}"
	    feedThumb="${content2x%%\|*}"
	    [ -z "$img" ] && img="/Images/tmp/unknown.png"
	    # images suffixes:
	    # width_100_play_0_pos_3_gs_0 width_130_play_0_pos_0_gs_0_height_74 width_141 width_147_play_6_pos_5_gs_0 width_171_play_0_pos_0_gs_0_height_70 width_180_play_0_pos_3_gs_0 width_195_play_6_pos_5_gs_0_height_110 width_250_play_0_pos_0_gs_0_height_141 width_260_play_0_pos_0_gs_0_height_174
	    # play - cursor type (1 - white triangle on blue rectangle, 2 - flashblock style, 3 - hd, 4 - white triangle on green rectangle, 5 - white triangle on lightblue rectangle, 6 -  white triangle on red circle)
	    # pos - cursor position (0 & 3 - center, 1,2,4,5 - corners, 5 - right bottom corner)
	    # gs - black&white (0 - color, 1 - bw)
	    [ -n "$feedThumb" ] && feedThumb="<img src='http://s.v3.$prv.pl/images/${feedThumb:0:1}/${feedThumb:1:1}/${feedThumb:2:1}/uid_${feedThumb/.jpg/}_width_141_play_6_pos_5_gs_0.jpg'>" || feedThumb="<img src='$img' width='141px' height='106px'>"
	    content3x="${content2x#*\|}"
	    feedUrl="${content3x%%\|*}"
	    echo "<td width='140px'><center>$feedThumb</center></td><td width='25%'><a id=\"link$item_nr\" href=\"$feedUrl\" target=\"_parent\"><b><font size=\"+1\">$feedTitle</font></b></a></td>" | tr '#' ' '
	    [ "$item_nr" = "1" ] && echo "<script>OnLoadSetCurrent();</script>"
	    [ "$(($item_nr % 4))" = "0" ] && echo "</tr><tr cellpadding='10'>"
	    item_nr=$(($item_nr+1))
	    #echo "$content" >> "$log_file.txt"
	done
    fi
    echo '</tr>'
    echo '</table>'
fi

?>
</BODY></HTML>

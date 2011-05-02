#!/bin/haserl
# settings.cgi by xeros
# Source code released under GPL License
content-type: text/html

<html>
<? include/keycontrol.cgi.inc ?>

<font color="white">
<!-- ? for i in `cat /mnt/user/cfg/settings`; do echo "$i<br/>"; done ? -->
</font>

	<div style="position: absolute; left: 10px; top: 10px; width:860px">
		<form id="URL" name="URL">
			<? export pagename="Settings List" ?>
			<? include/header_links.cgi.inc ?>
			<? 
			id_nr=1
			rm -f /tmp/settings.save
			for i in `cat /mnt/user/cfg/settings | awk -F# '{print $1}'`
			do
			    opt_name=`echo $i | awk -F= '{print $1}'`
			    opt_val=`echo $i | awk -F= '{print $2}'`
			    opt_def="`grep ^$opt_name /mnt/user/cfg/settings.default`"
			    opt_desc="`echo $opt_def | awk -F# '{print $2}'`"
			    opt_def_val="`echo $opt_def | awk -F# '{print $1}' | awk -F= '{print $2}'`"
			    if [ "$FORM_save" = "1" ]
			    then
				eval opt_val=\$FORM_check$id_nr
				if [ "$opt_val" = "" ]
				then
				    opt_val=0
				fi
				echo "$opt_name=$opt_val" >> /tmp/settings.save
			    else
				opt_val=`echo $i | awk -F= '{print $2}'`
			    fi
			    opt_checked=`if [ "$opt_val" = "1" ]; then echo checked; fi`
			    echo "<div id=\"check"$id_nr"Parent\" style=\"background-color:white;height:32px;\">"
			    echo '<div style="position: relative; left: 5px; top: 5px; font-size: 18px;">'
			    echo "<input type=\"checkbox\" name=\"check$id_nr\" value=\"1\" $opt_checked><div style='display: inline-block; width: 290px; font-size: 16px;'>"
			    if [ "$opt_val" != "$opt_def_val" ]
			    then
				#echo "<font color='red'>"
				echo "<font color='#D30105'>"
			    else
				#echo "<font color='green'>"
				echo "<font color='#0E5900'>"
			    fi
			    echo "<b>$opt_name</b></font></div>"
			    echo "$opt_desc"
			    echo '</div>'
			    echo '</div>'
			    id_nr=$((id_nr+1))
			done 
			?>
			<input type="hidden" name="save" value="1">
			<div id="textOnly" style="background-color:white;height:40px;">
				<div style="position: relative; left: 5px; top: 5px;">
				    <?
					if [ "$FORM_save" = "1" ]
					then
					    if [ -f "/tmp/settings.save" ]
					    then
						mv /mnt/user/cfg/settings /mnt/user/cfg/settings.bck
						mv /tmp/settings.save /mnt/user/cfg/settings
						echo "OpenLGTV_BCM-INFO: WebUI: Settings file: /mnt/user/cfg/settings changed by WebUI..." >> /var/log/OpenLGTV_BCM.log
					    fi
					    echo '<center><font size="+3" color="red"><b><span id="spanSAVED">SETTINGS SAVED !!!</span></b></font></center>'
					else
					    echo '<center><font size="+2" color="red"><b>Be very careful when changing settings !!!</b></font></center>'
					fi
				    ?>
				</div>
			</div>
		</form>
	</div>	
</body>
</html>

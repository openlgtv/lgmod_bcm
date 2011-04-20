#!/bin/haserl
content-type: text/html

<html>
<? cat /var/www/include/keycontrol.html.inc ?>

<font color="white">
<!-- ? for i in `cat /mnt/user/cfg/settings`; do echo "$i<br/>"; done ? -->
</font>

	<div style="position: absolute; left: 10px; top: 10px; width:600px">
		<form id="URL" name="URL">
			<? export pagename="Settings List" ?>
			<? include/header_links.cgi.inc ?>
			
			<? 
			id_nr=1
			rm -f /tmp/settings.save
			for i in `cat /mnt/user/cfg/settings`
			do
			    opt_name=`echo $i | awk -F= '{print $1}'`
			    opt_val=`echo $i | awk -F= '{print $2}'`
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
			    echo '<div style="position: relative; left: 5px; top: 5px;">'
			    ##echo $opt_val $opt_checked 
			    #echo "<input type=\"checkbox\" name=\"check$id_nr\" value=\"$opt_val\" $opt_checked> $opt_name"
			    echo "<input type=\"checkbox\" name=\"check$id_nr\" value=\"1\" $opt_checked> $opt_name"
			    echo '</div></div>'
			    id_nr=$((id_nr+1))
			done 
			?>
			<input type="hidden" name="save" value="1">
			<div id="textOnly" style="background-color:white;height:64px;">
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
					    echo '<center><font size="+2" color="red"><b>SETTING SAVED !!!</b></font></center>'
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

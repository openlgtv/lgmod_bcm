#!/bin/haserl
# home.cgi by xeros
# Source code released under GPL License
content-type: text/html

<html>
<? include/keycontrol.cgi.inc ?>

	<div style="position: absolute; left: 10px; top: 10px; width:860px; font-size:16px;">
		<form id="URL" name="URL">
			<? export pagename="Home Page" ?>
			<? include/header_links.cgi.inc ?>
			<? 
			  if [ "$FORM_run" = "Run" -a "$FORM_qURL" != "" ]
			  then
			    # Lets make more space for command output
			    echo "<div id=\"textOnly\" style=\"background-color:white\"><!--"
			  else
			    echo "<div id=\"textOnly\" style=\"background-color:white;height:160px;\">"
			  fi
			?>
				<div style="position: relative; left: 5px; top: 5px;">
					<br />
					<b><font size="+1">LG rootfs version:</font></b> <? cat /etc/ver | awk -F, '{print $1}' ?><br />
					<b><font size="+1">LG Web Browser version:</font></b> <? cat /mnt/browser/run3556 | grep Revision: | awk -F: '{print $2}' | sed 's/\"//g' ?><br />
					<b><font size="+1">Web Browser User Agent string:</font></b> <br />
					<font size="-1"><? echo "$HTTP_USER_AGENT" ?></font>
				</div>
			</div>
			<? 
			  if [ "$FORM_run" = "Run" -a "$FORM_qURL" != "" ]
			  then
			    echo "-->"
			  fi
			?>
			<div id="txtURLParent" style="background-color:white;height:60px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 0px; height:30;">
					<b>Shell command to execute: (use Save button to execute)</b>
				</div><div style="position: relative; left: 5px">
				    <input id="txtURL" name="qURL" type="textarea" style="width:695px" onFocus='javascript:PageElements[currElementIndex].focused=true;' onBlur='javascript:PageElements[currElementIndex].focused=false;' value="<? echo $src ?>"/>
				</div>
			</div>
			<input type="hidden" name="run" value="Run">
			<!-- execute code from form input - originally from tools.cgi in LGMOD -->
			<?
			 if [ "$FORM_run" = "Run" -a "$FORM_qURL" != "" ]; then
			    echo "<div style=\"background-color: white; position: relative; left: 0px\">"
			    echo "<font size=\"-1\"><b> Output from:</b> $FORM_qURL"
			    echo "<pre>"
			    echo -n "$FORM_qURL" > /tmp/shell_command.sh
			    dos2unix /tmp/shell_command.sh
			    chmod +x /tmp/shell_command.sh
			    /tmp/shell_command.sh > /tmp/shell_command.out 2>&1
			    sync
			    cat /tmp/shell_command.out
			    echo "</pre>"
			    echo "</font>"
			    echo "</div>"
			 fi
			?>
			<div id="txtUserParent" style="background-color:white;height:30px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 7px; height:23;">
					New WebUI/Telnet/SSH Password: 
				</div>
				<div style="position: relative; left: 300px; top: -22px;">
					<input id="txtUser" name="qUser" type="textarea" style="width:400px" onFocus='javascript:PageElements[currElementIndex].focused=true;' onBlur='javascript:PageElements[currElementIndex].focused=false;' value=""/>
				</div>
			</div>
			<div id="txtPasswParent" style="background-color:white;height:30px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 7px; height:23;">
					Confirm New Password: 
				</div>
				<div style="position: relative; left: 300px; top: -22px;">
					<input id="txtPassw" name="qPassw" type="textarea" style="width:400px" onFocus='javascript:PageElements[currElementIndex].focused=true;' onBlur='javascript:PageElements[currElementIndex].focused=false;' value=""/>
				</div>
			</div>
			<?
			 if [ "$FORM_run" = "Run" -a "$FORM_qPassw" != "" -a "$FORM_qUser" = "$FORM_qPassw" ]
			 then
			    cur_encPassw="`grep ^root: /mnt/user/etc/shadow | awk -F: '{print $2}'`"
			    new_encPassw="`httpd -m $FORM_qPassw`"
			    #sed -i -e "s/^\(root:\).*\(:.*\)/\1$FORM_qPassw\2/g" /mnt/user/etc/shadow 2>&1
			    echo "OpenLGTV BCM-INFO: WebUI: password change" >> /var/log/OpenLGTV_BCM.log
			    sed -i -e "s:^root\:$cur_encPassw:root\:$new_encPassw:g" /mnt/user/etc/shadow 2>&1 | tee -a /var/log/OpenLGTV_BCM.log
			    echo '<div style="background-color:white;"><center><font size="+3" color="red"><b><span id="spanPASSSET">NEW PASSWORD SET !!!</span></b></font><br/><b>Password change to WebUI will take effect after reboot!</b></center></div>'
			 fi
			?>

		</form>
	</div>	


</body>
</html>

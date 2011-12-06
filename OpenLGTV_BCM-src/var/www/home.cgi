#!/bin/haserl --upload-limit=14096 --upload-dir=/tmp
# home.cgi by xeros
# Source code released under GPL License
content-type: text/html

<html>
<? include/keycontrol.cgi.inc ?>

<script language="JavaScript" type="text/javascript">
function GoToNetCastLinks()
	{
	<?
		if [ -n "`pgrep -f run3556-proxy`" -a "$HTTP_HOST" = "127.0.0.1:88" ]
		then
		    echo "window.location='http://$HTTP_HOST/home.cgi?qURL=/mnt/browser/run3556+http://$HTTP_HOST/browser/links.html&run=Run&qUser=&qPassw=';"
		else
		    echo "window.location='browser/links.html';"
		fi
	?>
	}
</script>

	<div style="position: absolute; left: 10px; top: 10px; width:880px; font-size:16px;">
		<form id="URL" name="URL">
			<? 
			  export pagename="Home Page"
			
			  include/header_links.cgi.inc
			
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
					<b><font size="+1">LG Web Browser version:</font></b> <? grep Revision: /mnt/browser/run3556 | awk -F: '{print $2}' | sed 's/\"//g' ?><br />
					<b><font size="+1">Web Browser User Agent string:</font></b><br />
					<font size="-1"><? echo "$HTTP_USER_AGENT" ?></font>
				</div>
			<? 
			  if [ "$FORM_run" = "Run" -a "$FORM_qURL" != "" ]
			  then
			    echo "-->"
			  fi
			?>
			</div>
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
			<div id="txtPinParent" style="background-color:white;height:30px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 7px; height:23;">
					WebUI [TV] PIN (type '0' to disable): 
				</div>
				<div style="position: relative; left: 300px; top: -22px;">
					<input id="txtPin" name="qPin" type="textarea" style="width:400px" onFocus='javascript:PageElements[currElementIndex].focused=true;' onBlur='javascript:PageElements[currElementIndex].focused=false;' value=""/>
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
			 if [ "$FORM_run" = "Run" -a "$FORM_qPin" != "" ]
			 then
			    pin="$FORM_qPin"
			    if [ "$pin" != "0" ]
			    then
				echo "OpenLGTV BCM-INFO: WebUI: pin change" >> /var/log/OpenLGTV_BCM.log
				echo "$pin" > /mnt/user/cfg/pin
				echo "<div style='background-color:white;'><center><font size='+3' color='red'><b><span id='spanPASSSET'>NEW PIN TO WEBUI SET: $pin !!!</span></b></font><br/><b></b></center></div>"
			    else
				echo "OpenLGTV BCM-INFO: WebUI: pin disable" >> /var/log/OpenLGTV_BCM.log
				echo "" > /mnt/user/cfg/pin
				echo '<div style="background-color:white;"><center><font size="+3" color="red"><b><span id="spanPASSSET">PIN TO WEBUI - DISABLED !!!</span></b></font><br/><b></b></center></div>'
			    fi
			 fi
			?>
		</form>
	</div>
	<? if [ "$FORM_run" = "Run" -a "$FORM_qURL" != "" ]
	then
	    echo "<!--"
	fi 

if [ "$HTTP_HOST" = "127.0.0.1:88" ]; then echo "<!-- "; fi ?>
<div style="position: absolute; left: 5px; bottom: 110px; height:85; background-color:red; border: 1px solid #D3D3D3;">
<div class="posthead"><center>Upload the firmware file (*.epk) to first partition of USB drive connected to USB1 port (FAT32 or NTFS)&nbsp;<br/>
		              into LG_DTV dir if it's LG upgrade or (*.tar.sh) into OpenLGTV_BCM/upgrade if it's OpenLGTV BCM upgrade.</center></div><div class="posttext">
<form action="cgi-bin/firmware-upgrade.cgix" method="post" enctype="multipart/form-data" >
    <center><input type=file name=uploadfile><input type=submit value=Upload><br/>
    Select file and press Upload button. &nbsp; [OPTION AVAILABLE ONLY REMOTELY] &nbsp;</center>
</form>
</div></div>
<? if [ "$HTTP_HOST" = "127.0.0.1:88" ]; then echo "-->"; fi ?>

	<div id="footer2" class="footer2">
		<ul>
			<a onClick="javascript:window.location='home.cgi?qURL=reboot&run=Run';" href="#" style="text-decoration:none; color:white"><li class=""><span><img src="Images/Keyboard/stop_button.png" border="0" /></span>Reboot TV</li></a>
		</ul>
		<ul>
			<a onClick="javascript:window.location='remote';" href="#" style="text-decoration:none; color:white"><li class="">Remote control</li></a>
		</ul>
		<ul>
			<a onClick="javascript:GoToNetCastLinks();" href="#" style="text-decoration:none; color:white"><li class=""><span><img src="Images/Keyboard/info_button.png" border="0" /></span>NetCast</li></a>
		</ul>
		<ul>
			<a onClick="javascript:window.location='home.cgi?qURL=/scripts/reset_configs_netcast.sh&run=Run';" href="#" style="text-decoration:none; color:red"><li class="">NetCast cfg rst</li></a>
		</ul>
		<ul>
			<a onClick="javascript:window.location='home.cgi?qURL=/scripts/reset_configs.sh&run=Run';" href="#" style="text-decoration:none; color:white"><li class="">&nbsp;All cfg reset</li></a>
		</ul>
	</div>
	<? if [ "$FORM_run" = "Run" -a "$FORM_qURL" != "" ]
	then
	    echo "-->"
	fi ?>

</body>
</html>

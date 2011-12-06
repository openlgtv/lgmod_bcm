#!/bin/haserl
# mount-edit.cgi by xeros, nicola_12345
# Source code released under GPL License
content-type: text/html

<html>
<? include/keycontrol.cgi.inc ?>
	<div style="position: absolute; left: 10px; top: 10px; width:880px; font-size:16px;">
		<form id="URL" name="URL" action="mount-edit.cgi" method="GET">
			<? 
			    if [ "$FORM_type" = "etherwake" ]
			    then
				input_file=/mnt/user/cfg/ethwaketab
				export pagename="Ether Wake"
			    else
				input_file=/mnt/user/cfg/ndrvtab
				export pagename="Network Shares"
			    fi
			    include/header_links.cgi.inc
			?>
			<div id="textOnly" style="background-color:white;height:50px;">
				<div style="position: relative; left: 5px; top: 0px;">
					<? [ "$FORM_type" != "etherwake" ] && echo "<br /><center><b>Note: Relative destination mount paths need FAT/NTFS formated USB storage device.</b></center><br />" ?>
					<? [ "$FORM_type" = "etherwake" ]  && echo "<br /><center><b>Wake remotely machines which support WakeOnLan feature</b></center><br />" ?>
				</div>
			</div>

<?
# 0|1#cifs|nfs#[url]#NetShare(mount path on USB stick)#[options]#[username]#[password] - up to 0.5.0-beta1
# 0|1#cifs|nfs#[url]#NetShare(mount path on USB stick)#[options]#[username]#[password]#[0|1] - changed by 0.5.0-beta2 (added field for dir listing cache)

id="$FORM_id"

if [ "$FORM_qURL" != "" -a "$FORM_radio1" != "" -a "$id" != "" ]
then
    automount=0
    precache=0
    [ "$FORM_check1" = "automount" ] && automount=1
    [ "$FORM_check2" = "precache" ]  && precache=1
    cp -f ${input_file} ${input_file}.bck
    if [ "$FORM_qPath" != "" ]
    then
	qPath="$FORM_qPath"
    else
	qPath="NetShare"
    fi
    if [ "`cat ${input_file} | wc -l`" -lt "$id" ]
    then
	if [ "$FORM_type" = "etherwake" ]
	then
	    # (autowake on boot:0/1)#(hostname)#[ip.address]#(MAC:address)#[pa:ss:wo:rd]#[options]#
	    echo "$automount#$FORM_qURL#$FORM_qUser#$FORM_qPassw#$qPath##" >> ${input_file}
	else
	    echo "$automount#$FORM_radio1#$FORM_qURL#$qPath##$FORM_qUser#$FORM_qPassw#$precache" >> ${input_file}
	fi
    else
	if [ "$FORM_type" = "etherwake" ]
	then
	    sed -i -e "$id s?.*?$automount#$FORM_qURL#$FORM_qUser#$FORM_qPassw#$qPath##?" ${input_file}
	else
	    sed -i -e "$id s?.*?$automount#$FORM_radio1#$FORM_qURL#$qPath##$FORM_qUser#$FORM_qPassw#$precache?" ${input_file}
	fi
    fi
fi

if [ -f "${input_file}" -a "$id" != "" ]
then
    ndrv="`head -n $FORM_id ${input_file} | tail -n 1`"
    ndrv_2="${ndrv#*\#}"
    ndrv_3="${ndrv_2#*\#}"
    ndrv_4="${ndrv_3#*\#}"
    ndrv_5="${ndrv_4#*\#}"
    ndrv_6="${ndrv_5#*\#}"
    ndrv_7="${ndrv_6#*\#}"
    ndrv_8="${ndrv_7#*\#}"
    automount="${ndrv%%#*}"
    if [ "$FORM_type" = "etherwake" ]
    then
	automntname="AutoWake on boot"
	ew_autowake="${ndrv%%#*}"
	ew_name="${ndrv_2%%#*}"
	ew_ip="${ndrv_3%%#*}"
	ew_mac="${ndrv_4%%#*}"
	ew_pass="${ndrv_5%%#*}"
	ew_opt="${ndrv_6%%#*}"
	# ugly variables but make the code changes minimal
	src="${ew_name}"
	uname="${ew_ip}"
	pass="${ew_mac}"
	dst="${ew_pass}"
    else
	automntname="AutoMount"
	fs_type="${ndrv_2%%#*}"
	src="${ndrv_3%%#*}"
	dst="${ndrv_4%%#*}"
	opt="${ndrv_5%%#*}"
	uname="${ndrv_6%%#*}"
	pass="${ndrv_7%%#*}"
	precache="${ndrv_8%%#*}"
    fi
fi

mount_err_code=0

if [ "$FORM_mount" = "1" ]
then
    echo "OpenLGTV_BCM-INFO: WebUI: NetShare mounts - trying to mount NetShare id: $id by WebUI..." >> /var/log/OpenLGTV_BCM.log
    /etc/rc.d/rc.mount-netshare WebUI_MOUNT "$id" >> /var/log/OpenLGTV_BCM.log 2>&1
    export mount_err_code="$?"
fi

if [ "$FORM_wake" = "1" ]
then
    echo "OpenLGTV_BCM-INFO: WebUI: EtherWake - trying to wake id: $id by WebUI..." >> /var/log/OpenLGTV_BCM.log
    /etc/rc.d/rc.ether-wake WebUI_WAKE "$id" >> /var/log/OpenLGTV_BCM.log 2>&1
    export mount_err_code="$?"
fi

if [ "$mount_err_code" -ne "0" ]
then
    export mounting_error=1
fi

[ "$dst" = "" ] && dst="NetShare"

if [ "$FORM_umount" = "1" ]
then
    share_path="`grep -m 1 "$dst " /proc/mounts | cut -d' ' -f2`"
    echo "OpenLGTV_BCM-INFO: WebUI: NetShare mounts - trying to unmount NetShare: $share_path id: $id by WebUI..." >> /var/log/OpenLGTV_BCM.log
    umount "$share_path" >> /var/log/OpenLGTV_BCM.log 2>&1
fi

?>
			<center>
			    <div id="link11Parent" style="background-color:white;height:40px;">
				<?
				    action=mount
				    if [ -z "`grep "$dst " /proc/mounts`" ]
				    then
					if [ -f "${input_file}" ]
					then
					    input_rest="value=\"Mount\" style=\"width:100px\""
					else
					    input_rest="value=\"Mount button: You need to save first to be able to mount\" style=\"width:600px\" disabled"
					fi
				    else
					action=umount
					input_rest="value=\"Unmount\" style=\"width:400px\""
				    fi
				    [ "$FORM_type" = "etherwake" ] && action=wake && input_rest="value=\"Wake\" style=\"width:100px\""
				    echo -n "<input type=\"button\" id=\"link11\" onKeyPress=\"javascript:window.location='mount-edit.cgi?${action}=1&id=${id}&type=${FORM_type}';\" onClick=\"javascript:window.location='mount-edit.cgi?mount=1&id=${id}&type=${FORM_type}';\" ${input_rest} />"
				?>
			    </div>
			</center>
			<div id="txtURLParent" style="background-color:white;height:40px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 7px; height:23;">
					<?
					    if [ "$FORM_type" = "etherwake" ]
					    then
						echo "Name:"
					    else
						echo "URL:"
					    fi
					?>
				</div>
				<div style="position: relative; left: 100px; top: -22px;">
				    <input id="txtURL" name="qURL" type="textarea" style="width:400px" onFocus='javascript:PageElements[currElementIndex].focused=true;' onBlur='javascript:PageElements[currElementIndex].focused=false;' value="<? echo $src ?>"/>
				</div>
			</div>
			<div id="txtUserParent" style="background-color:white;height:40px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 7px; height:23;">
					<?
					    if [ "$FORM_type" = "etherwake" ]
					    then
						echo "IP address:"
					    else
						echo "Username:"
					    fi
					?>
				</div>
				<div style="position: relative; left: 100px; top: -22px;">
					<input id="txtUser" name="qUser" type="textarea" style="width:400px" onFocus='javascript:PageElements[currElementIndex].focused=true;' onBlur='javascript:PageElements[currElementIndex].focused=false;' value="<? echo $uname ?>"/>
				</div>
			</div>
			<div id="txtPasswParent" style="background-color:white;height:40px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 7px; height:23;">
					<?
					    if [ "$FORM_type" = "etherwake" ]
					    then
						echo "MAC:"
					    else
						echo "Password:"
					    fi
					?>
				</div>
				<div style="position: relative; left: 100px; top: -22px;">
					<input id="txtPassw" name="qPassw" type="textarea" style="width:400px" onFocus='javascript:PageElements[currElementIndex].focused=true;' onBlur='javascript:PageElements[currElementIndex].focused=false;' value="<? echo $pass ?>"/>
				</div>
			</div>
			<div id="txtPathParent" style="background-color:white;height:40px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 7px; height:23;">
					<?
					    if [ "$FORM_type" = "etherwake" ]
					    then
						echo "Password:"
					    else
						echo "Mount path:"
					    fi
					?>
				</div>
				<div style="position: relative; left: 100px; top: -22px;">
					<input id="txtPath" name="qPath" type="textarea" style="width:400px" onFocus='javascript:PageElements[currElementIndex].focused=true;' onBlur='javascript:PageElements[currElementIndex].focused=false;' value="<? echo $dst ?>"/>
				</div>
			</div>
			<? [ "$FORM_type" = "etherwake" ] && echo "<!--" ?>
			<div id="radio1Parent" style="background-color:white;height:40px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 5px;">
					Network Protocol: 
					<? if [ "$fs_type" = "cifs" ]
					   then
					       echo '<input type="radio" name="radio1" value="cifs" checked> CIFS'
					       echo '<input type="radio" name="radio1" value="nfs"> NFS'
					   else
					       echo '<input type="radio" name="radio1" value="cifs"> CIFS'
					       echo '<input type="radio" name="radio1" value="nfs" checked> NFS'
					   fi ?>
				</div>
			</div>
			<? [ "$FORM_type" = "etherwake" ] && echo "-->" ?>
			<div id="check1Parent" style="background-color:white;height:40px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 5px;">
				<? if [ "$automount" = "1" ]
				   then
					echo "<input type='checkbox' name='check1' value='automount' checked> $automntname"
				   else
					echo "<input type='checkbox' name='check1' value='automount'> $automntname"
				   fi ?>
				</div>
			</div>
			<? [ "$FORM_type" = "etherwake" ] && echo "<!--" ?>
			<div id="check2Parent" style="background-color:white;height:40px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 5px;">
				<? if [ "$precache" = "1" ]
				   then
					echo '<input type="checkbox" name="check2" value="precache" checked> Precache directory listing for media player (do not enable when there is no invisible dirs problem)'
				   else
					echo '<input type="checkbox" name="check2" value="precache"> Precache directory listing for media player (do not enable when there is no invisible dirs problem)'
				   fi ?>
				</div>
			</div>
			<? [ "$FORM_type" = "etherwake" ] && echo "--><input type='hidden' name='type' value='etherwake'><input type='hidden' name='radio1' value='etherwake'>" ?>
			<input type="hidden" name="save" value="1">
			<? echo "<input type='hidden' name='id' value='$id'>" ?>
			<div id="textOnly" style="background-color:white;height:64px;">
				<div style="position: relative; left: 5px; top: 5px;">
				    <?
					if [ "$FORM_save" = "1" ]
					then
					    echo "OpenLGTV_BCM-INFO: WebUI: NetShare mounts file: ${input_file} changed by WebUI..." >> /var/log/OpenLGTV_BCM.log
					    echo '<center><font size="+3" color="red"><b><span id="spanSAVED">SETTINGS SAVED !!!</span></b></font></center>'
					else
					    if [ "$mounting_error" = "1" ]
					    then
						echo "<center><font size=\"+2\" color=\"red\"><b>Mounting ERROR with error code: $mount_err_code !!!<br />Check your logs and settings!</b></font></center>"
					    else
						echo '<br /><center><font size="+2" color="red"><b>Remember to save settings before trying to use mount button</b></font></center>'
					    fi
					fi
				    ?>
				</div>
			</div>
		</form>
	</div>	
</body>
</html>

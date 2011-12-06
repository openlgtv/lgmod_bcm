#!/bin/haserl
# mount-edit.cgi by xeros, nicola_12345
# Source code released under GPL License
content-type: text/html

<html>
<? include/keycontrol.cgi.inc ?>
	<div style="position: absolute; left: 10px; top: 10px; width:860px; font-size:16px;">
		<form id="URL" name="URL" action="mount-edit.cgi" method="GET">
			<? 
			    export pagename="Network Share Mounts"
			    include/header_links.cgi.inc
			?>
			<div id="textOnly" style="background-color:white;height:50px;">
				<div style="position: relative; left: 5px; top: 0px;">
					<br />
					<center><b>Note: Relative destination mount paths need FAT/NTFS formated USB storage device.</b></center><br />
				</div>
			</div>

<?
# 0|1#cifs|nfs#[url]#NetShare(mount path on USB stick)#[options]#[username]#[password] - up to 0.5.0-beta1
# 0|1#cifs|nfs#[url]#NetShare(mount path on USB stick)#[options]#[username]#[password]#[0|1] - changed by 0.5.0-beta2 (added field for dir listing cache)

id="$FORM_id"

if [ "$FORM_qURL" != "" -a "$FORM_radio1" != "" -a "$id" != "" ]
then
    if [ "$FORM_check1" = "automount" ]
    then
	automount=1
    else
	automount=0
    fi
    if [ "$FORM_check2" = "precache" ]
    then
	precache=1
    else
	precache=0
    fi
    cp -f /mnt/user/cfg/ndrvtab /mnt/user/cfg/ndrvtab.bck
    if [ "$FORM_qPath" != "" ]
    then
	qPath="$FORM_qPath"
    else
	qPath="NetShare"
    fi
    
    if [ "`cat /mnt/user/cfg/ndrvtab | wc -l`" -lt "$id" ]
    then
	echo "$automount#$FORM_radio1#$FORM_qURL#$qPath##$FORM_qUser#$FORM_qPassw#$precache" >> /mnt/user/cfg/ndrvtab
    else
	sed -i -e "$id s?.*?$automount#$FORM_radio1#$FORM_qURL#$qPath##$FORM_qUser#$FORM_qPassw#$precache?" /mnt/user/cfg/ndrvtab
    fi
fi

if [ -f "/mnt/user/cfg/ndrvtab" -a "$id" != "" ]
then
    ndrv="`head -n $FORM_id /mnt/user/cfg/ndrvtab | tail -n 1`"
    automount="${ndrv%%#*}"
    ndrv_2="${ndrv#*\#}"
    fs_type="${ndrv_2%%#*}"
    ndrv_3="${ndrv_2#*\#}"
    src="${ndrv_3%%#*}"
    ndrv_4="${ndrv_3#*\#}"
    dst="${ndrv_4%%#*}"
    ndrv_5="${ndrv_4#*\#}"
    opt="${ndrv_5%%#*}"
    ndrv_6="${ndrv_5#*\#}"
    uname="${ndrv_6%%#*}"
    ndrv_7="${ndrv_6#*\#}"
    pass="${ndrv_7%%#*}"
    ndrv_8="${ndrv_7#*\#}"
    precache="${ndrv_8%%#*}"
fi

if [ "$FORM_mount" = "1" ]
then
    echo "OpenLGTV_BCM-INFO: WebUI: NetShare mounts - trying to mount NetShare id: $id by WebUI..." >> /var/log/OpenLGTV_BCM.log
    /etc/rc.d/rc.mount-netshare WebUI_MOUNT "$id" >> /var/log/OpenLGTV_BCM.log 2>&1
    export mount_err_code="$?"
    if [ "$mount_err_code" -ne "0" ]
    then
	export mounting_error=1
    fi
fi

if [ "$dst" = "" ]
then
    dst="NetShare"
fi

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
				    if [ -z "`grep "$dst " /proc/mounts`" ]
				    then
					if [ -f "/mnt/user/cfg/ndrvtab" ]
					then
					    echo -n "<input type=\"button\" id=\"link11\" onKeyPress=\"javascript:window.location='mount-edit.cgi?mount=1&id=$id';\" onClick=\"javascript:window.location='mount-edit.cgi?mount=1&id=$id';\" value=\"Mount\" style=\"width:100px\" />"
					else
					    echo -n "<input type=\"button\" id=\"link11\" onKeyPress=\"javascript:window.location='mount-edit.cgi?mount=1&id=$id';\" onClick=\"javascript:window.location='mount-edit.cgi?mount=1&id=$id';\" value=\"Mount button: You need to save first to be able to mount\" style=\"width:600px\" disabled />"
					fi
				    else
					echo -n "<input type=\"button\" id=\"link11\" onKeyPress=\"javascript:window.location='mount-edit.cgi?umount=1&id=$id';\" onClick=\"javascript:window.location='mount-edit.cgi?umount=1&id=$id';\" value=\"Unmount\" style=\"width:400px\" />"
				    fi
				?>
			    </div>
			</center>
			<div id="txtURLParent" style="background-color:white;height:40px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 7px; height:23;">
					URL: 
				</div>
				<div style="position: relative; left: 100px; top: -22px;">
				    <input id="txtURL" name="qURL" type="textarea" style="width:400px" onFocus='javascript:PageElements[currElementIndex].focused=true;' onBlur='javascript:PageElements[currElementIndex].focused=false;' value="<? echo $src ?>"/>
				</div>
			</div>
			<div id="txtUserParent" style="background-color:white;height:40px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 7px; height:23;">
					Username: 
				</div>
				<div style="position: relative; left: 100px; top: -22px;">
					<input id="txtUser" name="qUser" type="textarea" style="width:400px" onFocus='javascript:PageElements[currElementIndex].focused=true;' onBlur='javascript:PageElements[currElementIndex].focused=false;' value="<? echo $uname ?>"/>
				</div>
			</div>
			<div id="txtPasswParent" style="background-color:white;height:40px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 7px; height:23;">
					Password: 
				</div>
				<div style="position: relative; left: 100px; top: -22px;">
					<input id="txtPassw" name="qPassw" type="textarea" style="width:400px" onFocus='javascript:PageElements[currElementIndex].focused=true;' onBlur='javascript:PageElements[currElementIndex].focused=false;' value="<? echo $pass ?>"/>
				</div>
			</div>
			<div id="txtPathParent" style="background-color:white;height:40px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 7px; height:23;">
					Mount path: 
				</div>
				<div style="position: relative; left: 100px; top: -22px;">
					<input id="txtPath" name="qPath" type="textarea" style="width:400px" onFocus='javascript:PageElements[currElementIndex].focused=true;' onBlur='javascript:PageElements[currElementIndex].focused=false;' value="<? echo $dst ?>"/>
				</div>
			</div>
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
			<div id="check1Parent" style="background-color:white;height:40px; font-size:16px;">
				<div style="position: relative; left: 5px; top: 5px;">
				<? if [ "$automount" = "1" ]
				   then
					echo '<input type="checkbox" name="check1" value="automount" checked> AutoMount'
				   else
					echo '<input type="checkbox" name="check1" value="automount"> AutoMount'
				   fi ?>
				</div>
			</div>
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
			<input type="hidden" name="save" value="1">
			<? echo "<input type='hidden' name='id' value='$id'>" ?>
			<div id="textOnly" style="background-color:white;height:64px;">
				<div style="position: relative; left: 5px; top: 5px;">
				    <?
					if [ "$FORM_save" = "1" ]
					then
					    echo "OpenLGTV_BCM-INFO: WebUI: NetShare mounts file: /mnt/user/cfg/ndrvtab changed by WebUI..." >> /var/log/OpenLGTV_BCM.log
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

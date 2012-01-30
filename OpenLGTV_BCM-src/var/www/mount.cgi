#!/usr/bin/haserl
# mount.cgi by xeros, nicola_12345
# Source code released under GPL License
content-type: text/html

<html>
<? include/keycontrol.cgi.inc ?>

	<div style="position: absolute; left: 10px; top: 10px; width:880px; font-size:16px;">
		<form id="URL" name="URL" action="mount.cgi" method="GET">
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
			    [ "$FORM_type" = "etherwake" ] && echo "<!-- "
			?>
			<div id="textOnly" style="background-color:white;height:50px;">
				<div style="position: relative; left: 5px; top: 0px;">
					<center><b>Note: mount paths without '/' at the beginning are relative to USB device mount path<br />
					and need the USB storage device connected. That is not needed for absolute paths.</b></center><br />
				</div>
			</div>

<?
			    [ "$FORM_type" = "etherwake" ] && echo "-->"

# 0|1#cifs|nfs#[url]#NetShare(mount path on USB stick)#[options]#[username]#[password] - up to 0.5.0-beta1
# 0|1#cifs|nfs#[url]#NetShare(mount path on USB stick)#[options]#[username]#[password]#[0|1] - changed by 0.5.0-beta2 (added field for dir listing cache)
# 0|1#cifs|nfs#[url]#NetShare(mount path on USB stick)#[options]#[username]#[password]#[0|1]#[pings]# - changed by 0.5.0-beta4 (added field with number of pings to try)

echo "<div id='info' style='background-color:white;height:30px;'>"
if [ "$FORM_type" = "etherwake" ]
then
    echo "<table width='100%' border='1' style='background-color:pink;font-weight:bold;'><tr><td class='ew_name'>Name</td><td class='ew_ip'>IP address</td><td class='ew_mac'>MAC address</td><td class='ew_autowake'>AutoWake</td><td class='ew_edit'>Edit</td></tr></table>"
else
    echo "<table width='100%' border='1' style='background-color:pink;font-weight:bold;'><tr><td class='mountsrc'>Source</td><td class='mountdst'>Mount path</td><td class='mountfstype'>Type</td><td class='mountuname'>Username</td><td class='mountauto'>AutoMnt</td><td class='mountedit'>Edit</td></tr></table>"
fi
echo "</div>"

share_id=1
link_id=11
num_lines="`cat ${input_file} 2>/dev/null | wc -l`"

if [ "${num_lines}" != "0" ]
then
    if [ "$FORM_id" != "" -a "$FORM_action" = "remove" ]
    then
	id="$FORM_id"
	if [ "$num_lines" -ge "$id" ]
	then
	    sed -i -e "$id d" ${input_file}
	    num_lines="`cat ${input_file} | wc -l`"
	fi
    fi

    cat ${input_file} | while read ndrv
    do
	ndrv_2="${ndrv#*\#}"
	ndrv_3="${ndrv_2#*\#}"
	ndrv_4="${ndrv_3#*\#}"
	ndrv_5="${ndrv_4#*\#}"
	ndrv_6="${ndrv_5#*\#}"
	echo "<div id='link${link_id}Parent' style='background-color:white;height:40px;'>"
	if [ "$FORM_type" = "etherwake" ]
	then
	    ew_autowake="${ndrv%%#*}"
	    ew_name="${ndrv_2%%#*}"
	    ew_ip="${ndrv_3%%#*}"
	    ew_mac="${ndrv_4%%#*}"
	    ew_pass="${ndrv_5%%#*}"
	    ew_opt="${ndrv_6%%#*}"
	    echo "<table width='100%' border='1'><tr><td class='ew_name'>$ew_name</td><td class='ew_ip'>$ew_ip</td><td class='ew_mac'>$ew_mac</td><td class='ew_autowake'>$ew_autowake</td>"
	    echo -n "<td class='ew_edit'><input type=\"button\" name=\"\" id=\"link${link_id}\" onKeyPress=\"javascript:window.location='mount-edit.cgi?type=etherwake&id=${share_id}';\" onClick=\"javascript:window.location='mount-edit.cgi?type=etherwake&id=${share_id}';\" value=\"Edit\"/></td>"
	else
	    automount="${ndrv%%#*}"
	    fs_type="${ndrv_2%%#*}"
	    src="${ndrv_3%%#*}"
	    dst="${ndrv_4%%#*}"
	    uname="${ndrv_6%%#*}"
	    #mntstat=`mount | grep "$src.*$dst"`
	    echo "<table width='100%' border='1'><tr><td class='mountsrc'>$src</td><td class='mountdst'>$dst</td><td class='mountfstype'>$fs_type</td><td class='mountuname'>$uname</td><td class='mountauto'>$automount</td>"
	    echo -n "<td class='mountedit'><input type=\"button\" name=\"\" id=\"link${link_id}\" onKeyPress=\"javascript:window.location='mount-edit.cgi?id=${share_id}';\" onClick=\"javascript:window.location='mount-edit.cgi?id=${share_id}';\" value=\"Edit\"/></td>"
	fi
	echo "</tr></table>"
	echo '</div>'
	share_id="$((${share_id}+1))"
	link_id="$((${link_id}+1))"
    done
else
    noSetupMsg="No Network Shares Defined Yet"
    [ "$FORM_type" = "etherwake" ] && noSetupMsg="No Devices To Wake Up Defined Yet"
    echo "<div id='link${link_id}Parent' style='background-color:white;height:40px;text-align:center;font-size:26px;'>$noSetupMsg</div>"
fi
if [ "$FORM_type" = "etherwake" ]
then
    yellowtxt="Add Device"
    bluetxt="Del Device"
    echo "<input type='hidden' name='type' value='etherwake'>"
else
    yellowtxt="Add Share"
    bluetxt="Del Share"
fi
echo "<script type='text/javascript'>"
echo "var share_id = $((${num_lines}+1));"
echo "var type = '${FORM_type}';"
?>

var yellowbtn = document.getElementById('YellowBtn');
var bluebtn = document.getElementById('BlueBtn')
<? 
    echo "yellowbtn.innerHTML = '<li class=\"yellow\"><span><img src=\"Images/Keyboard/yellow_button.png\" border=\"0\" /></span>$yellowtxt</li>';"
    echo "bluebtn.innerHTML = '<li class=\"blue\"><span><img src=\"Images/Keyboard/blue_button.png\" border=\"0\" /></span>$bluetxt</li>';"
?>
var currentId;

// ugly workaround: the real BackSpace() function code has been changed to match '/mount.cgi' only

<?
echo "yellowbtn.href = 'mount-edit.cgi?type=' + type + '&id=' + share_id;"
echo "function SaveForm() { window.location='mount-edit.cgi?type=' + type + '&id=' + share_id; }"
?>

</script>
		</form>
	</div>	
</body>
</html>

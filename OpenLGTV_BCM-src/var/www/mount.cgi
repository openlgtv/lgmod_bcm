#!/bin/haserl
# mount.cgi by xeros, nicola_12345
# Source code released under GPL License
content-type: text/html

<html>
<? include/keycontrol.cgi.inc ?>

	<div style="position: absolute; left: 10px; top: 10px; width:860px; font-size:16px;">
		<form id="URL" name="URL" action="mount.cgi" method="GET">
			<? 
			    export pagename="Network Share Mounts"
			    include/header_links.cgi.inc
			?>
			<div id="textOnly" style="background-color:white;height:50px;">
				<div style="position: relative; left: 5px; top: 0px;">
					<center><b>Note: mount paths without '/' at the beginning are relative to USB device mount path<br />
					and need the USB storage device connected. That is not needed for absolute paths.</b></center><br />
				</div>
			</div>

<?
# 0|1#cifs|nfs#[url]#NetShare(mount path on USB stick)#[options]#[username]#[password] - up to 0.5.0-beta1
# 0|1#cifs|nfs#[url]#NetShare(mount path on USB stick)#[options]#[username]#[password]#[0|1] - changed by 0.5.0-beta2 (added field for dir listing cache)

echo "<div id='info' style='background-color:white;height:30px;'>"
echo "<table width='100%' border='1' style='background-color:pink;font-weight:bold;'><tr><td class='mountsrc'>Source</td><td class='mountdst'>Mount path</td><td class='mountfstype'>Type</td><td class='mountuname'>Username</td><td class='mountauto'>AutoMnt</td><td class='mountedit'>Edit</td></tr></table>"
echo "</div>"

share_id=1
link_id=11

if [ -f "/mnt/user/cfg/ndrvtab" ]
then
    num_lines="`cat /mnt/user/cfg/ndrvtab | wc -l`"
    if [ "$FORM_id" != "" -a "$FORM_action" = "remove" ]
    then
	id="$FORM_id"
	if [ "$num_lines" -ge "$id" ]
	then
	    sed -i -e "$id d" /mnt/user/cfg/ndrvtab
	    num_lines="`cat /mnt/user/cfg/ndrvtab | wc -l`"
	fi
    fi

    cat /mnt/user/cfg/ndrvtab | while read ndrv
    do
	automount="${ndrv%%#*}"
	ndrv_2="${ndrv#*\#}"
	fs_type="${ndrv_2%%#*}"
	ndrv_3="${ndrv_2#*\#}"
	src="${ndrv_3%%#*}"
	ndrv_4="${ndrv_3#*\#}"
	dst="${ndrv_4%%#*}"
	ndrv_5="${ndrv_4#*\#}"
	ndrv_6="${ndrv_5#*\#}"
	uname="${ndrv_6%%#*}"
	#mntstat=`mount | grep "$src.*$dst"`
	echo "<div id='link${link_id}Parent' style='background-color:white;height:40px;'>"
	echo "<table width='100%' border='1'><tr><td class='mountsrc'>$src</td><td class='mountdst'>$dst</td><td class='mountfstype'>$fs_type</td><td class='mountuname'>$uname</td><td class='mountauto'>$automount</td>"
	echo -n "<td class='mountedit'><input type=\"button\" name=\"\" id=\"link${link_id}\" onKeyPress=\"javascript:window.location='mount-edit.cgi?id=${share_id}';\" onClick=\"javascript:window.location='mount-edit.cgi?id=${share_id}';\" value=\"Edit\"/></td>"
	echo "</tr></table>"
	echo '</div>'
	share_id="$((${share_id}+1))"
	link_id="$((${link_id}+1))"
    done
fi

echo "<script type='text/javascript'>"
echo "var share_id = $((${num_lines}+1));"

?>


var yellowbtn = document.getElementById('YellowBtn');
var bluebtn = document.getElementById('BlueBtn')
yellowbtn.innerHTML = '<li class="yellow"><span><img src="Images/Keyboard/yellow_button.png" border=\"0\" /></span>Add Share</li>';
bluebtn.innerHTML = '<li class="blue"><span><img src="Images/Keyboard/blue_button.png" border=\"0\" /></span>Del Share</li>';
var currentId;

// ugly workaround: the real BackSpace() function code has been changed to match '/mount.cgi' only

<?

echo "yellowbtn.href = 'mount-edit.cgi?id=' + share_id;"
echo "function SaveForm() { window.location='mount-edit.cgi?id=' + share_id; }"

?>

</script>

		</form>
	</div>	
</body>
</html>

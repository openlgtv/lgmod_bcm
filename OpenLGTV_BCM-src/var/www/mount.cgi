#!/bin/haserl
content-type: text/html

<html>
<? cat /var/www/include/keycontrol.html.inc ?>

	<div style="position: absolute; left: 10px; top: 10px; width:600px">
		<form id="URL" name="URL" action="mount.cgi" method="GET">
			<? export pagename="Network Share Mounts" ?>
			<? include/header_links.cgi.inc ?>
			<div id="textOnly" style="background-color:white;height:50px;">
				<div style="position: relative; left: 5px; top: 0px;">
					<br />
					Note: Needs to have USB stick and CIFS needs additional driver<br />
				</div>
			</div>

<?
# 0|1#cifs|nfs#[url]#NetShare(mount path on USB stick)#[options]#[username]#[password]
# for now only one mount point is supported, could be extended in future

#echo '<div style="position: absolute; left: 650px; top: 10px; width:300px; background-color:white;height:50px;">'
#echo ndrv: $FORM_qURL $FORM_qPassw $FORM_qUser $FORM_radio1 $FORM_check1 $opt $uname $pass
#echo '</div>'

if [ "$FORM_qURL" != "" -a "$FORM_radio1" != "" ]
then
    if [ "$FORM_check1" = "automount" ]
    then
	automount=1
    else
	automount=0
    fi
    
    #echo '<div style="position: absolute; left: 650px; top: 10px; width:400px; background-color:white;height:150px;">'
    #echo form: $FORM_qURL $FORM_qPassw $FORM_qUser $FORM_radio1 $FORM_check1
    #echo "save: $automount#$FORM_radio1#$FORM_qURL#NetShare##$FORM_qUser#$FORM_qPassw"
    cp /mnt/user/cfg/ndrvtab /mnt/user/cfg/ndrvtab.bck
    echo "$automount#$FORM_radio1#$FORM_qURL#NetShare##$FORM_qUser#$FORM_qPassw" > /mnt/user/cfg/ndrvtab
    #echo '</div>'
fi

if [ -f "/mnt/user/cfg/ndrvtab" ]
then
    #cat /mnt/user/cfg/ndrvtab | while read ndrv < /mnt/user/cfg/ndrvtab
    #while read ndrv < /mnt/user/cfg/ndrvtab
    #cat /mnt/user/cfg/ndrvtab | read ndrv
    ndrv=`cat /mnt/user/cfg/ndrvtab`
    #do
	automount=`echo $ndrv | awk -F# '{print $1}'`
	fs_type=`echo $ndrv | awk -F# '{print $2}'`
	src=`echo $ndrv | awk -F# '{print $3}'`
	dst=`echo $ndrv | awk -F# '{print $4}'`
	opt=`echo $ndrv | awk -F# '{print $5}'`
	uname=`echo $ndrv | awk -F# '{print $6}'`
	pass=`echo $ndrv | awk -F# '{print $7}'`
	#mntstat=`mount | grep "$src.*$dst"`
    ##echo '<div style="position: absolute; left: 650px; top: 10px; width:300px; background-color:white;height:50px;">'
    ##echo ndrv: $automount $fs_type $src $dst $opt $uname $pass
    ##echo '</div>'
    #done
fi

?>

			<div id="txtURLParent" style="background-color:white;height:30px;">
				<div style="position: relative; left: 5px; top: 7px; height:23;">
					URL: 
				</div>
				<div style="position: relative; left: 100px; top: -22px;">
				    <input id="txtURL" name="qURL" type="textarea" style="width:400px" value="<? echo $src ?>"/>
				</div>
			</div>
			<div id="txtUserParent" style="background-color:white;height:30px;">
				<div style="position: relative; left: 5px; top: 7px; height:23;">
					Username: 
				</div>
				<div style="position: relative; left: 100px; top: -22px;">
					<input id="txtUser" name="qUser" type="textarea" style="width:400px" value="<? echo $uname ?>"/>
				</div>
			</div>
			<div id="txtPasswParent" style="background-color:white;height:30px;">
				<div style="position: relative; left: 5px; top: 7px; height:23;">
					Password: 
				</div>
				<div style="position: relative; left: 100px; top: -22px;">
					<input id="txtPassw" name="qPassw" type="textarea" style="width:400px" value="<? echo $pass ?>"/>
				</div>
			</div>
			<div id="radio1Parent" style="background-color:white;height:30px;">
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
			<div id="check1Parent" style="background-color:white;height:30px;">
				<div style="position: relative; left: 5px; top: 5px;">
				<? if [ "$automount" = "1" ]
				   then
					echo '<input type="checkbox" name="check1" value="automount" checked> AutoMount'
				   else
					echo '<input type="checkbox" name="check1" value="automount"> AutoMount'
				   fi ?>
				</div>
			</div>
		</form>
	</div>	


</body>
</html>

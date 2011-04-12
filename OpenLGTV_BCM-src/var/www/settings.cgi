#!/usr/bin/haserl
content-type: text/html

<html>
<? cat /var/www/include/keycontrol.html.inc ?>

<font color="white">
<!-- ? for i in `cat /mnt/user/cfg/settings`; do echo "$i<br/>"; done ? -->
</font>

	<div style="position: absolute; left: 10px; top: 15px; width:550px">
		<div id="textOnly" style="background-color:white;height:64px;">
			<div style="position: relative; left: 5px; top: 5px;">
				<font size="+3"><b>OpenLGTV BCM settings list</b></font>
			</div>
		</div>
		<form id="URL" name="URL">
			<div id="txtURLParent" style="background-color:white;height:32px;">
				<div style="position: relative; left: 5px; top: 5px;">
					URL: <input id="txtURL" type="textarea" style="width:200px" value=""/>
				</div>
			</div>
			<div id="txtUserParent" style="background-color:white;height:32px;">
				<div style="position: relative; left: 5px; top: 5px;">
					Username: <input id="txtUser" type="textarea" style="width:200px" value=""/>
				</div>
			</div>
			<div id="txtPasswParent" style="background-color:white;height:32px;">
				<div style="position: relative; left: 5px; top: 5px;">
					Password: <input id="txtPassw" type="textarea" style="width:200px" value=""/>
				</div>
			</div>
			<div id="radio1Parent" style="background-color:white;height:32px;">
				<div style="position: relative; left: 5px; top: 5px;">
					Radio buttons 
					<input type="radio" name="radio1" value="Option1"> Option1
					<input type="radio" name="radio1" value="Option2" checked> Option2
					<input type="radio" name="radio1" value="Option3"> Option3
				</div>
			</div>

			<? 
			id_nr=1
			for i in `cat /mnt/user/cfg/settings`
			do
			    opt_name=`echo $i | awk -F= '{print $1}'`
			    opt_val=`echo $i | awk -F= '{print $2}'`
			    opt_checked=`if [ \"$opt_val\" = \"1\" ]; then echo checked; fi`
			    echo "<div id=\"check"$id_nr"Parent\" style=\"background-color:white;height:32px;\">"
			    echo '<div style="position: relative; left: 5px; top: 5px;">'
			    #echo "<input type=\"checkbox\" name=\"$opt_name\" value=\"$opt_val\" \"$opt_checked\"> $opt_name"
			    echo "<input type=\"checkbox\" name=\"check$id_nr\" value=\"$opt_val\" \"$opt_checked\"> $opt_name"
			    echo '</div></div>'
			    id_nr=$((id_nr+1))
			done 
			?>
			<div id="textOnly" style="background-color:white;height:64px;">
				<div style="position: relative; left: 5px; top: 5px;">
				    <font size="+3">Save is not done yet!</font>
				</div>
			</div>
		</form>
	</div>	


</body>
</html>

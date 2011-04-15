#!/bin/haserl
content-type: text/html

<html>
<? cat /var/www/include/keycontrol.html.inc ?>

	<div style="position: absolute; left: 10px; top: 15px; width:600px">
		<form id="URL" name="URL">
			<? export pagename="Sample Key Control" ?>
			<? include/header_links.cgi.inc ?>
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
			<div id="check1Parent" style="background-color:white;height:32px;">
				<div style="position: relative; left: 5px; top: 5px;">
					<input type="checkbox" name="check1" value="Option3" checked> Check1
				</div>
			</div>
			<div id="check2Parent" style="background-color:white;height:32px;">
				<div style="position: relative; left: 5px; top: 5px;">
					<input type="checkbox" name="check2" value="Option3"> Check2
				</div>
			</div>
			<div id="check3Parent" style="background-color:white;height:32px;">
				<div style="position: relative; left: 5px; top: 5px;">
					<input type="checkbox" name="check3" value="Option3"> Check3
				</div>
			</div>
		</form>
	</div>	


</body>
</html>

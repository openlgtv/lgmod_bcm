#!/bin/haserl
content-type: text/html

<html>
<? cat /var/www/include/keycontrol.html.inc ?>

	<div style="position: absolute; left: 10px; top: 15px; width:600px">
		<form id="URL" name="URL">
			<? export pagename="Home Page" ?>
			<? include/header_links.cgi.inc ?>

			<div id="textOnly" style="background-color:white;height:300px;">
				<div style="position: relative; left: 5px; top: 5px;">
					<br />
					LG rootfs version: <? cat /proc/ver ?><br />
					LG Web Browser version: <? cat /mnt/browser/run3556 | grep Revision: | awk -F: '{print $2}' | sed 's/\"//g' ?><br />
					Web Browser User Agent string: <br />
					<font size="-1"><? echo "$HTTP_USER_AGENT" ?></font>
				</div>
			</div>

		</form>
	</div>	


</body>
</html>

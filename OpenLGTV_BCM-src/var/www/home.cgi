#!/bin/haserl
# home.cgi by xeros
# Source code released under GPL License
content-type: text/html

<html>
<? cat /var/www/include/keycontrol.html.inc ?>

	<div style="position: absolute; left: 10px; top: 10px; width:860px; font-size:16px;">
		<form id="URL" name="URL">
			<? export pagename="Home Page" ?>
			<? include/header_links.cgi.inc ?>
			<div id="textOnly" style="background-color:white;height:300px;">
				<div style="position: relative; left: 5px; top: 5px;">
					<br />
					<b>LG rootfs version:</b> <? cat /etc/ver | awk -F, '{print $1}' ?><br /><br />
					<b>LG Web Browser version:</b> <? cat /mnt/browser/run3556 | grep Revision: | awk -F: '{print $2}' | sed 's/\"//g' ?><br /><br />
					<b>Web Browser User Agent string:</b> <br />
					<font size="-1"><? echo "$HTTP_USER_AGENT" ?></font>
				</div>
			</div>

		</form>
	</div>	


</body>
</html>

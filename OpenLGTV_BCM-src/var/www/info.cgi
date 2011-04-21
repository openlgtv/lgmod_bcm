#!/bin/haserl
# info.cgi by xeros
# Source code released under GPL License
content-type: text/html

<html>
<? cat /var/www/include/keycontrol.html.inc ?>

	<div style="position: absolute; left: 10px; top: 10px; width:860px">
		<form id="URL" name="URL">
			<? export pagename="Info Page" ?>
			<? include/header_links.cgi.inc ?>
			
			<div id="textOnly" style="background-color:white;height:390px;">
				<div style="position: relative; left: 5px; top: 5px;">
					<!-- /proc/cpuinfo:<br />
					<pre><? cat /proc/cpuinfo ?></pre> -->
					Last 25 running processes:<br />
					<font size="-3"><pre><? ps w | tail -n 25 ?></pre></font>
				</div>
			</div>
		</form>
	</div>	


</body>
</html>

#!/bin/haserl
content-type: text/html

<html>
<? cat /var/www/include/keycontrol.html.inc ?>

	<div style="position: absolute; left: 10px; top: 15px; width:600px">
		<form id="URL" name="URL">
			<? export pagename="Info Page" ?>
			<? include/header_links.cgi.inc ?>
			
			<div id="textOnly" style="background-color:white;height:400px;">
				<div style="position: relative; left: 5px; top: 5px;">
					<!-- /proc/cpuinfo:<br />
					<pre><? cat /proc/cpuinfo ?></pre> -->
					Running processes:<br />
					<font size="-3"><pre><? ps w ?></pre></font>
				</div>
			</div>
		</form>
	</div>	


</body>
</html>

#!/usr/bin/haserl
# info.cgi by xeros
# Source code released under GPL License
content-type: text/html

<html>
<? include/keycontrol.cgi.inc ?>

	<div style="position: absolute; left: 10px; top: 10px; width:880px; font-size:16px;">
		<form id="URL" name="URL">
			<? 
			    export pagename="Info Page"
			    include/header_links.cgi.inc
			?>
			
			<div id="textOnly" style="background-color:white; height:480px;">
				<div style="position: relative; left: 5px; top: 5px;">
					Last 30 running processes:<br />
					<font size="-3"><pre><? ps w | tail -n 30 ?></pre></font>
				</div>
			</div>
		</form>
	</div>	


</body>
</html>

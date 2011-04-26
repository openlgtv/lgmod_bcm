#!/bin/haserl
# header_links.cgi.inc by xeros
# Source code released under GPL License

			<div id="textOnly" style="background-color:white;height:130px; background-color:yellow">
				<div style="position: relative; left: 5px; top: -2px;">
					<center><font size="+3"><b>OpenLGTV BCM <? cat /etc/ver2 ?><br/></font><font size="+2">Web UI<br/></font><font color="blue" size="+3"><? echo $pagename ?></font></b></font></center>
				</div>
			</div>
			<center>
			<div id="link1Parent" style="background-color:white;height:30px;display:inline-block;width:150px">
				<input type="button" id="link1" onKeyPress="javascript:window.location='home.cgi';" onClick="javascript:window.location='home.cgi';" value="Home" style="width:100px" />
			</div><div id="link2Parent" style="background-color:white;height:30px;display:inline-block;width:150px">
				<input type="button" id="link2" onKeyPress="javascript:window.location='info.cgi';" onClick="javascript:window.location='info.cgi';" value="Info" style="width:100px" />
			</div><div id="link3Parent" style="background-color:white;height:30px;display:inline-block;width:160px">
				<input type="button" id="link3" onKeyPress="javascript:window.location='settings.cgi';" onClick="javascript:window.location='settings.cgi';" value="Settings" style="width:100px" />
			</div><div id="link4Parent" style="background-color:white;height:30px;display:inline-block;width:230px">
				<input type="button" id="link4" onKeyPress="javascript:window.location='mount.cgi';" onClick="javascript:window.location='mount.cgi';" value="Network Share Mounts" style="width:200px" width="100" />
			</div><div id="link5Parent" style="background-color:white;height:30px;display:inline-block;width:170px">
				<input type="button" id="link5" onKeyPress="javascript:window.location='browser.html';" onClick="javascript:window.location='browser.html';" value="Web Browser" style="width:150px" />
			</div>
			</center>

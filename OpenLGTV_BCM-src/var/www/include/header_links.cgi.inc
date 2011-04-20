#!/bin/haserl
			<div id="textOnly" style="background-color:white;height:120px;">
				<div style="position: relative; left: 5px; top: 0px;">
					<center><font size="+3"><b>OpenLGTV BCM <? cat /etc/ver2 ?><br/></font><font size="+2">Web UI<br/></font><font color="blue" size="+3"><? echo $pagename ?></font></b></font></center>
				</div>
			</div>
			<div id="link1Parent" style="background-color:white;height:25px;">
				<div style="position: relative; left: 5px; top: -2px;">
					<center><input type="button" id="link1" onKeyPress="javascript:window.location='home.cgi';" onClick="javascript:window.location='home.cgi';" value="Home" style="width:300px" /></center>
				</div>
			</div>
			<div id="link2Parent" style="background-color:white;height:25px;">
				<div style="position: relative; left: 5px; top: -2px;">
					<center><input type="button" id="link2" onKeyPress="javascript:window.location='info.cgi';" onClick="javascript:window.location='info.cgi';" value="Info" style="width:300px" /></center>
				</div>
			</div>
			<div id="link3Parent" style="background-color:white;height:25px;">
				<div style="position: relative; left: 5px; top: -2px;">
					<center><input type="button" id="link3" onKeyPress="javascript:window.location='settings.cgi';" onClick="javascript:window.location='settings.cgi';" value="Settings" style="width:300px" /></center>
				</div>
			</div>
			<div id="link4Parent" style="background-color:white;height:25px;">
				<div style="position: relative; left: 5px; top: -2px;">
					<center><input type="button" id="link4" onKeyPress="javascript:window.location='mount.cgi';" onClick="javascript:window.location='mount.cgi';" value="Network Share Mounts" style="width:300px" /></center>
				</div>
			</div>

			<!-- TODO - 'button' page elements presentation and navigation in one row
			<div id="linksParent" style="background-color:white;height:32px;">
				<div id="link1Parent" style="background-color:white;height:32px;">
				    <div style="position: relative; left: 5px; top: 5px;">
					<input id="links" type="hidden" href="settings.cgi" onKeyPress="javascript:setCurrent(this);return false" onClick="javascript:NextControl();" value="TEST" style="width:200px" />
					Links: 
					<input type="button" id="link1" href="settings.cgi" onKeyPress="javascript:window.location='settings.cgi';" onClick="javascript:window.location='settings.cgi';" value="Settings" style="width:100px" />
					<input type="button" id="link2" href="settings.cgi" onKeyPress="javascript:window.location='samplekeycontrol.cgi';" onClick="javascript:window.location='samplekeycontrol.cgi';" value="Settings2" style="width:100px" />
				    </div>
				</div>
			</div> -->

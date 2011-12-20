#!/bin/haserl
<!-- header_links.cgi.inc by xeros -->
<!-- Source code released under GPL License -->
			<div id="textOnly" style="background-color:white;height:130px; background-color:yellow">
				<center><font size="+3"><b>OpenLGTV BCM <? cat /etc/ver2 ?><br/></font><font size="+2">Web UI<br/></font><font color="blue" size="+3"><? echo $pagename ?></font></b></font></center>
			</div>
			<div style="position: absolute; right: 5px; top: 0px;"><b><font size="+3"><span id="clock">&nbsp;</span></b></font></div>
			<!-- div id="link1Parent" class="menuitem" style="background-color:white;height:32px;display:inline-block;width:110px" -->
			<div id="link1Parent" class="menuitem" style="width:100px">
				<!-- center><input type="button" id="link1" class="menubutton" onKeyPress="javascript:window.location='home.cgi';" onClick="javascript:window.location='home.cgi';" value="Home" style="width:100px" /></center -->
				<a id="link1" class="menubutton" href="home.cgi">Home</a>
			</div><div id="link2Parent" class="menuitem" style="width:100px">
				<a id="link2" class="menubutton" href="info.cgi">Info</a>
			</div><div id="link3Parent" class="menuitem" style="width:100px">
				<a id="link3" class="menubutton" href="settings.cgi">Settings</a>
			</div><div id="link4Parent" class="menuitem" style="width:126px">
				<a id="link4" class="menubutton" href="mount.cgi?type=etherwake">Ether Wake</a>
			</div><div id="link5Parent" class="menuitem" style="width:150px">
				<a id="link5" class="menubutton" href="mount.cgi">Network Shares</a>
			</div><div id="link6Parent" class="menuitem" style="width:170px">
				<a id="link6" class="menubutton" href="browser.cgi">Internet Browser</a>
			</div><div id="link7Parent" class="menuitem" style="width:120px">
				<a id="link7" class="menubutton" href="fm.cgi?side=l&lpth=/mnt/usb1&rpth=/mnt/usb2">FileManager</a>
			</div>

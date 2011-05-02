#!/bin/haserl
<head>
<!-- Sample Key Control NetCast Web UI by nicola_12345, changes by xeros -->
<!-- Source code released under GPL License -->

<title>OpenLGTV BCM</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<meta http-equiv="Content-Style-Type" content="text/css">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<!-- link rel="stylesheet" type="text/css" href="player/styles.css"/ -->
<link rel="stylesheet" type="text/css" href="css/styles.css"/>
<link rel="stylesheet" type="text/css" href="css/keyboard.css"/>

<SCRIPT language="JavaScript" type="text/javascript" src="js/control.js"></script>
</head>
<body>
<IMG align="right" SRC="Images/openlgtvbcm_logo.png" ALT="OpenLGTV BCM" style="position: relative; right: 110px; top: 30px;"/>
	<!-- div style="position: absolute; right: 10px; bottom: 300px;" --> <!-- old, wider keypad -->
	<div style="position: absolute; right: 60px; bottom: 300px;">        <!-- new, tapkey size adjusted keypad -->
		<? cat include/keypad_table.html.inc ?>
	</div>
	<div style="position: absolute; right: 60px; bottom: 100px;">
		<Table Border=0 cellspacing=0>
			<tr>
				<td><img src="Images/Keyboard/tapkey.png" align="middle"></td>
			</tr>
		</Table>
	</div>
	<div id="footer" class="footer">
		<ul>
			<!-- li class="blank"><span></span></li -->
			<a onClick="javascript:PrevControl();" href="#" style="text-decoration:none; color:white"><li class="red"><span><img src="Images/Keyboard/red_button.png" border="0" /></span>Prev Ctrl</li></a>
			<a onClick="javascript:NextControl();" href="#" style="text-decoration:none; color:white"><li class="green"><span><img src="Images/Keyboard/green_button.png" border="0" /></span>Next Ctrl</li></a>
			<a onClick="javascript:SaveForm();" href="#" style="text-decoration:none; color:white"><li class="yellow"><span><img src="Images/Keyboard/yellow_button.png" border="0" /></span>Save</li></a>
			<a onClick="javascript:BackSpace();" href="#" style="text-decoration:none; color:white"><li class="blue"><span><img src="Images/Keyboard/blue_button.png" border="0" /></span>BackSpace</li></a>
			<a onClick="javascript:history.go(-1);" href="#" style="text-decoration:none; color:white"><li id="return_bt" class="return"><span><img src="Images/Keyboard/back_button.png" border="0" /></span>Back</li></a>
			<a onClick="window.NetCastBack();" href="#" style="text-decoration:none; color:white"><li class="exit"><span><img src="Images/Keyboard/exit_button.png" border="0" /></span>Exit</li></a>
		</ul>
	</div>
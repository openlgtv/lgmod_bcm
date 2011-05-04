#!/bin/haserl
content-type: text/html

<HTML>
  <HEAD>
	<!-- Code for OpenLGTV BCM Browser by Nicola Ottomano -->
	<!-- Source code released under GPL License -->
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
	<meta http-equiv="Content-Style-Type" content="text/css">
	<meta http-equiv="Content-Script-Type" content="text/javascript">
	<style>
	body {
	    overflow: hidden;
	    overflow-y: hidden;
	    overflow-x: hidden;
	}
	</style>
    <TITLE>OpenLGTV BCM Browser</TITLE>
  </HEAD>
  <FRAMESET cols="263,*" frameborder=0 border="0" framespacing="0">
  <frame name="Keyboard" src="browser/keyboard.cgi" scrolling="no">
  <!-- frame name="MainPage" src="browser/mainpage.html" scrolling="no" -->
  <frame name="MainPage" src="browser/mainpage.html">
  </FRAMESET>
  <NOFRAMES>
    <BODY>
	Frameset unsupported
    </BODY>
  </NOFRAMES>
</HTML>
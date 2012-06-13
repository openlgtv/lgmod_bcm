#!/usr/bin/haserl
<content-type: text/html>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<!-- showmsg.cgi for OpenLGTV BCM by xeros -->
<!-- shows messages on TV screen using web browser -->
<!-- Source code released under GPL License -->
<!-- usage: /mnt/browser/run3556 "http://127.0.0.1/tools/showmsg.cgi?font1=6&font2=3&msg1=short big message&msg=smaller but longer message below&timeout=10" -->
<!-- NOT FINISHED YET -->
<HEAD>
<style type="text/css">
    body {
	font-family:"TiresiasScreenfont";
	background-color:black;
	color: yellow;
    }
</style>
<title>OpenLGTV BCM</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<?
    [ -n "$FORM_timeout" ] && timeout="$FORM_timeout" || timeout=10
    [ -n "$FORM_font1"   ] && font1="$FORM_font1"   || font1=6
    [ -n "$FORM_font2"   ] && font2="$FORM_font2"   || font2=3
    [ -n "$FORM_font3"   ] && font3="$FORM_font3"   || font3=3
    [ -n "$FORM_color1"  ] && color1="$FORM_color1" || color1=yellow
    [ -n "$FORM_color2"  ] && color2="$FORM_color2" || color2=white
    [ -n "$FORM_color3"  ] && color3="$FORM_color3" || color3=white
    [ "$HTTP_HOST" = "127.0.0.1:88" -a "$timeout" -gt 0 ] &&  echo "<META http-equiv='refresh' content='$timeout;url=../home.cgi?qURL=killall+lb4wk+GtkLauncher&run=Run'>"
?>
</HEAD>
<BODY BGCOLOR="BLACK">
<CENTER>
<FONT SIZE="+6">
<BR/>
<IMG SRC="../Images/openlgtvbcm_logo.png" ALT="OpenLGTV BCM"/>
</FONT><BR/>
<?
    echo "<FONT SIZE="+$font1" color="$color1">$FORM_msg1</FONT><BR/><BR/>"
    echo "<FONT SIZE="+$font2" color="$color2">$FORM_msg2</FONT><BR/><BR/>"
    echo "<FONT SIZE="+$font3" color="$color3">$FORM_msg3</FONT>"
?>
<BR/>
</CENTER>
</BODY>
</HTML>

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
<?
    [ -n "$FORM_timeout" ] && timeout="$FORM_timeout" || timeout=10
    [ -n "$FORM_font1" ] && font1="$FORM_font1" || font1=6
    [ -n "$FORM_font2" ] && font1="$FORM_font2" || font1=3
    echo "<META http-equiv='refresh' content='$timeout;url=../home.cgi?qURL=killall+lb4wk+GtkLauncher&run=Run'>"
?>
</HEAD>
<BODY>
<CENTER>
<FONT SIZE="+6">
<BR/>
<IMG SRC="../Images/openlgtvbcm_logo.png" ALT="OpenLGTV BCM"/>
<BR/>OpenLGTV BCM<BR/>
</FONT><BR/><FONT SIZE="+6">
<? echo "$FORM_msg1" ?><BR/>
</FONT>
<BR/>
<FONT SIZE="+3">
<? echo "$FORM_msg2" ?><BR/>
</FONT>
</CENTER>
</BODY>
</HTML>

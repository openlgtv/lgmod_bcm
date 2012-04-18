#!/usr/bin/haserl
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
</HEAD>
<BODY>

<!-- OpenLGTV BCM FileManager by xeros -->
<!-- Source code released under GPL License -->

<? 
    SIFS="$IFS"
    IFS=$'\n'
    for i in `env`; do echo "$i<br/>"; done | sort
    IFS="$IFS"
?>

</BODY>
</HTML>

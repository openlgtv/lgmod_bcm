#!/bin/haserl
content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>

<meta HTTP-EQUIV="REFRESH" content="5; url=mainpage.cgi">

<!-- Code for OpenLGTV BCM Browser by Nicola Ottomano -->
<!-- Source code released under GPL License -->

</head>
<body>

	bookmark saved: <? echo "${GET_bookmarkURL}" ?>
	<? 
		sed -i -e "${GET_bookmarkId}s|.*|${GET_bookmarkURL}|" /var/www/user/bookmarks.inc
	?>
	
</body>
</html>


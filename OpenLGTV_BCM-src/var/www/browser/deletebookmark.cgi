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
			<? 
				sed -i -e "${GET_bookmarkId}s/.*//" /var/www/user/bookmarks.inc
				echo "bookmark deleted"
			?>


</body>
<html>


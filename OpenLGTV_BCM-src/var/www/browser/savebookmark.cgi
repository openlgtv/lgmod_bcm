#!/usr/bin/haserl
content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>

<meta HTTP-EQUIV="REFRESH" content="5; url=mainpage.cgi">

<!-- Code for OpenLGTV BCM Browser by Nicola Ottomano -->
<!-- Source code released under GPL License -->

</head>
<body bgcolor="#0E6EC6">
	<table cellpadding="0" cellspacing="0" border="0" style="margin: auto; position: relative; top: 230px;">
		<tr>
			<td><img src="Images/roundedcorner1.png"></td>
			<td bgcolor="#FFFFFF"></td>
			<td><img src="Images/roundedcorner2.png"></td>
		</tr>
		<tr>
			<td bgcolor="#FFFFFF"></td>
			<td bgcolor="#FFFFFF" align="center">
				<img src="Images/bookmark.png"><br><br>
				<font size="6">Bookmark saved:<br>
				<? echo "${GET_bookmarkURL}"; sed -i -e "${GET_bookmarkId}s|.*|${GET_bookmarkURL}|" /var/www/user/bookmarks.inc ?>
				</font>
			</td>
			<td bgcolor="#FFFFFF"></td>
		</tr>
		<tr>
			<td><img src="Images/roundedcorner3.png"></td>
			<td bgcolor="#FFFFFF"></td>
			<td><img src="Images/roundedcorner4.png"></td>
		</tr>
	</table>
</body>
</html>


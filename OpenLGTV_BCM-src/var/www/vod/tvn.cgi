#!/usr/bin/haserl
content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
	 "http://www.w3.org/TR/html4/strict.dtd">

<html>
	<head>
		<title>tvn player</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<link rel="stylesheet" href="http://sonyps3.services.tvnplayer.pl/index.css?v=20120706104336-prod">
	</head>
	<body scroll="no" class="starting">
		<div id="logo"></div>
		<div id="loading" style="display:block"></div>
		<img id="start-logo" src="http://sonyps3.services.tvnplayer.pl/tvnplayer/start_logo.png">
		<div id="console" style="display:none"></div>
		<script type="text/javascript">
		<? wget -U "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322)" "http://sonyps3.services.tvnplayer.pl/main.js" -O- | \
			sed -e "s#path: 'tvnplayer/'#path: 'http://sonyps3.services.tvnplayer.pl/tvnplayer/'#" \
			    -e 's/this.data.adserver/this.data.adserverX/g'
		?>
		</script>
	</body>
</html>

/*jslint white: true, browser: true, undef: true, nomen: true, eqeqeq: true, plusplus: false, bitwise: true, regexp: true, strict: true, newcap: true, immed: true, maxerr: 14 */
/*global window: false, ActiveXObject: true */

/*
Darko Bunic
http://www.redips.net/
Sep, 2012.

minor modifications by xeros
*/

/* enable strict mode */
"use strict";

// create object container
var remote = {};

// define service URL
remote.url = 'remote.cgi';

if (!Number.toFixed) {
	Number.prototype.toFixed=function(n){
		return Math.round(this*Math.pow(10, n)) / Math.pow(10, n);
	}
}

// initialization
remote.init = function () {
	// create XMLHttp request object
	remote.request = remote.initXMLHttpClient();
	// define reference to title
	remote.title = document.getElementById('title');
	// scale page to fit width on vertical view on mobile devices
	if (screen.height > screen.width) {
		var wScale = window.innerWidth/240;
		var metas = document.getElementsByTagName('meta');
		var i;
		for (i=0; i<metas.length; i++) {
			if (metas[i].name == "viewport") {
				//metas[i].content = 'width='+window.innerWidth;
				//metas[i].content = 'width='+window.innerWidth+'; target-densitydpi=device-dpi; initial-scale='+wScale+'; maximum-scale='+wScale+'; minimum-scale=1.0;';
				//metas[i].content = 'width=device-width; target-densitydpi=device-dpi; initial-scale='+wScale+'; maximum-scale='+wScale+'; minimum-scale=1.0;';
				metas[i].content = 'initial-scale='+wScale+'; maximum-scale='+wScale+'; minimum-scale=1.0;';
			}
		}
		// scroll to center by default
		//window.scrollTo((document.body.offsetWidth-document.documentElement.offsetWidth)/2,0);
		window.scrollTo(document.documentElement.offsetWidth/4,0);
	};
	//alert(window.innerWidth+'x'+window.innerHeight);
	//alert(screen.width+'x'+screen.height);
	//alert(document.body.offsetWidth+'x'+document.documentElement.offsetWidth)
};


// XMLHttp request object
remote.initXMLHttpClient = function () {
	var XMLHTTP_IDS,
		xmlhttp,
		success = false,
		i;
	// Mozilla/Chrome/Safari (normal browsers)
	try {
		xmlhttp = new XMLHttpRequest(); 
	}
	// IE (?!)
	catch (e1) {
		XMLHTTP_IDS = [ 'MSXML2.XMLHTTP.5.0', 'MSXML2.XMLHTTP.4.0',
						'MSXML2.XMLHTTP.3.0', 'MSXML2.XMLHTTP', 'Microsoft.XMLHTTP' ];
		for (i = 0; i < XMLHTTP_IDS.length && !success; i++) {
			try {
				success = true;
				xmlhttp = new ActiveXObject(XMLHTTP_IDS[i]);
			}
			catch (e2) {}
		}
		if (!success) {
			throw new Error('Unable to create XMLHttpRequest!');
		}
	}
	return xmlhttp;
};


// method executed on every key press
remote.key = function (key) {
	var time = new Date().getTime(),	// generate time (to prevent AJAX caching)
		text;							// returned text
	// open asynchronus request
	remote.request.open('GET', remote.url + '?key=' + key + '&t=' + time, true);
	// the onreadystatechange event is triggered every time the readyState changes
	remote.request.onreadystatechange = function () {
		//  request finished and response is ready
		if (remote.request.readyState === 4) {
			if (remote.request.status === 200) {
				// set returned text (remove trailing spaces, newline ...)
				text = remote.request.responseText.replace(/[\s\r\n]+$/, '');
				// service should return OK
				if (text === 'OK') {
					// change title color 
					remote.color();
				}
				// if returned value is not 'OK' then display error message
				else {
					alert('Error: [' + text + ']');
				}
			}
			// if request status is not 200 then display error message (this is error like 404 ...)
			else {
				alert('Error: [' + remote.request.status + '] ' + remote.request.statusText);
			}
	    }
	};
	remote.request.send(null); // send request
};


// if service returns 'OK' then shortly change title color to light blue
remote.color = function (message) {
	// change title color
	remote.title.style.color = 'lightBlue';
	// return default title color
	setTimeout(function () {
		remote.title.style.color = 'white';
	}, 250);
};


// add onload event listener
if (window.addEventListener) {
	window.addEventListener('load', remote.init, false);
}
else if (window.attachEvent) {
	window.attachEvent('onload', remote.init);
}
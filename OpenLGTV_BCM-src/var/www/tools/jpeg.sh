#!/bin/sh
type="jpeg"
jpegtran=`which jpegtran`
[ -z "$jpegtran" ] && type="png"
echo "Content-type: image/$type"
echo ""
[ -n "$QUERY_STRING" -a -n "$jpegtran" ] && wget -q -O - "$QUERY_STRING" | "$jpegtran" || cat /home/netcast_icons/www/unknown.png

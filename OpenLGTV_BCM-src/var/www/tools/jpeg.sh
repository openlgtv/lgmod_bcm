#!/bin/sh
type="jpeg"
jpegtran=`which jpegtran`
[ -z "$jpegtran" ] && type="png"
echo "Content-type: image/$type"
echo ""
if [ -n "$QUERY_STRING" -a -n "$jpegtran" ]
then
    url="$QUERY_STRING"
    url="${url//_amp_/&}"
    url="${url//_qst_/?}"
    wget -q -O - "$url" | "$jpegtran"
else
    cat /home/netcast_icons/www/unknown.png
fi

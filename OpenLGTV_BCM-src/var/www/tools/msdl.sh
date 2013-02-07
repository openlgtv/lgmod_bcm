#!/bin/sh
cat <<EOF
Content-type: application/x-netcast-av

EOF
killall msdl-1.2.7-r2-orig 2>/dev/null
msdl=`which msdl-1.2.7-r2-orig`

if [ -n "$msdl" ]
then
    echo "$msdl -q -o - \"$QUERY_STRING\"" >> /tmp/msdl.log
    "$msdl" -q -o - "$QUERY_STRING"
else
    echo "wget -q -O - \"$QUERY_STRING\"" >> /tmp/msdl.log
    wget -q -O - "$QUERY_STRING"
fi

#!/bin/sh
cat <<EOF
Content-type: application/x-netcast-av

EOF
killall msdl-1.2.7-r2-orig 2>/dev/null
msdl=`which msdl-1.2.7-r2-orig`
[ -n "$msdl" ] && "$msdl" -q -o - "$QUERY_STRING" || wget -q -O - "$QUERY_STRING"

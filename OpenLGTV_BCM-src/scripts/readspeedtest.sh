#!/bin/sh
# Source code released under GPL License
# readspeedtest.sh script for Saturn6/Saturn7/BCM by mmm4m5m,xeros

f="$1"
if [ -f "$f" ]; then
	size=$(stat -c%s "$f")
	time cat "$f" 2>&1 >/dev/null | \
		awk -F'[^.0-9]+' '/^r/{s='"$size"';t=$2*60+$3;print s" / "t" = "s/t/1024/1024" MB/s"}'
else
	echo "OpenLGTV: Script for file read transfer check"
	echo "Usage: $0 /path/to/file"
	echo "For accurate results: run once per file, use file with min size 100MB"
fi

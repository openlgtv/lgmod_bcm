#!/bin/sh
f="$1"
if [ -f "$f" ]
then
	time cat "$f" 2>&1 >/dev/null | awk -F'[^.0-9]+' '/^r/{s='$(stat -c%s "$f")';t=$2*60+$3;print s" / "t" = "s/t/1024/1024" MB/s"}'
else
	echo "Script for file read transfer check by mmm4m5m"
	echo "Measurement will be accurate if run once per file and file size should be at least 100MB"
	echo "Usage: $0 /path/to/file"
fi

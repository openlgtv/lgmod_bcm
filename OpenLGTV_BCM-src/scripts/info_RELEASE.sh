#!/bin/sh
# get_RELEASE_info.sh script by xeros
# this script get some useful info from RELEASE binary
# Source code released under GPL License

# works on all TV platforms from Saturn 6 up to SmartTV worldwide models
# update: modified only for 2010 BCM models for speedup run time

if [ -z "$1" ]
then
    RELEASE=$1
else
    RELEASE=/lg/lgapp/RELEASE
fi

if [ ! -f "$RELEASE" ]
then
    echo "Usage: /path/to/get_RELEASE_info.sh /path/to/RELEASE" >&2
    exit 1
fi

if [ ! -f "${path_to_bbe}bbe" -a ! -f "`which bbe`" ]
then
    echo "bbe not found!" >&2
    exit 1
fi

# set first read only the part of RELEASE which should fit all (most?) BCM 2010 2D and 3D firmwares
read="dd bs=20000 skip=640 count=200 if=$RELEASE"

rel_info="`$read 2>/dev/null | strings | grep -m1 -B1 -A4 swfarm | grep -v '^0.\..*\..*' | \
    head -n 5 | sed \"s/^'//g\"`"
# lets compare if the data got is right - not less than 7 words, not more than 100 characters
if [ "`echo $rel_info | wc -w`" -lt "7" -o "`echo $rel_info | wc -w`" -gt "100" ]
then
    rel_info="`strings $RELEASE | grep -m1 -B1 -A4 swfarm | grep -v '^0.\..*\..*' | head -n 5 | sed \"s/^'//g\"`"
    read="cat $RELEASE"
fi
rel_rev="`echo $rel_info | cut -d\" \" -f7`"
rel_rev_hex=$(for i in `echo -n $rel_rev | hexdump -v -e '/1 "%02X "'`; do echo -n "x$i"; done)
rel_ver=$($read 2>/dev/null | bbe -s -b /\\x00$rel_rev\\x00\\x00/:30 -e "p H" | sed -e 's/ //g' -e "s/x00${rel_rev_hex}\(x00\)*//gI" | awk -Fx '{print $5 $4 $3 $2}' | sed -e 's/\(..\)/\1./g' -e 's/.$//g' -e 's/^\(00\.\)*//g')
echo "LG firmware version information:"
echo $rel_info | awk '{print "Platform:         " $1 "\nBuilder:          " $2 "\nBuild date/time:  " $3 " " $4 " " $5 " " $6 "\nRevision:         " $7}'
echo "Version:          $rel_ver"

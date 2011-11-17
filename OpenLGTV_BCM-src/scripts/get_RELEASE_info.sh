#!/bin/sh
# get_RELEASE_info.sh script by xeros
# this script get some useful info from RELEASE binary
# Source code released under GPL License

# works on all TV platforms from Saturn 6 up to SmartTV worldwide models
# update: modified only for 2010 BCM models for speedup run time

# example outputs:
# $ /var/www/tv/scripts/get_RELEASE_info.sh /var/www/tv/03.20.19/RELEASE 
# DVB-BB-BCM3556         # platform
# bell.kim@swfarm-l4     # builder
# Jan 17 2011 16:20:13   # build date and time
# 50662                  # revision
# 03.20.19.01            # version - getting this needed most of the code below as it's hex and in dynamic content around

# $ /var/www/tv/scripts/get_RELEASE_info.sh /tmp/3.19_s6/RELEASE 
# DVB-SATURN6
# hyunduk.cho@swfarm-l1
# Jul 8 2010 14:28:17
# 1.0.09.34
# 03.19

# $ /var/www/tv/scripts/get_RELEASE_info.sh /var/www/tv/Saturn7_US_dump/unpacked/RELEASE 
# ATSC-SATURN7
# chanhun.kum@swfarm-l15
# Apr 29 2010 22:22:04
# 30060
# 03.04.24.01

# updated output with info from NVRAM (if valid):
# get_RELEASE_info.sh; nvram-edit | egrep "Model name|Platform|Debug status|Baudrate"
# LG firmware version information:
# Platform:         DVB-BB-BCM3556
# Builder:          bell.kim@swfarm-l4
# Build date/time:  Jan 17 2011 16:20:13
# Revision:         50662
# Version:          03.20.19.01
# Model name:       47LE7500-ZC
# Platform:         Broadcom BCM3549/3556
# Debug status:     RELEASE (5)
# Baudrate:         9600 bps (3)

# output rows are the same as in example for all mentioned platforms and this script can be used for parsing in other scripts

if [ "$1" != "" ]
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

# unversal code - takes much time
#rel_info="`strings $RELEASE | grep -m1 -B1 -A4 swfarm | grep -v '^0.\..*\..*' | head -n 5 | sed \"s/^'//g\"`"
#echo $rel_info | awk '{print $1 "\n" $2 "\n" $3 " " $4 " " $5 " " $6 "\n" $7}'; rel_rev="`echo $rel_info | awk '{print $7}'`"
#rel_rev_hex=$(for i in `echo -n $rel_rev | hexdump -v -e '/1 "%02X "'`; do echo -n "x$i"; done)
#cat $RELEASE | bbe -s -b /\\x00$rel_rev\\x00\\x00/:30 -e "p H" | sed -e 's/ //g' -e "s/x00${rel_rev_hex}\(x00\)*//gI" | \
#    awk -Fx '{print $5 $4 $3 $2}' | sed -e 's/\(..\)/\1./g' -e 's/.$//g' -e 's/^\(00\.\)*//g'

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

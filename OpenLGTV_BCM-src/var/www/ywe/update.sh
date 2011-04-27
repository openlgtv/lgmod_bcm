#!/bin/sh
# update.sh by xeros, tbage, QueZt
# Source code released under GPL License

echo "Content-type: text/html"
echo ""

# needed tools, on PC native, on TV needs busybox
busybox=""              # for native tools
#busybox="/tmp/busybox "  # for busybox tools in tv
#busybox="/bin/busybox "  # for busybox tools in tv
awk="$busybox"awk
md5sum="$busybox"md5sum
httpd="$busybox"httpd
wget="$busybox"wget
#tr="$busybox"tr
grep="$busybox"grep

#g_yaction=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])yaction=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "=" | sed 's/format//g'`
g_yaction=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])yaction=[^&]+" | cut -f 2 -d "=" | sed 's/format//g'`

useragent="Mozilla/5.0 (Samsung; U; Linux; en) Konfabulator/5.5.5"

widgetsPhpLoc="http://127.0.0.1:88/ywe/widgets.sh"
url="http://gallery.tv.widgets.yahoo.com/api/v1/gallery/samsung$g_yaction"
secret="R8P6PtAlwn2bQobnedI2g7TxgqL4n091Fcq44nRh6CY-"
	
fwversion="1.3.12.C"
dockversion="1.2.68.C"

man="SEC-VD"

model="LNYYC650"

deviceid="`cat /mnt/user/ywe/deviceid`"

hwversion="LNYYC650"

swversion="T-ML09_2000.0"

region="US"
#lang="en"
lang=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])lang=[^&]+" | cut -f 2 -d "="`

yweversion="5.5.5"

yweres="960x540"

#query=$QUERY_STRING

#ID=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])id=[0-9]+" | cut -f 2 -d "=" | head -n1`
#INFO=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])info=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "="`

#g_ts=""
#g_installed=""
#g_last=""
#g_bootstrap=""
#g_devcode=""
#g_appid=""

#export g_ts=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])ts=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "="`
#export g_installed=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])installed=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "="`
#export g_last=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])last=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "="`
#export g_bootstrap=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])bootstrap=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "="`
#export g_devcode=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])devcode=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "="`
#export g_appid=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])appid=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "="`

g_ts=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])ts=[^&]+" | cut -f 2 -d "="`
g_installed=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])installed=[^&]+" | cut -f 2 -d "="`
g_last=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])last=[^&]+" | cut -f 2 -d "="`
g_bootstrap=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])bootstrap=[^&]+" | cut -f 2 -d "="`
g_devcode=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])devcode=[^&]+" | cut -f 2 -d "="`
g_appid=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])appid=[^&]+" | cut -f 2 -d "="`

export g_ts g_installed g_last g_bootstrap g_devcode g_appid

#echo g_ts=$g_ts
#echo g_installed=$g_installed
#echo g_last=$g_last
#echo g_bootstrap=$g_bootstrap
#echo g_devcode=$g_devcode
#echo g_appid=$g_appid

separator="&"

for i in g_ts g_installed g_last g_bootstrap g_devcode g_appid
do
    #if [ "${!i}" != "" ] # too bad, this variable indirection works only in bash
    export ij=`echo $i | sed 's/^g_//g'` 
    eval export ii=\$$i
    if [ "$ii" != "" ]
    then                             
        #url="$url$separator$i=${!i}"           
        #url="$url$separator$i=`eval echo \$$i`"
        #eval url="$url$separator$i=\$$i"
        url="$url$separator$ij=$ii"
	separator="&"
    fi
done

#echo url=$url

#url="$url&format=json"
#url="$url&fwversion=$fwversion"
#url="$url&dockversion=$dockversion"
#url="$url&man=$man"
#url="$url&model=$model"
#url="$url&deviceid=$deviceid"
#url="$url&hwversion=$hwversion"
#url="$url&swversion=$swversion"
#url="$url&region=$region"
#url="$url&lang=$lang"
#url="$url&yweversion=$yweversion"
#url="$url&yweres=$yweres"

url="$url&format=json&fwversion=$fwversion&dockversion=$dockversion&man=$man&model=$model&deviceid=$deviceid"
url="$url&hwversion=$hwversion&swversion=$swversion&region=$region&lang=$lang&yweversion=$yweversion&yweres=$yweres"

export url secret

#	$url=$url."&sig=".urlencode(md5($url.$secret));
url="$url&sig=`echo -n $url$secret | $md5sum | $awk '{print $1}'`"

#echo url=$url

export wget useragent

#echo "$url" >/tmp/url.log

#str=`$wget -q -U "$useragent" -O - "$url"`

#sleep 3

#export str

#str=`echo $str | sed 's#http://gallery.tv.widgets.yahoo.com/api/v1/gallery/samsung/category/#&ycat=#g' | \
#sed 's#/widgets##g' | sed 's#&ycat=#$widgetsPhpLoc?yaction=/widgets?format=json&ycat=#g'`

#str=`echo $str | sed 's@http://gallery.tv.widgets.yahoo.com/api/v1/gallery/samsung/category/@\&ycat=@g'`                      
#str=`echo $str | sed 's@/widgets@@g'`
#str=`echo $str | sed "s@\&ycat=@$widgetsPhpLoc?yaction=/widgets?format=json\&ycat=@g"` 

#str=`echo $str | sed 's@http://gallery.tv.widgets.yahoo.com/api/v1/gallery/samsung/category/@\&ycat=@g' | sed 's@/widgets@@g' | sed "s@\&ycat=@$widgetsPhpLoc?yaction=/widgets?format=json\&ycat=@g"` 

$wget -q -U "$useragent" -O - "$url" | sed 's@http://gallery.tv.widgets.yahoo.com/api/v1/gallery/samsung/category/@\&ycat=@g' | sed 's@/widgets@@g' | sed "s@\&ycat=@$widgetsPhpLoc?yaction=/widgets?format=json\&ycat=@g"


#echo $str

#echo "$str" >/tmp/str.log

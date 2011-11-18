#!/bin/sh
# update.sh by xeros, tbage, QueZt
# Source code released under GPL License

echo "Content-type: text/html"
echo ""

#debug=1

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
#####g_yaction=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])yaction=[^&]+" | cut -f 2 -d "=" | sed 's/format//g'`
##g_yaction_a="${QUERY_STRING#*\?yaction=}"
##g_yaction_b="${g_yaction_a#*\&yaction=}"
g_yaction_a="${QUERY_STRING#yaction=}"
g_yaction_e="${g_yaction_a%%\?*}"
[ "$g_yaction_e" != "$QUERY_STRING" ] && g_yaction="${g_yaction_e}"

if [ -f "/mnt/user/ywe/version" ]
then
    yweversion="`cat /mnt/user/ywe/version`"
else
    yweversion="5.5.5"
fi

useragent="Mozilla/5.0 (Samsung; U; Linux; en) Konfabulator/$yweversion"

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

#region="US"
if [ -f "/mnt/user/ywe/region" ]
then
    region="`cat /mnt/user/ywe/region`"
else
    #####region=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])region=[^&]+" | cut -f 2 -d "="`
    region_x="${QUERY_STRING#*\&region=}"
    ##region_y="${region_x#*\?region=}"
    ##[ "$region_y" != "$QUERY_STRING" ] && region="${region_y%%\&*}"
    [ "$region_x" != "$QUERY_STRING" ] && region="${region_x%%\&*}"
fi

#lang="en"
if [ -f "/mnt/user/ywe/lang" ]
then
    region="`cat /mnt/user/ywe/lang`"
else
    #####lang=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])lang=[^&]+" | cut -f 2 -d "="`
    lang_x="${QUERY_STRING#*\&lang=}"
    ##lang_y="${lang_x#*\?lang=}"
    ##[ "$lang_y" != "$QUERY_STRING" ] && lang="${lang_y%%\&*}"
    [ "$lang_x" != "$QUERY_STRING" ] && lang="${lang_x%%\&*}"
fi

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

#####g_ts=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])ts=[^&]+" | cut -f 2 -d "="`
g_ts_x="${QUERY_STRING#*\&ts=}"
##g_ts_y="${g_ts_x#*\?ts=}"
##[ "$g_ts_y" != "$QUERY_STRING" ] && g_ts="${g_ts_y%%\&*}"
[ "$g_ts_x" != "$QUERY_STRING" ] && g_ts="${g_ts_x%%\&*}"

#####g_installed=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])installed=[^&]+" | cut -f 2 -d "="`
g_installed_x="${QUERY_STRING#*\&installed=}"
##g_installed_y="${g_installed_x#*\?installed=}"
##[ "$g_installed_y" != "$QUERY_STRING" ] && g_installed="${g_installed_y%%\&*}"
[ "$g_installed_x" != "$QUERY_STRING" ] && g_installed="${g_installed_x%%\&*}"

#####g_last=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])last=[^&]+" | cut -f 2 -d "="`
g_last_x="${QUERY_STRING#*\&last=}"
##g_last_y="${g_last_x#*\?last=}"
##[ "$g_last_y" != "$QUERY_STRING" ] && g_last="${g_last_y%%\&*}"
[ "$g_last_x" != "$QUERY_STRING" ] && g_last="${g_last_x%%\&*}"

#####g_bootstrap=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])bootstrap=[^&]+" | cut -f 2 -d "="`
g_bootstrap_x="${QUERY_STRING#*\&bootstrap=}"
##g_bootstrap_y="${g_bootstrap_x#*\?bootstrap=}"
##[ "$g_bootstrap_y" != "$QUERY_STRING" ] && g_bootstrap="${g_bootstrap_y%%\&*}"
[ "$g_bootstrap_x" != "$QUERY_STRING" ] && g_bootstrap="${g_bootstrap_x%%\&*}"

#####g_devcode=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])devcode=[^&]+" | cut -f 2 -d "="`
g_devcode_x="${QUERY_STRING#*\&devcode=}"
##g_devcode_y="${g_devcode_x#*\?devcode=}"
##[ "$g_devcode_y" != "$QUERY_STRING" ] && g_devcode="${g_devcode_y%%\&*}"
[ "$g_devcode_x" != "$QUERY_STRING" ] && g_devcode="${g_devcode_x%%\&*}"

#####g_appid=`echo "$QUERY_STRING" | $grep -oE "(^|[?&])appid=[^&]+" | cut -f 2 -d "="`
g_appid_x="${QUERY_STRING#*\&appid=}"
##g_appid_y="${g_appid_x#*\?appid=}"
##[ "$g_appid_y" != "$QUERY_STRING" ] && g_appid="${g_appid_y%%\&*}"
[ "$g_appid_x" != "$QUERY_STRING" ] && g_appid="${g_appid_x%%\&*}"

export g_ts g_installed g_last g_bootstrap g_devcode g_appid

separator="?"

for i in g_ts g_installed g_last g_bootstrap g_devcode g_appid
do
    #if [ "${!i}" != "" ] # too bad, this variable indirection works only in bash
    export ij="${i#g_}"
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

#export url secret

url="$url&sig=`echo -n $url$secret | $md5sum | cut -d " " -f 1`"

#export wget useragent

#########$wget -q -U "$useragent" -O - "$url" | sed 's@http://gallery.tv.widgets.yahoo.com/api/v1/gallery/samsung/category/@\&ycat=@g' | sed 's@/widgets@@g' | sed "s@\&ycat=@$widgetsPhpLoc?yaction=/widgets?format=json\&ycat=@g"

if [ "$debug" = "1" ]
then
    mkdir -p /var/log/ywe
    $wget -q -U "$useragent" -O - "$url" | tee -a /var/log/ywe/update-answer1.log | sed -e 's@http://gallery.tv.widgets.yahoo.com/api/v1/gallery/samsung/category/@\&ycat=@g' -e 's@/widgets@@g' -e "s@\&ycat=@$widgetsPhpLoc?yaction=/widgets?format=json\&ycat=@g" | tee -a /var/log/ywe/update-answer2.log
    echo "$g_yaction" >> /var/log/ywe/update-yaction.log
    echo "$url" >> /var/log/ywe/update-url.log
    echo "$QUERY_STRING" >> /var/log/ywe/update-query.log
else
    $wget -q -U "$useragent" -O - "$url" | sed -e 's@http://gallery.tv.widgets.yahoo.com/api/v1/gallery/samsung/category/@\&ycat=@g' -e 's@/widgets@@g' -e "s@\&ycat=@$widgetsPhpLoc?yaction=/widgets?format=json\&ycat=@g"
fi

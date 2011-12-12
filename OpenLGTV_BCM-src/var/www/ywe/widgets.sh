#!/bin/sh
# widgets.sh by xeros, tbage, QueZt
# Source code released under GPL License

echo "Content-type: text/html"
echo ""

#debug=1

# needed tools, on PC native, on TV needs busybox
busybox=""                # for native tools
#busybox="/tmp/busybox "  # for busybox tools in tv
#busybox="/bin/busybox "  # for busybox tools in tv
awk="$busybox"awk
md5sum="$busybox"md5sum
httpd="$busybox"httpd
wget="$busybox"wget
#tr="$busybox"tr
grep="$busybox"grep

g_yaction_x="${QUERY_STRING#yaction=}"
g_yaction_y="${g_yaction_x%%\&*}"
[ "$g_yaction_x" != "$QUERY_STRING" ] && g_yaction="${g_yaction_x%%\?*}"

g_ycat_x="${QUERY_STRING#*\&ycat=}"
g_ycat_y="${g_ycat_x#*\?ycat=}"
g_ycat_z="${g_ycat_y%%\&*}"
[ "$g_ycat_z" != "$QUERY_STRING" ] && g_ycat="${g_ycat_z%%\/*}"

if [ -f "/mnt/user/ywe/version" ]
then
    yweversion="`cat /mnt/user/ywe/version`"
else
    yweversion="5.5.5"
fi

useragent="Mozilla/5.0 (Samsung; U; Linux; en) Konfabulator/$yweversion"
url="http://gallery.tv.widgets.yahoo.com/api/v1/gallery/samsung/category/${g_ycat}${g_yaction}"
secret="R8P6PtAlwn2bQobnedI2g7TxgqL4n091Fcq44nRh6CY-"
fwversion="1.3.12.C"
dockversion="1.2.68.C"
man="SEC-VD"
model="LNYYC650"
deviceid="`cat /mnt/user/ywe/deviceid`"
hwversion="LNYYC650"
swversion="T-ML09_2000.0"

if [ -f "/mnt/user/ywe/region" ]
then
    region="`cat /mnt/user/ywe/region`"
else
    region_x="${QUERY_STRING#*\&region=}"
    [ "$region_x" != "$QUERY_STRING" ] && region="${region_x%%\&*}"
fi

if [ -f "/mnt/user/ywe/lang" ]
then
    region="`cat /mnt/user/ywe/lang`"
else
    lang_x="${QUERY_STRING#*\&lang=}"
    [ "$g_lang_x" != "$QUERY_STRING" ] && lang="${g_lang_x%%\&*}"
fi

yweres="960x540"

g_ts_x="${QUERY_STRING#*\&ts=}"
g_installed_x="${QUERY_STRING#*\&installed=}"
g_last_x="${QUERY_STRING#*\&last=}"
g_bootstrap_x="${QUERY_STRING#*\&bootstrap=}"
g_devcode_x="${QUERY_STRING#*\&devcode=}"
g_appid_x="${QUERY_STRING#*\&appid=}"
[ "$g_ts_x" != "$QUERY_STRING" ] && g_ts="${g_ts_x%%\&*}"
[ "$g_installed_x" != "$QUERY_STRING" ] && g_installed="${g_installed_x%%\&*}"
[ "$g_last_x" != "$QUERY_STRING" ] && g_last="${g_last_x%%\&*}"
[ "$g_bootstrap_x" != "$QUERY_STRING" ] && g_bootstrap="${g_bootstrap_x%%\&*}"
[ "$g_devcode_x" != "$QUERY_STRING" ] && g_devcode="${g_devcode_x%%\&*}"
[ "$g_appid_x" != "$QUERY_STRING" ] && g_appid="${g_appid_x%%\&*}"
export g_ts g_installed g_last g_bootstrap g_devcode g_appid

separator="?"

for i in g_ts g_installed g_last g_bootstrap g_devcode g_appid
do
    #if [ "${!i}" != "" ] # too bad, this variable indirection works only in bash
    export ij="${i#g_}"
    # do we really need to substitute %20 with spaces?
    #export ii=$(eval echo $"$i" | sed 's/%20/ /g')
    eval export ii=\$$i
    if [ "$ii" != "" ]
    then                             
	url="$url$separator$ij=$ii"
	separator="&"
    fi
done

url="$url&format=json&fwversion=$fwversion&dockversion=$dockversion&man=$man&model=$model&deviceid=$deviceid"
url="$url&hwversion=$hwversion&swversion=$swversion&region=$region&lang=$lang&yweversion=$yweversion&yweres=$yweres"
url="$url&sig=`echo -n $url$secret | $md5sum | cut -d " " -f 1`"

if [ "$debug" = "1" ]
then
    mkdir -p /var/log/ywe
    $wget -q -U "$useragent" -O - "$url" | tee -a /var/log/ywe/widgets-answer.log
    echo "$g_yaction" >> /var/log/ywe/widgets-yaction.log
    echo "$url" >> /var/log/ywe/widgets-url.log
    echo "$QUERY_STRING" >> /var/log/ywe/widgets-query.log
else
    $wget -q -U "$useragent" -O - "$url"
fi

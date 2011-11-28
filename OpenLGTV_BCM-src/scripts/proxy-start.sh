#!/bin/ash
# OpenLGTV BCM script proxy-start.sh by xeros
# Proxy script for JavaScript code injection starting
# Source code released under GPL License

# proxy_log_debug values:
# 0 - no logging at all
# 1 - logging only processes
# 2 - logging whole request on stderr
# 3 - logging request and answer to file

[ -z "$proxy_custom_cfgdir" ]             && proxy_custom_cfgdir=/mnt/user/cfg/proxy   # custom proxy configs directory
[ -z "$proxy_connect_port" ]              && proxy_connect_port=80                     # default port for making connections
[ -z "$proxy_listen_port" ]               && proxy_listen_port=8888                    # proxy listening port
[ -z "$proxy_listen_port_hex" ]           && proxy_listen_port_hex=22B8                # proxy listening port written as hex
[ -z "$proxy_localhost_only" ]            && proxy_localhost_only=1                    # listen for connections on localhost (127.0.0.1) address only
#[ -z "$proxy_wait_time" ]                && proxy_wait_time=8
[ -z "$proxy_wait_time" ]                 && proxy_wait_time=4                         # timeout on connections with modified code
[ -z "$proxy_wait_moretime" ]             && proxy_wait_moretime=3                     # additional time for timeout on detected binary/not modified content
#[ -z "$proxy_log_debug" ]                && proxy_log_debug=3
[ -z "$proxy_log_debug" ]                 && proxy_log_debug=0                         # debug logs verbosity (0 - do not log anything, 1 - log processes info, 2 - log requests, 3 - log all with downloaded content to log file)
[ -z "$proxy_log_file" ]                  && proxy_log_file=/var/log/proxy.log         # log file for debug logs verbosity set to 3
[ -z "$proxy_sh" ]                        && proxy_sh=/scripts/proxy.sh                # script that manages each proxy connection
[ -z "$proxy_inject_file" ]               && proxy_inject_file=/mnt/user/www/inject.js                 # custom JavaScript file for existence check to inject
[ -z "$proxy_inject_url" ]                && proxy_inject_url="http://127.0.0.1:88/user/inject.js"     # as above, just network link - code from that file is used instead of the builtin one in proxy script

[ -f "$proxy_custom_cfgdir/adblockflt" ]  && proxy_adblock_flt="`cat $proxy_custom_cfgdir/adblockflt`" # custom adblock filter file
[ -f "$proxy_custom_cfgdir/useragent" ]   && proxy_useragent="`cat $proxy_custom_cfgdir/useragent`"    # custom useragent string file used for connections

[ -z "$proxy_adblock_flt"  ]              && proxy_adblock_flt="`cat /etc/default/proxy/adblockflt 2>/dev/null`" # default adblock filter file
[ -z "$proxy_useragent" ]                 && proxy_useragent="`cat /etc/default/proxy/useragent 2>/dev/null`"    # default useragent file

# last resort hardcoded default - in case of /etc/default/proxy/* were missing - testing on PC/other device
[ -z "$proxy_adblock_flt" ]               && proxy_adblock_flt='doubleclick\.net|emediate\.eu|googleadservices\.com|/adserver\.|/googleads\.|://ads\.|/www/delivery/|media\.richrelevance.com/rrserver/js/|/advertising/|yieldmanager\.com|pagead2\.googlesyndication\.com|hit\.gemius\.pl'
[ -z "$proxy_useragent" ]                 && proxy_useragent="Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0" # useragent string used for connections

#[ -z "$nc" ]                             && nc="busybox nc"                           # for proxy testing on PC
[ -z "$nc" ]                              && nc=nc
[ -z "$awk" ]                             && awk=awk
[ -z "$tcpsvd" ]                          && tcpsvd=tcpsvd

export proxy_custom_cfgdir proxy_listen_port proxy_log_debug proxy_log_file proxy_wait_time proxy_wait_moretime proxy_connect_port proxy_log_file proxy_inject_file proxy_inject_url proxy_adblock_flt proxy_useragent awk nc tcpsvd

export id=1

if [ "$proxy_localhost_only" = "1" ]
then
    proxy_listen_ip="127.0.0.1"
    proxy_listen_ip_hex="0100007F"
else
    proxy_listen_ip="0"
    proxy_listen_ip_hex="00000000"
fi

if [ -n "`grep $proxy_listen_ip_hex:$proxy_listen_port_hex /proc/net/tcp`" ]
then
    echo "Proxy is running!"
    exit 1
fi

if [ "$proxy_log_debug" -ge "1" ]
then
    $tcpsvd -v $proxy_listen_ip $proxy_listen_port $proxy_sh
else
    $tcpsvd $proxy_listen_ip $proxy_listen_port $proxy_sh
fi

exit 0

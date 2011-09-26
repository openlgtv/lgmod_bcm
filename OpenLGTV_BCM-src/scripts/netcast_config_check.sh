#!/bin/sh
# OpenLGTV BCM NetCast config format check v.0.0.1 by xeros
# Source code released under GPL License

# busybox egrep applet works exactly the same as grep - need to fix that
if [ ! -f "$1" ]
then
    echo "Usage: $0 /path/to/config.xml"
    export config_ver=0
    exit 1
fi

export config_xml="$1"
export tmp_cfgxml="/tmp/config.xml"
cat $1 | tr -d '\r\n' > $tmp_cfgxml

#if [ -z "`grep '<xml>' $config_xml`" -o -z "`grep '<country' $config_xml`" -o -z "`grep '<item' $config_xml`" ]
if [ -z "`egrep -e '<xml>.*<country.*<item.*</item>.*</country>.*</xml>' $tmp_cfgxml`" ]
then
    echo "Input file is not proper config.xml"
    export config_ver=0
    exit 2
fi

#if [ -n "`grep '<exec_engine>' $config_xml`" -a -n "`grep '<exec_app>' $config_xml`" -a -n "`grep 'check_network' $config_xml`" -a -n "`grep 'native' $config_xml`" ]
if [ -n "`egrep -e 'native.*check_network.*<exec_engine>.*<exec_app>' $tmp_cfgxml`" ]
then
    if [ -n "`egrep -e '<title>.*<cp_main_path>' $tmp_cfgxml`" ]
    then
	# BCM35230 SmartTV
	export config_ver=3
    else
	# BCM3549/3556 current
        export config_ver=2
    fi
else
    if [ -n "`egrep -e '<title>.*<url_exec>.*<url_icon>' $tmp_cfgxml`" ]
    then
	# BCM3549/3556 old
        export config_ver=1
    else
	echo "Input file is not proper config.xml"
        export config_ver=0
	exit 2
    fi
fi

echo "Detected config.xml version: $config_ver"
rm $tmp_cfgxml

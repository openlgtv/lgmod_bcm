#!/bin/sh
# OpenLGTV BCM NetCast config format check v.0.0.5 by xeros
# Source code released under GPL License

[ -n "$1" ] && cfg_xml="$1"

if [ ! -f "$cfg_xml" ]
then
    echo "Usage: $0 /path/to/config.xml"
    echo "or: cfg_xml=/path/to/config.xml; source $0"
    export config_ver=0
    export netcast_config_ok=0
    return 1
fi

export config_xml="$cfg_xml"
export tmp_cfgxml="/tmp/config.xml"
# first remove newlines, carriage return and tabulators but then cut lines by countries to make regex search work better
cat "$config_xml" | tr -d '\t\r\n' | head -c 1000 > $tmp_cfgxml

if [ -z "`egrep -m 1 -e '<xml>.*<country.*<item' $tmp_cfgxml`" ]
then
    echo "Input file is not proper config.xml"
    export config_ver=0
    export netcast_config_ok=0
    return 2
fi

if [ -n "`egrep -m 1 -e 'check_network.*<exec_engine>.*<exec_app>' $tmp_cfgxml`" ]
then
    if [ -n "`egrep -m 1 -e '<title>.*<cp_main_path>' $tmp_cfgxml`" ]
    then
	# BCM35230 SmartTV
	export config_ver=3
	export netcast_config_ok=0
    else
	# BCM3549/3556 current
        export config_ver=2
	export netcast_config_ok=1
    fi
else
    if [ -n "`egrep -m 1 -e '<title>.*<url_exec>.*<url_icon>' $tmp_cfgxml`" ]
    then
	# BCM3549/3556 old
        export config_ver=1
	export netcast_config_ok=1
    else
	echo "Input file is not proper config.xml"
        export config_ver=0
	export netcast_config_ok=0
	return 2
    fi
fi

echo "OpenLGTV_BCM-INFO: detected NetCast config.xml version: $config_ver"
rm $tmp_cfgxml

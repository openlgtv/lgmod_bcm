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
#cat "$config_xml" | tr -d '\t\r\n' | sed 's:\(</country>\):\1\n:g' > $tmp_cfgxml
cat "$config_xml" | tr -d '\t\r\n' | head -c 1000 > $tmp_cfgxml

#if [ -z "`grep '<xml>' $config_xml`" -o -z "`grep '<country' $config_xml`" -o -z "`grep '<item' $config_xml`" ]
#if [ -z "`egrep -e '<xml>.*<country.*<item.*</item>.*</country>.*</xml>' $tmp_cfgxml`" ]
#if [ -z "`awk '/<xml>.*<country.*<item.*<\/item>.*<\/country>.*<\/xml>/{print}' $tmp_cfgxml`" ]
#if [ -z "`egrep -m 1 -e '<xml>.*<country.*<item.*</item>.*</country>' $tmp_cfgxml`" ]
#if [ -z "`head -c 1500 $tmp_cfgxml | egrep -m 1 -e '<xml>.*<country.*<item.*</item>'`" ]
#if [ -z "`head -c 1000 $tmp_cfgxml | egrep -m 1 -e '<xml>.*<country.*<item'`" ]
if [ -z "`egrep -m 1 -e '<xml>.*<country.*<item' $tmp_cfgxml`" ]
then
    echo "Input file is not proper config.xml"
    export config_ver=0
    export netcast_config_ok=0
    return 2
fi

#if [ -n "`grep '<exec_engine>' $config_xml`" -a -n "`grep '<exec_app>' $config_xml`" -a -n "`grep 'check_network' $config_xml`" -a -n "`grep 'native' $config_xml`" ]
#if [ -n "`awk '/native.*check_network.*<exec_engine>.*<exec_app>/{print}' $tmp_cfgxml`" ]
#if [ -n "`egrep -m 1 -e 'native.*check_network.*<exec_engine>.*<exec_app>' $tmp_cfgxml`" ]
#if [ -n "`head -c 1000 $tmp_cfgxml | egrep -m 1 -e 'check_network.*<exec_engine>.*<exec_app>'`" ]
if [ -n "`egrep -m 1 -e 'check_network.*<exec_engine>.*<exec_app>' $tmp_cfgxml`" ]
then
    #if [ -n "`awk '/<title>.*<cp_main_path>/{print}' $tmp_cfgxml`" ]
    #if [ -n "`head -c 1000 $tmp_cfgxml | egrep -m 1 -e '<title>.*<cp_main_path>'`" ]
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
    #if [ -n "`awk '/<title>.*<url_exec>.*<url_icon>/{print}' $tmp_cfgxml`" ]
    #if [ -n "`head -c 1000 $tmp_cfgxml | egrep -m 1 -e '<title>.*<url_exec>.*<url_icon>'`" ]
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

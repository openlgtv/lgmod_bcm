#!/bin/ash
# OpenLGTV BCM NetCast config parser and regenerator v.0.5 by xeros
# Source code released under GPL License
echo "OpenLGTV BCM-INFO: NetCast config parser and regenerator script."

# command line
for argv in "$@"
do
    [ "${argv#config_xml=}"              != "$argv" ] && org_cfgxml="${argv#config_xml=}"
    [ "${argv#browser_application_txt=}" != "$argv" ] && org_brw_app_txt="${argv#browser_application_txt=}"
    [ "${argv#run3556=}"                 != "$argv" ] && org_run3556="${argv#run3556=}"
    [ "${argv#proxy_config_txt=}"        != "$argv" ] && proxy_config_txt="${argv#proxy_config_txt=}"
    [ "${argv#extra_conf=}"              != "$argv" ] && org_extra_conf="${argv#extra_conf=}"
    [ "$argv" = "enable_all" ]   && enable_all=1
    [ "$argv" = "add_openlgtv" ] && add_openlgtv=1
    [ "$argv" = "add_yahoo" ]    && add_yahoo=1
    [ "$argv" = "add_www" ]      && add_www=1
    [ "$argv" = "set_proxy" ]    && set_proxy=1
    [ "$argv" = "kill_browser" ] && kill_browser=1
done

oid_number=254                                #OpenLGTV BCM WebUI NetCast ID
wid_number=255                                #OpenLGTV BCM Internet Browser NetCast ID
oid_name=openlgtv                             #OpenLGTV BCM WebUI NetCast item name
yid_name=yahoo                                #Yahoo Widgets NetCast item name
wid_name=www                                  #OpenLGTV BCM Internet Browser NetCast item name
oid_link=http://127.0.0.1:88/                 #OpenLGTV BCM WebUI URL
proxy_link=http://127.0.0.1:8888/             #Web proxy for remote navigation code injection URL
wid_link=http://127.0.0.1:88/browser.cgi      #OpenLGTV BCM Internet Browser URL

tmp1_cfgxml=/tmp/config.xml.tmp1
tmp2_cfgxml=/tmp/config.xml.tmp2
new_cfgxml=/tmp/config.xml.new
bck_cfgxml=$org_cfgxml.backup
new_brw_app_txt=$org_brw_app_txt.new
bck_brw_app_txt=$org_brw_app_txt.backup
run3556_proxy=$org_run3556-proxy
extra_conf_proxy=$org_extra_conf-proxy

if [ "$1" = "" ]
then
    echo "OpenLGTV BCM-WARN: NetCast config generator"
    echo "Usage: "
    echo "$0 (action) [(options)]"
    echo "Actions:"
    echo " add_openlgtv - add OpenLGTV BCM WebUI item to config.xml and browser_application.txt (for all countries)"
    echo " add_yahoo    - add Yahoo Widgets item to config.xml"
    echo " add_www      - add OpenLGTV BCM Internet Browser item to config.xml and browser_application.txt"
    echo " set_proxy    - generate run3556-proxy, extra_conf-proxy and new proxy_config_txt files for builtin web proxy"
    echo " enable_all   - enable all NetCast services which have their available swf icons in /home/netcast_icons"
    echo "Options:"
    echo " config_xml=/path/to/config.xml"
    echo "       - config.xml file used to modify NetCast menu (needed for: add_openlgtv, add_yahoo, add_www, enable_all)"
    echo " browser_application_txt=/path/to/browser_application.txt"
    echo "       - web browser links file to modify (needed for: add_openlgtv, add_www)"
    echo " run3556=/path/to/run3556"
    echo "       - path to input run3556 (web browser starting script) do modify (needed for: set_proxy)"
    echo " proxy_config_txt=/path/to/proxy_config.txt"
    echo "       - path to output proxy_config.txt file used for web proxy configuration (needed for: set_proxy)"
    echo " extra_conf=/path/to/extra_conf"
    echo "       - path to input extra_conf file used for additional web proxy configuration (needed for: set_proxy)"
    exit 0
fi

if [ "$org_cfgxml" != "" ]
then
    if [ "$add_openlgtv" = "1" ]
    then
	echo "OpenLGTV BCM-INFO: NetCast config generator: \"add_openlgtv\" argument passed..."
	id_number="$oid_number"
	id_name="$oid_name"
	id_link="$oid_link"
    else
	if [ "$add_www" = "1" ]
	then
	    echo "OpenLGTV BCM-INFO: NetCast config generator: \"add_www\" argument passed..."
	    id_number="$wid_number"
	    id_name="$wid_name"
	    id_link="$wid_link"
	fi
    fi
    if [ ! -f "$org_cfgxml" ]; then echo "OpenLGTV BCM-ERROR: NetCast config generator: $org_cfgxml file not found!"; exit 1; fi
    if [ "$enable_all" = "1" ]
    then
	echo "OpenLGTV BCM-INFO: NetCast config generator: \"enable_all\" argument passed, regenerating new config.xml: $org_cfgxml with all services"
	cat $org_cfgxml | tr -d '\r' | sed -e 's/<!--//g' -e 's/-->//g' | sed -e 's/^ *//g' -e 's/^\t*//g' | \
	    grep -v "^$" | sed -e 's/^ *//g' | sed -e 's/>j$/>/g' | grep -v '<.*xml>' | grep -v '<.*country.*>' | \
	    tr -d '\n' | sed -e 's#</item><item#</item>\n<item#g' | sed -e 's/\"\([a-zA-Z]*\)=/\" \1=/g' | sort | uniq > $tmp1_cfgxml
	rm -f $tmp2_cfgxml
	for s_id in `cat $tmp1_cfgxml | awk '{print $2}' | sed -e 's/id=//g' -e 's/\"//g'`
	do
	    if [ -f "/home/netcast_icons/icon_$s_id.swf" ]
	    then
		cat $tmp1_cfgxml | grep "id=\"$s_id\"" >> $tmp2_cfgxml
	    fi
	done
	echo -e '<xml>\r' > $new_cfgxml
	#for cntry in `cat $org_cfgxml | grep 'country code=' | awk -F\" '{print $2}' | sort | uniq`
	for cntry in `cat $org_cfgxml | grep 'country code=' | awk -F\" '{print $2}' | grep COMMON | sort | uniq` AUS
	do
	    echo -e "\t<country code=\"$cntry\">\r" >> $new_cfgxml
	    # v- busybox sed has problems with handling '\r'
	    #cat $tmp_cfgxml | sed -e 's/^/\t\t/g'| sed -e 's/></>\r\n\t\t\t</g' -e 's#\t</item>.*#</item>\r#g' >> $new_cfgxml
	    cat $tmp2_cfgxml | sort | uniq | sed -e 's/^/\t\t/g'| sed -e 's/></>\n\t\t\t</g' -e 's#\t</item>.*#</item>#g' >> $new_cfgxml
	    echo -e "\t</country>\r" >> $new_cfgxml
	    echo -e "\r" >> $new_cfgxml
	done
	echo -e "</xml>\r" >> $new_cfgxml
	rm -f $tmp1_cfgxml
	rm -f $tmp2_cfgxml
	mv -f $new_cfgxml $org_cfgxml
    fi
    if [ "$add_openlgtv" = "1" -o "$add_www" = "1" ]
    then
	if [ -z "`grep $id_name $org_cfgxml`" ]
	then
	    echo "OpenLGTV BCM-INFO: NetCast config generator: adding \"$id_name\" id to existing config.xml: $org_cfgxml"
	    #cat $org_cfgxml | sed "s#<country code=\(.*\)#<country code=\1\n\t\t\t\t\t<item id=\"$id_name\" type=\"browser\" use_magic=\"true\" check_network=\"false\" resolution=\"1280*720\" use_com_ani=\"false\" mini_ver=\"\" >\r\n\t\t\t\t\t\t\t\t<exec_engine>/mnt/browser/run3556</exec_engine>\r\n\t\t\t\t\t\t\t\t<exec_app>$id_number</exec_app>\r\n\t\t\t\t\t</item>\r\n#g" > $new_cfgxml
	    cat $org_cfgxml | sed "s#<country code=\(.*\)#<country code=\1\n\t\t\t\t\t<item id=\"$id_name\" type=\"browser\" use_magic=\"true\" check_network=\"false\" resolution=\"1280*720\" use_com_ani=\"false\" mini_ver=\"\" >\n\t\t\t\t\t\t\t\t<exec_engine>/mnt/browser/run3556</exec_engine>\n\t\t\t\t\t\t\t\t<exec_app>$id_number</exec_app>\n\t\t\t\t\t</item>\n#g" > $new_cfgxml
	    mv -f $org_cfgxml $bck_cfgxml
	    mv -f $new_cfgxml $org_cfgxml
	else
	    echo "OpenLGTV BCM-INFO: NetCast config generator: \"$id_name\" id already exist in current config.xml"
	fi
    fi
    if [ "$add_yahoo" = "1" ]
    then
	echo "OpenLGTV BCM-INFO: NetCast config generator: \"add_yahoo\" argument passed..."
	# v- we will not check if it exists there as it exist there for sure somewhere, we need to use lock file
	#if [ -z "`grep $yid_name $org_cfgxml`" ]
	if [ ! -f "/mnt/user/lock/ywe_added_to_config_xml.lock" ]
	then
	    echo "OpenLGTV BCM-INFO: NetCast config generator: adding \"$yid_name\" id to existing config.xml: $org_cfgxml"
	    if [ -d "/mnt/addon/ywe" ]
	    then
		echo "OpenLGTV BCM-INFO: NetCast config generator: found /mnt/addon/ywe, setting it as ywedir for \"$yid_name\" in existing config.xml: $org_cfgxml"
		ywedir=/mnt/addon/ywe
	    else
		#echo "OpenLGTV BCM-INFO: NetCast config generator: NOT found /mnt/addon/ywe, setting ywedir to /mnt/usb1/Drive1/OpenLGTV_BCM/ywe for \"$yid_name\" in existing config.xml"
		echo "OpenLGTV BCM-INFO: NetCast config generator: NOT found /mnt/addon/ywe, setting ywe_konfab_sh to /scripts/konfabulator-exec.sh for \"$yid_name\" in existing config.xml: $org_cfgxml"
		ywedir=/mnt/usb1/Drive1/OpenLGTV_BCM/ywe
		ywe_konfab_sh=/scripts/konfabulator-exec.sh
	    fi
	    if [ "$ywe_konfab_sh" = "" ]; then ywe_konfab_sh=$ywedir/bin/konfabulator.sh; fi
	    cat $org_cfgxml | sed "s#<country code=\(.*\)#<country code=\1\n\t\t\t\t\t<item id=\"$yid_name\" type=\"native\" use_magic=\"true\" check_network=\"true\" resolution=\"960*540\" use_com_ani=\"false\" mini_ver=\"\" >\n\t\t\t\t\t\t\t\t<exec_engine>$ywe_konfab_sh</exec_engine>\n\t\t\t\t\t\t\t\t<option id=\"IDSTR_NETCAST_OPTION_RESTORE_YAHOO\" cmd=\"$ywedir/opt/restore_factory_setting.sh\" processMode=\"MODE_KILL\" fullpath=\"$ywe_konfab_sh\"/>\n\t\t\t\t\t</item>\n#g" > $new_cfgxml
	    mv -f $org_cfgxml $bck_cfgxml
	    mv -f $new_cfgxml $org_cfgxml
	    touch /mnt/user/lock/ywe_added_to_config_xml.lock
	else
	    if [ -n "`grep '/mnt/usb1/Drive1/OpenLGTV_BCM/ywe' $org_cfgxml`" ]
	    then
		echo "OpenLGTV BCM-WARN: NetCast config generator: found old settings for konfabulator.sh path (/mnt/usb1/Drive1/OpenLGTV_BCM/ywe) in \"$yid_name\" id, changing it to /scripts/konfabulator-exec.sh now in $org_cfgxml"
		sed -i 's#/mnt/usb1/Drive1/OpenLGTV_BCM/ywe/bin/konfabulator.sh#/scripts/konfabulator-exec.sh#g' $org_cfgxml
	    else
		echo "OpenLGTV BCM-INFO: NetCast config generator: \"$yid_name\" id should be already in current config.xml (/mnt/user/lock/ywe_added_to_config_xml.lock lockfile exist)"
	    fi
	fi
    fi
    if [ "$kill_browser" = "1" ]
    then
	echo "OpenLGTV BCM-INFO: NetCast config generator: \"kill_browser\" argument passed..."
	if [ ! -f "$org_run3556" ]; then echo "OpenLGTV BCM-ERROR: NetCast config generator: $org_run3556 file not found!"; exit 1; fi
	if [ -z "`grep '^killall lb4wk' $org_run3556`" ]
	    then
	    echo "OpenLGTV BCM-INFO: NetCast config generator: adding \"killall lb4wk\" at the beginning of existing run3556 script: $org_run3556"
	    #cat $org_cfgxml | sed 's:#!/bin/sh:#!/bin/sh\nkillall lb4wk:g' > $new_cfgxml
	    sed -i -e 's:#!/bin/sh:#!/bin/sh\nkillall lb4wk:g' $org_run3556
	else
	    echo "OpenLGTV BCM-INFO: NetCast config generator: \"killall lb4wk\" already exist in current run3556 script: $org_cfgxml"
	fi
    fi
    if [ "$org_brw_app_txt" != "" ]
    then
	if [ ! -f "$org_brw_app_txt" ]; then echo "OpenLGTV BCM-ERROR: NetCast config generator: $org_brw_app_txt file not found!"; exit 1; fi
	#is_id_openlgtv="`grep ^254 $org_brw_app_txt | grep \"http://127.0.0.1/\"`"
	is_id_openlgtv="`grep ^$id_number $org_brw_app_txt`"
	is_id_openlgtv_link="`grep ^$id_number $org_brw_app_txt | grep \"$id_link\"`"
	#if [ -z "$is_id_openlgtv_link" ]
	if [ -z "$is_id_openlgtv" ]
	then
	    echo "OpenLGTV BCM-INFO: NetCast config generator: adding \"$id_name\" id $id_number link: $id_link to existing browser_application.txt file: $org_brw_app_txt"
	    cp -f $org_brw_app_txt $new_brw_app_txt
	    #echo '254\thttp://127.0.0.1/\t1\t1\t1\t1\t1\t1\t0\ten\t1\t1\t1\t1\r\n' >> $new_brw_app_txt
	    #echo "$id_number\thttp://127.0.0.1/\t1\t1\t1\t1\t1\t1\t0\ten\t1\t1\t1\t1\r\n" >> $new_brw_app_txt
	    echo -e "$id_number\t$id_link\t1\t1\t1\t1\t1\t1\t0\ten\t1\t1\t1\t1\r\n" >> $new_brw_app_txt
	    mv -f $org_brw_app_txt $bck_brw_app_txt
	    mv -f $new_brw_app_txt $org_brw_app_txt
	else
	    if [ -z "$is_id_openlgtv_link" ]
	    then
		echo "OpenLGTV BCM-WARN: NetCast config generator: found incorrect link to \"$id_name\" id: $id_number, changing to new link: $id_link in existing browser_application.txt file"
		cp -f $org_brw_app_txt $new_brw_app_txt
		sed -i -e "s#^$id_number.*#$id_number\t$id_link\t1\t1\t1\t1\t1\t1\t0\ten\t1\t1\t1\t1#g" $new_brw_app_txt
		mv -f $org_brw_app_txt $bck_brw_app_txt
		mv -f $new_brw_app_txt $org_brw_app_txt
	    else
		echo "OpenLGTV BCM-INFO: NetCast config generator: \"$id_name\" id: $id_number link: $id_link already exist in current browser_application.txt: $org_brw_app_txt"
	    fi
	fi
    fi
fi

if [ "$org_run3556" != "" ]
then
    if [ "$set_proxy" = "1" -a "$org_extra_conf" != "" -a "$proxy_config_txt" != "" ]
    then
	if [ ! -f "$org_run3556" ];    then echo "OpenLGTV BCM-ERROR: NetCast config generator: $org_run3556 file not found!"; exit 1; fi
	if [ ! -f "$org_extra_conf" ]; then echo "OpenLGTV BCM-ERROR: NetCast config generator: $org_extra_conf file not found!"; exit 1; fi
	if [ ! -f "$run3556_proxy" -o ! -f "$proxy_config_txt" -o ! -f "$extra_conf_proxy" ]
	then
	    echo "OpenLGTV BCM-INFO: NetCast config generator: setting \"$wid_name\" id: $wid_number link: $wid_link for proxy in $proxy_config_txt"
	    cat "$org_run3556" | \
		sed -e 's/^export MAX_CONNECTION=.*/export MAX_CONNECTION=1/g' \
		    -e 's/^export MAX_CONNECTION_PER_HOST=/export MAX_CONNECTION_PER_HOST=1/g' \
		    -e "s#^export PROXY_CONFIG_FILE_PATH=.*#export PROXY_CONFIG_FILE_PATH=\"$proxy_config_txt\"#g" \
		    -e "s#^EXTRA_CONF=.*#EXTRA_CONF=\"$extra_conf_proxy\"#g" \
		    > $run3556_proxy
	    echo -e "$wid_number\t$proxy_link\n" >> "$proxy_config_txt"
	    echo "OpenLGTV BCM-INFO: NetCast config generator: $run3556_proxy file generated with proxy setup"
	    cat "$org_extra_conf" | \
		sed -e "s#^export PROXY_CONFIG_FILE_PATH=.*#export PROXY_CONFIG_FILE_PATH=\"$proxy_config_txt\"#g" \
		    > $extra_conf_proxy
	    echo "OpenLGTV BCM-INFO: NetCast config generator: $extra_conf_proxy file generated with proxy setup"
	else
	    echo "OpenLGTV BCM-INFO: NetCast config generator: all needed scripts are already configured for proxy"
	fi
    fi
fi

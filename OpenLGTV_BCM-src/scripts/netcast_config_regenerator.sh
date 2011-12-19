#!/bin/sh
# OpenLGTV BCM NetCast config parser and regenerator v.0.8.4 by xeros
# Source code released under GPL License

echo "OpenLGTV_BCM-INFO: NetCast config parser and regenerator script."

# variables
oid_number=254                                #OpenLGTV BCM WebUI NetCast ID
wid_number=255                                #OpenLGTV BCM Internet Browser NetCast ID
oid_name=openlgtv                             #OpenLGTV BCM WebUI NetCast item name
yid_name=yahoo                                #Yahoo Widgets NetCast item name
wid_name=www                                  #OpenLGTV BCM Internet Browser NetCast item name
oid_link=http://127.0.0.1:88/                 #OpenLGTV BCM WebUI URL
proxy_link=http://127.0.0.1:8888/             #Web proxy for remote navigation code injection URL
wid_link=http://127.0.0.1:88/browser.cgi      #OpenLGTV BCM Internet Browser URL
[ -z "$config_ver" ] && config_ver=2          #default config.xml format version
country_groups="KR US BR EU CN AU SG ZA VN TW XA XB IL ID MY IR ZZ"
proxy_MAX_CONNECTION=6                        #maximum number of simulatenous connections on proxy - looks like even web browser version 4.0.xx ignores that
proxy_MAX_CONNECTION_PER_HOST=4               #maximum number of simulatenous connections per host on proxy - looks like even web browser version 4.0.xx ignores that

#INFO:
#proxy is not supported by web browser versions 3.0.xx

# default configs paths - should get new values with command line arguments
org_cfgxml=/mnt/user/netcast/config.xml
org_brw_app_txt=/mnt/user/netcast/browser_application.txt
org_run3556=/mnt/user/netcast/run3556
org_extra_conf=/mnt/user/netcast/extra_conf
proxy_config_txt=/mnt/user/netcast/proxy_config-proxy.txt

# command line
argc=0
for argv in "$@"
do
    [ "${argv#config_xml=}"              != "$argv"        ] && org_cfgxml="${argv#config_xml=}"
    [ "${argv#browser_application_txt=}" != "$argv"        ] && org_brw_app_txt="${argv#browser_application_txt=}"
    [ "${argv#run3556=}"                 != "$argv"        ] && org_run3556="${argv#run3556=}"
    [ "${argv#extra_conf=}"              != "$argv"        ] && org_extra_conf="${argv#extra_conf=}"
    [ "${argv#proxy_config_txt=}"        != "$argv"        ] && proxy_config_txt="${argv#proxy_config_txt=}"
    [ "${argv#add=}"                     != "$argv"        ] && add="${argv#add=}"
    [ "${argv#del=}"                     != "$argv"        ] && del="${argv#del=}"
    [ "${argv#config_ver=}"              != "$argv"        ] && config_ver="${argv#config_ver=}"
    [ "$argv"                             = "enable_all"   ] && enable_all=1
    [ "$argv"                             = "set_proxy"    ] && set_proxy=1
    [ "$argv"                             = "unset_proxy"  ] && unset_proxy=1
    [ "$argv"                             = "kill_browser" ] && kill_browser=1
    argc=$(($argc+1))
done

#echo argc $argc argv "$@"

# temporary variables
tmp1_cfgxml=/tmp/config.xml.tmp1
tmp2_cfgxml=/tmp/config.xml.tmp2
new_cfgxml=/tmp/config.xml.new
bck_cfgxml=$org_cfgxml.backup
new_brw_app_txt=$org_brw_app_txt.new
bck_brw_app_txt=$org_brw_app_txt.backup
run3556_proxy=$org_run3556-proxy
extra_conf_proxy=$org_extra_conf-proxy

if [ "$argc" = "0" ]
then
    #echo "OpenLGTV_BCM-WARN: NetCast config generator"
    echo "Usage: "
    echo "$0 (action) [(options)]"
    echo "Actions:"
    echo " add=openlgtv - add OpenLGTV_BCM WebUI item to config.xml and browser_application.txt (for all countries)"
    echo " add=yahoo    - add Yahoo Widgets item to config.xml"
    echo " add=www      - add OpenLGTV_BCM Internet Browser item to config.xml and browser_application.txt"
    echo " del=...      - remove any item from config.xml file"
    echo " config_ver=..- set config.xml file version: 1 - old 2010 model firmwares, 2 - new 2010 model firmwares, 3 - 2011 model firmwares"
    echo " set_proxy    - generate run3556-proxy, extra_conf-proxy and new proxy_config_txt files for builtin web proxy"
    echo " unset_proxy  - remove run3556-proxy, extra_conf-proxy and proxy_config_txt files and change OpenLGTV_BCM Internet Browser item in config_xml file"
    echo " enable_all   - enable all NetCast services which have their available swf icons in /home/netcast_icons"
    echo " kill_browser - modify run3556 adding 'killall lb4wk GtkLauncher' at the beginning to kill old web browser instances at each run"
    echo "Options:"
    echo " config_xml=/path/to/config.xml"
    echo "       - config.xml file used to modify NetCast menu (needed for all actions)"
    echo " browser_application_txt=/path/to/browser_application.txt"
    echo "       - web browser links file to modify (needed for: add=openlgtv, add=www)"
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
    if [ ! -f "$org_cfgxml" ]; then echo "OpenLGTV_BCM-ERROR: NetCast config generator: $org_cfgxml file not found!"; exit 1; fi
    if [ "$add" = "openlgtv" -o "$del" = "openlgtv" ]
    then
	id_number="$oid_number"
	id_name="$oid_name"
	id_link="$oid_link"
    else
	if [ "$add" = "www" -o "$del" = "www" ]
	then
	    id_number="$wid_number"
	    id_name="$wid_name"
	    id_link="$wid_link"
	fi
    fi
    if [ "$enable_all" = "1" ]
    then
	echo "OpenLGTV_BCM-INFO: NetCast config generator: \"enable_all\" argument passed, regenerating new config.xml: $org_cfgxml, config_ver: $config_ver with all services"
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
	# v- that might not contain all country groups
	#for cntry in `cat $org_cfgxml | grep 'country code=' | awk -F\" '{print $2}' | grep COMMON | sort | uniq` AUS
	for cntryx in $country_groups
	do
	    cntry=${cntryx}_COMMON
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
    if [ "$add" != "" ]
    then
	echo "OpenLGTV_BCM-INFO: NetCast config generator: \"add=$add\" argument passed..."
	case "$add" in
		openlgtv | www)
			if [ -z "`grep -m 1 id=.$id_name.\  $org_cfgxml`" ]
			then
			    echo "OpenLGTV_BCM-INFO: NetCast config generator: adding \"$id_name\" id to existing config.xml: $org_cfgxml, config_ver: $config_ver"
			    if [ "$config_ver" = "2" ]
			    then
				#cat $org_cfgxml | sed "s#<country code=\(.*\)#<country code=\1\n\t\t\t\t\t<item id=\"$id_name\" type=\"browser\" use_magic=\"true\" check_network=\"false\" resolution=\"1280*720\" use_com_ani=\"false\" mini_ver=\"\" >\r\n\t\t\t\t\t\t\t\t<exec_engine>/mnt/browser/run3556</exec_engine>\r\n\t\t\t\t\t\t\t\t<exec_app>$id_number</exec_app>\r\n\t\t\t\t\t</item>\r\n#g" > $new_cfgxml
				cat $org_cfgxml | sed "s#<country code=\(.*\)#<country code=\1\n\t\t\t\t\t<item id=\"$id_name\" type=\"browser\" use_magic=\"true\" check_network=\"false\" resolution=\"1280*720\" use_com_ani=\"false\" mini_ver=\"\" >\n\t\t\t\t\t\t\t\t<exec_engine>/mnt/browser/run3556</exec_engine>\n\t\t\t\t\t\t\t\t<exec_app>$id_number</exec_app>\n\t\t\t\t\t</item>\n#g" > $new_cfgxml
			    else
				if [ "$config_ver" = "1" ]
				then
				    cat $org_cfgxml | sed "s#<country code=\(.*\)#<country code=\1\n\t\t\t\t\t<item id=\"$id_name\" type=\"c\" use_portal=\"false\">\r\n\t\t\t\t\t\t\t\t<title>$id_name</title>\r\n\t\t\t\t\t\t\t\t<url_exec>/mnt/browser/run3556</url_exec>\r\n\t\t\t\t\t\t\t\t<exec_id>$id_number</exec_id>\r\n\t\t\t\t\t\t\t\t<url_icon>netcast/icon_${id_name}.swf</url_icon>\r\n\t\t\t\t\t</item>\r\n#g" > $new_cfgxml
				else
				    echo "OpenLGTV_BCM-ERROR: NetCast config generator: there is no support for config_ver: $config_ver config.xml: $org_cfgxml yet"
				fi
			    fi
			    mv -f $org_cfgxml $bck_cfgxml
			    mv -f $new_cfgxml $org_cfgxml
			else
			    echo "OpenLGTV_BCM-INFO: NetCast config generator: \"$id_name\" id already exist in current config.xml: $org_cfgxml config_ver: $config_ver"
			fi
			if [ "$org_brw_app_txt" != "" ]
			then
			    if [ ! -f "$org_brw_app_txt" ]; then echo "OpenLGTV_BCM-ERROR: NetCast config generator: $org_brw_app_txt file not found!"; exit 1; fi
			    #is_id_openlgtv="`grep ^254 $org_brw_app_txt | grep \"http://127.0.0.1/\"`"
			    is_id_openlgtv="`grep -m 1 ^$id_number $org_brw_app_txt`"
			    is_id_openlgtv_link="`grep -m 1 ^$id_number $org_brw_app_txt | grep -m 1 \"$id_link\"`"
			    #if [ -z "$is_id_openlgtv_link" ]
			    if [ -z "$is_id_openlgtv" ]
			    then
				echo "OpenLGTV_BCM-INFO: NetCast config generator: adding \"$id_name\" id $id_number link: $id_link config_ver: $config_ver to existing browser_application.txt file: $org_brw_app_txt"
				cp -f $org_brw_app_txt $new_brw_app_txt
				#echo '254\thttp://127.0.0.1/\t1\t1\t1\t1\t1\t1\t0\ten\t1\t1\t1\t1\r\n' >> $new_brw_app_txt
				#echo "$id_number\thttp://127.0.0.1/\t1\t1\t1\t1\t1\t1\t0\ten\t1\t1\t1\t1\r\n" >> $new_brw_app_txt
				if [ "$config_ver" = "2" ]
				then
				    echo -e "$id_number\t$id_link\t1\t1\t1\t1\t1\t1\t0\ten\t1\t1\t1\t1\r\n" >> $new_brw_app_txt
				else
				    if [ "$config_ver" = "1" ]
				    then
					echo -e "$id_number\t$id_link\t1\t1\t1\t1\t1\t1\t0\ten\t1\r\n" >> $new_brw_app_txt
				    else
					echo "OpenLGTV_BCM-ERROR: NetCast config generator: there is no support for config_ver: $config_ver config.xml: $org_cfgxml yet"
				    fi
				fi
				mv -f $org_brw_app_txt $bck_brw_app_txt
				mv -f $new_brw_app_txt $org_brw_app_txt
			    else
				if [ -z "$is_id_openlgtv_link" ]
				then
				    echo "OpenLGTV_BCM-WARN: NetCast config generator: found incorrect link to \"$id_name\" id: $id_number config_ver: $config_ver, changing to new link: $id_link in existing browser_application.txt file"
				    cp -f $org_brw_app_txt $new_brw_app_txt
				    if [ "$config_ver" = "2" ]
				    then
					sed -i -e "s#^$id_number.*#$id_number\t$id_link\t1\t1\t1\t1\t1\t1\t0\ten\t1\t1\t1\t1#g" $new_brw_app_txt
				    else
					if [ "$config_ver" = "1" ]
					then
					    sed -i -e "s#^$id_number.*#$id_number\t$id_link\t1\t1\t1\t1\t1\t1\t0\ten\t1#g" $new_brw_app_txt
					else
					    echo "OpenLGTV_BCM-ERROR: NetCast config generator: there is no support for config_ver: $config_ver config.xml: $org_cfgxml yet"
					fi
				    fi
				    mv -f $org_brw_app_txt $bck_brw_app_txt
				    mv -f $new_brw_app_txt $org_brw_app_txt
				else
				    echo "OpenLGTV_BCM-INFO: NetCast config generator: \"$id_name\" id: $id_number link: $id_link already exist in current browser_application.txt: $org_brw_app_txt"
				fi
			    fi
			fi
			;;
		yahoo)
			# v- we will not check if it exists there as it exist there for sure somewhere, we need to use lock file
			#if [ -z "`grep $yid_name $org_cfgxml`" ]
			#if [ ! -f "/mnt/user/lock/ywe_added_to_config_xml.lock" ]
			if [ "`grep -m 3 id=.$yid_name.\  $org_cfgxml | wc -l`" -le "2" ]
			then
			    echo "OpenLGTV_BCM-INFO: NetCast config generator: adding \"$yid_name\" id to existing config.xml: $org_cfgxml config_ver: $config_ver"
			    if [ -d "/mnt/addon/ywe" ]
			    then
				echo "OpenLGTV_BCM-INFO: NetCast config generator: found /mnt/addon/ywe, setting it as ywedir for \"$yid_name\" in existing config.xml: $org_cfgxml"
				ywedir=/mnt/addon/ywe
				ywe_konfab_sh=/scripts/konfabulator-exec.sh
			    else
				#echo "OpenLGTV_BCM-INFO: NetCast config generator: NOT found /mnt/addon/ywe, setting ywedir to /mnt/usb1/Drive1/OpenLGTV_BCM/ywe for \"$yid_name\" in existing config.xml"
				echo "OpenLGTV_BCM-INFO: NetCast config generator: NOT found /mnt/addon/ywe, setting ywe_konfab_sh to /scripts/konfabulator-exec.sh for \"$yid_name\" in existing config.xml: $org_cfgxml"
				ywedir=/mnt/usb1/Drive1/OpenLGTV_BCM/ywe
				ywe_konfab_sh=/scripts/konfabulator-exec.sh
			    fi
			    if [ "$ywe_konfab_sh" = "" ]; then ywe_konfab_sh=$ywedir/bin/konfabulator.sh; fi
			    if [ "$config_ver" = "2" ]
			    then
				cat $org_cfgxml | sed "s#<country code=\(.*\)#<country code=\1\n\t\t\t\t\t<item id=\"$yid_name\" type=\"native\" use_magic=\"true\" check_network=\"true\" resolution=\"960*540\" use_com_ani=\"false\" mini_ver=\"\" >\n\t\t\t\t\t\t\t\t<exec_engine>$ywe_konfab_sh</exec_engine>\n\t\t\t\t\t\t\t\t<option id=\"IDSTR_NETCAST_OPTION_RESTORE_YAHOO\" cmd=\"$ywedir/opt/restore_factory_setting.sh\" processMode=\"MODE_KILL\" fullpath=\"$ywe_konfab_sh\"/>\n\t\t\t\t\t</item>\n#g" > $new_cfgxml
			    else
				if [ "$config_ver" = "1" ]
				then
				    cat $org_cfgxml | sed "s#<country code=\(.*\)#<country code=\1\n\t\t\t\t\t<item id=\"$yid_name\" type=\"c\" use_portal=\"true\">\r\n\t\t\t\t\t\t\t\t<title>$yid_name</title>\r\n\t\t\t\t\t\t\t\t<url_exec>$ywe_konfab_sh</url_exec>\r\n\t\t\t\t\t\t\t\t<url_icon>netcast/icon_${yid_name}.swf</url_icon>\r\n\t\t\t\t\t\t\t\t<option id=\"IDSTR_NETCAST_OPTION_RESTORE_YAHOO\" cmd=\"$ywedir/opt/restore_factory_setting.sh\" processMode=\"MODE_KILL\" fullpath=\"$ywe_konfab_sh\"/>\r\n\t\t\t\t\t</item>\r\n#g" > $new_cfgxml
				else
				    echo "OpenLGTV_BCM-ERROR: NetCast config generator: there is no support for config_ver: $config_ver config.xml: $org_cfgxml yet"
				fi
			    fi
			    mv -f $org_cfgxml $bck_cfgxml
			    mv -f $new_cfgxml $org_cfgxml
			    #touch /mnt/user/lock/ywe_added_to_config_xml.lock
			else
			    if [ -z "`egrep -m 1 '/scripts/konfabulator-exec.sh' $org_cfgxml`" ]
			    then
				if [ -n "`grep '/mnt/usb1/Drive1/OpenLGTV_BCM/ywe' $org_cfgxml`" ]
				then
				    echo "OpenLGTV_BCM-WARN: NetCast config generator: found old settings for konfabulator.sh path (/mnt/usb1/Drive1/OpenLGTV_BCM/ywe/bin) in \"$yid_name\" id, changing it to /scripts/konfabulator-exec.sh now in $org_cfgxml"
				    sed -i 's#/mnt/addon/ywe/bin/konfabulator.sh#/scripts/konfabulator-exec.sh#g' $org_cfgxml
				else
				    if [ -n "`grep '/mnt/addon/ywe/bin/konfabulator.sh' $org_cfgxml`" ]
				    then
					echo "OpenLGTV_BCM-WARN: NetCast config generator: found orig settings for konfabulator.sh path (/mnt/addon/ywe/bin/) in \"$yid_name\" id, changing it to /scripts/konfabulator-exec.sh now in $org_cfgxml"
					sed -i 's#/mnt/addon/ywe/bin/konfabulator.sh#/scripts/konfabulator-exec.sh#g' $org_cfgxml
				    else
					echo "OpenLGTV_BCM-INFO: NetCast config generator: \"$yid_name\" id should be already in current config.xml"
				    fi
				fi
			    fi
			fi
			;;
		*)
			echo "OpenLGTV_BCM-ERROR: NetCast config generator: \"add=$add\" argument is NOT SUPPORTED!"
			exit 1
			;;
	esac
    fi
    if [ "$del" != "" ]
    then
	echo "OpenLGTV_BCM-INFO: NetCast config generator: \"del=$del\" argument passed..."
	#if [ -n "`grep id=.$id_name $org_cfgxml`" ]
	if [ -n "`grep -m 1 id=.$del.\  $org_cfgxml`" ]
	then
	    echo "OpenLGTV_BCM-INFO: NetCast config generator: removing \"$del\" id from existing config.xml: $org_cfgxml config_ver: $config_ver"
	    if [ "$config_ver" = "2" -o "$config_ver" = "1" ]
	    then
		#cat $org_cfgxml | \
		#    sed -n -e "1h;1!H;\${;g;s#<item id=\"$del\"[^<]*[<]*[^<]*[<]*[^<]*[<]*[^<]*[<]*[^<]*[<]*[^<]*[<]*[^<]*[<]*[^<]*[<]*[^<]*</item>[^<]*##g;p;}" \
		#	> $new_cfgxml
		cat "$org_cfgxml" | \
		    sed -n -e '1h;1!H;${;g;s#<item id="'"$del"'"[^<]*<*[^<]*<*[^<]*<*[^<]*<*[^<]*<*[^<]*<*[^<]*<*[^<]*<*[^<]*</item>[^<]*##g;p;}' \
			> "$new_cfgxml"
	    else
		echo "OpenLGTV_BCM-ERROR: NetCast config generator: there is no support for config_ver: $config_ver config.xml: $org_cfgxml yet"
	    fi
	    mv -f $new_cfgxml $org_cfgxml
	else
	    echo "OpenLGTV_BCM-INFO: NetCast config generator: \"$del\" id does not exist in current config.xml"
	fi
    fi
    if [ "$kill_browser" = "1" ]
    then
	echo "OpenLGTV_BCM-INFO: NetCast config generator: \"kill_browser\" argument passed..."
	if [ ! -f "$org_run3556" ]; then echo "OpenLGTV_BCM-ERROR: NetCast config generator: $org_run3556 file not found!"; exit 1; fi
	if [ -z "`grep -m 1 '^killall lb4wk GtkLauncher' $org_run3556`" ]
	    then
	    echo "OpenLGTV_BCM-INFO: NetCast config generator: adding \"killall lb4wk GtkLauncher\" at the beginning of existing run3556 script: $org_run3556"
	    #cat $org_cfgxml | sed 's:#!/bin/sh:#!/bin/sh\nkillall lb4wk:g' > $new_cfgxml
	    sed -i -e 's:#!/bin/sh:#!/bin/sh\nkillall lb4wk GtkLauncher > /dev/null 2>\&1:g' $org_run3556
	else
	    echo "OpenLGTV_BCM-INFO: NetCast config generator: \"killall lb4wk GtkLauncher\" already exist in current run3556 script: $org_cfgxml"
	fi
    fi
    if [ "$org_run3556" != "" ]
    then
	if [ "$set_proxy" = "1" -a "$org_extra_conf" != "" -a "$proxy_config_txt" != "" ]
	then
	    if [ ! -f "$org_run3556" ];    then echo "OpenLGTV_BCM-ERROR: NetCast config generator: $org_run3556 file not found!"; exit 1; fi
	    if [ ! -f "$org_extra_conf" ]; then echo "OpenLGTV_BCM-ERROR: NetCast config generator: $org_extra_conf file not found!"; exit 1; fi
	    if [ -z "`grep -m 1 id=.$wid_name.\  $org_cfgxml`" ]; then echo "OpenLGTV_BCM-ERROR: NetCast config generator: id $wid_name not found in config.xml file, you should use add=$widname parameter first!"; exit 1; fi
	    if [ "$kill_browser" = "1" -a -f "$run3556_proxy" ]
	    then
		if [ -z "`grep -m 1 '^killall lb4wk GtkLauncher' $run3556_proxy`" ]
		then
		    echo "OpenLGTV_BCM-INFO: NetCast config generator: removing old web browser with proxy starting script ($run3556_proxy) to prepare new one"
		fi
	    fi
	    if [ ! -f "$run3556_proxy" -o ! -f "$proxy_config_txt" -o ! -f "$extra_conf_proxy" ]
	    then
		echo "OpenLGTV_BCM-INFO: NetCast config generator: setting \"$wid_name\" id: $wid_number link: $wid_link for proxy in $proxy_config_txt"
		cat "$org_run3556" | \
		    sed -e "s/^export MAX_CONNECTION=.*/export MAX_CONNECTION=$proxy_MAX_CONNECTION/g" \
			-e "s/^export MAX_CONNECTION_PER_HOST=.*/export MAX_CONNECTION_PER_HOST=$proxy_MAX_CONNECTION_PER_HOST/g" \
			-e "s#^export PROXY_CONFIG_FILE_PATH=.*#export PROXY_CONFIG_FILE_PATH=\"$proxy_config_txt\"#g" \
			-e "s#^EXTRA_CONF=.*#EXTRA_CONF=\"$extra_conf_proxy\"#g" \
			> $run3556_proxy
		chmod 755 $run3556_proxy
		echo -e "$wid_number\t$proxy_link\n" >> "$proxy_config_txt"
		echo "OpenLGTV_BCM-INFO: NetCast config generator: $run3556_proxy file generated with proxy setup"
		cat "$org_extra_conf" | \
		    sed -e "s#^export PROXY_CONFIG_FILE_PATH=.*#export PROXY_CONFIG_FILE_PATH=\"$proxy_config_txt\"#g" \
			> $extra_conf_proxy
		chmod 755 $extra_conf_proxy
		echo "OpenLGTV_BCM-INFO: NetCast config generator: $extra_conf_proxy file generated with proxy setup"
		cat $org_cfgxml | tr -d '\r' | \
		    sed -n -e "1h;1!H;\${;g;s#\(<item id=\"$wid_name\"[^<]*[<]*[^<]*[<]*[^<]*<[A-Za-z_]*exec[A-Za-z_]*>\)\/mnt\/browser\/run3556#\1\/mnt\/user\/netcast\/run3556-proxy#g;p;}" \
			> $new_cfgxml
		mv -f $new_cfgxml $org_cfgxml
		echo "OpenLGTV_BCM-INFO: NetCast config generator: $org_cfgxml file regenerated with proxy setup for id: $wid_name"
	    else
		echo "OpenLGTV_BCM-INFO: NetCast config generator: all needed scripts are already configured for proxy"
	    fi
	fi
	#echo TODO: should it remove files or just disable proxy?
	if [ "$unset_proxy" = "1" -a "$org_extra_conf" != "" -a "$proxy_config_txt" != "" ]
	then
	    echo "OpenLGTV_BCM-INFO: NetCast config generator: disabling proxy for all services"
	    cat $org_cfgxml | sed "s#$run3556_proxy#$org_run3556#g" > $new_cfgxml
	    mv -f $new_cfgxml $org_cfgxml
	    if [ -f "$extra_conf_proxy" -a -f "$proxy_config_txt" -a -f "$run3556_proxy" ]
	    then 
		rm -f "$extra_conf_proxy" "$proxy_config_txt" "$run3556_proxy"
	    fi
	fi
    fi
fi

#!/bin/sh
# OpenLGTV BCM NetCast config parser and regenerator v.0.3
echo "OpenLGTV BCM-INFO: NetCast config parser and regenerator script."
if [ "$1" != "" ]
then
    id_number=254
    id_name=openlgtv
    id_link=http://127.0.0.1:88/
    yid_name=yahoo
    org_cfgxml=$1
    tmp_cfgxml=$org_cfgxml.tmp
    new_cfgxml=$org_cfgxml.new
    bck_cfgxml=$org_cfgxml.backup
    if [ "$2" = "enable_all" ]
    then
	echo "OpenLGTV BCM-INFO: NetCast config generator: \"enable_all\" argument passed, regenerating new config.xml with all services"
	cat $org_cfgxml | sed 's/\r//g' | sed 's/<!--//g' | sed 's/-->//g' | sed 's/^ *//g' | sed 's/^\t*//g' | grep -v "^$" | sed 's/^ *//g' | sed 's/>j$/>/g' | grep -v '<.*xml>' | grep -v '<.*country.*>' | tr -d '\n' | sed 's#</item><item#</item>\n<item#g' | sed 's/\"\([a-zA-Z]*\)=/\" \1=/g' | sort | uniq > $tmp_cfgxml
	echo -e '<xml>\r' > $new_cfgxml
	#for cntry in `cat $org_cfgxml | grep 'country code=' | awk -F\" '{print $2}' | sort | uniq`
	for cntry in `cat $org_cfgxml | grep 'country code=' | awk -F\" '{print $2}' | grep COMMON | sort | uniq`
	do
	    echo -e "\t<country code=\"$cntry\">\r" >> $new_cfgxml
	    cat $tmp_cfgxml | sed 's/^/\t\t/g'| sed 's/></>\r\n\t\t\t</g' | sed 's#\t</item>.*#</item>\r#g' >> $new_cfgxml
	    echo -e "\t</country>\r" >> $new_cfgxml
	    echo -e "\r" >> $new_cfgxml
	done
	echo -e "</xml>\r" >> $new_cfgxml
	rm $tmp_cfgxml
    else
	if [ "$2" = "add_openlgtv" ]
	then
	    echo "OpenLGTV BCM-INFO: NetCast config generator: \"add_openlgtv\" argument passed..."
	    if [ -z "`grep $id_name $org_cfgxml`" ]
	    then
		echo "OpenLGTV BCM-INFO: NetCast config generator: adding \"$id_name\" id to existing config.xml"
		#cat $org_cfgxml | sed "s#<country code=\(.*\)#<country code=\1\n\t\t\t\t\t<item id=\"$id_name\" type=\"browser\" use_magic=\"true\" check_network=\"false\" resolution=\"1280*720\" use_com_ani=\"false\" mini_ver=\"\" >\r\n\t\t\t\t\t\t\t\t<exec_engine>/mnt/browser/run3556</exec_engine>\r\n\t\t\t\t\t\t\t\t<exec_app>$id_number</exec_app>\r\n\t\t\t\t\t</item>\r\n#g" > $new_cfgxml
		cat $org_cfgxml | sed "s#<country code=\(.*\)#<country code=\1\n\t\t\t\t\t<item id=\"$id_name\" type=\"browser\" use_magic=\"true\" check_network=\"false\" resolution=\"1280*720\" use_com_ani=\"false\" mini_ver=\"\" >\n\t\t\t\t\t\t\t\t<exec_engine>/mnt/browser/run3556</exec_engine>\n\t\t\t\t\t\t\t\t<exec_app>$id_number</exec_app>\n\t\t\t\t\t</item>\n#g" > $new_cfgxml
		mv $org_cfgxml $bck_cfgxml
		mv $new_cfgxml $org_cfgxml
	    else
		echo "OpenLGTV BCM-INFO: NetCast config generator: \"$id_name\" id already exist in current config.xml"
	    fi
	else
	    if [ "$2" = "add_yahoo" ]
	    then
		echo "OpenLGTV BCM-INFO: NetCast config generator: \"add_yahoo\" argument passed..."
		# v- we will not check if it exists there as it exist there for sure somewhere, we need to use lock file
		#if [ -z "`grep $yid_name $org_cfgxml`" ]
		if [ ! -f "/mnt/user/lock/ywe_added_to_config_xml.lock" ]
		then
		    echo "OpenLGTV BCM-INFO: NetCast config generator: adding \"$yid_name\" id to existing config.xml"
		    if [ -d "/mnt/addon/ywe" ]
		    then
			echo "OpenLGTV BCM-INFO: NetCast config generator: found /mnt/addon/ywe, setting it as ywedir for \"$yid_name\" in existing config.xml"
			ywedir=/mnt/addon/ywe
		    else
			#echo "OpenLGTV BCM-INFO: NetCast config generator: NOT found /mnt/addon/ywe, setting ywedir to /mnt/usb1/Drive1/OpenLGTV_BCM/ywe for \"$yid_name\" in existing config.xml"
			echo "OpenLGTV BCM-INFO: NetCast config generator: NOT found /mnt/addon/ywe, setting ywe_konfab_sh to /scripts/konfabulator-exec.sh for \"$yid_name\" in existing config.xml"
			ywedir=/mnt/usb1/Drive1/OpenLGTV_BCM/ywe
			ywe_konfab_sh=/scripts/konfabulator-exec.sh
		    fi
		    if [ "$ywe_konfab_sh" = "" ]; then ywe_konfab_sh=$ywedir/bin/konfabulator.sh; fi
		    cat $org_cfgxml | sed "s#<country code=\(.*\)#<country code=\1\n\t\t\t\t\t<item id=\"$yid_name\" type=\"native\" use_magic=\"true\" check_network=\"true\" resolution=\"960*540\" use_com_ani=\"false\" mini_ver=\"\" >\n\t\t\t\t\t\t\t\t<exec_engine>$ywe_konfab_sh</exec_engine>\n\t\t\t\t\t\t\t\t<option id=\"IDSTR_NETCAST_OPTION_RESTORE_YAHOO\" cmd=\"$ywedir/opt/restore_factory_setting.sh\" processMode=\"MODE_KILL\" fullpath=\"$ywe_konfab_sh\"/>\n\t\t\t\t\t</item>\n#g" > $new_cfgxml
		    mv $org_cfgxml $bck_cfgxml
		    mv $new_cfgxml $org_cfgxml
		    touch /mnt/user/lock/ywe_added_to_config_xml.lock
		else
		    if [ -n "`grep '/mnt/usb1/Drive1/OpenLGTV_BCM/ywe' $org_cfgxml`" ]
		    then
			echo "OpenLGTV BCM-WARN: NetCast config generator: found old settings for konfabulator.sh path (/mnt/usb1/Drive1/OpenLGTV_BCM/ywe) in \"$yid_name\" id, changing it to /scripts/konfabulator-exec.sh now..."
			sed -i 's#/mnt/usb1/Drive1/OpenLGTV_BCM/ywe/bin/konfabulator.sh#/scripts/konfabulator-exec.sh#g' $org_cfgxml
		    else
			echo "OpenLGTV BCM-INFO: NetCast config generator: \"$yid_name\" id should be already in current config.xml (/mnt/user/lock/ywe_added_to_config_xml.lock lockfile exist)"
		    fi
		fi
	    fi
	fi
	if [ "$3" != "" ]
	then
	    org_brw_app_txt=$3
	    new_brw_app_txt=$3.new
	    bck_brw_app_txt=$3.backup
	    #is_id_openlgtv="`grep ^254 $org_brw_app_txt | grep \"http://127.0.0.1/\"`"
	    is_id_openlgtv="`grep ^$id_number $org_brw_app_txt`"
	    is_id_openlgtv_link="`grep ^$id_number $org_brw_app_txt | grep \"$id_link\"`"
	    #if [ -z "$is_id_openlgtv_link" ]
	    if [ -z "$is_id_openlgtv" ]
	    then
		echo "OpenLGTV BCM-INFO: NetCast config generator: adding \"$id_name\" id $id_number link: $id_link to existing browser_application.txt file"
		cp -f $org_brw_app_txt $new_brw_app_txt
		#echo '254\thttp://127.0.0.1/\t1\t1\t1\t1\t1\t1\t0\ten\t1\t1\t1\t1\r\n' >> $new_brw_app_txt
		#echo "$id_number\thttp://127.0.0.1/\t1\t1\t1\t1\t1\t1\t0\ten\t1\t1\t1\t1\r\n" >> $new_brw_app_txt
		echo -e "$id_number\t$id_link\t1\t1\t1\t1\t1\t1\t0\ten\t1\t1\t1\t1\r\n" >> $new_brw_app_txt
		mv $org_brw_app_txt $bck_brw_app_txt
		mv $new_brw_app_txt $org_brw_app_txt
	    else
		if [ -z "$is_id_openlgtv_link" ]
		then
		    echo "OpenLGTV BCM-WARN: NetCast config generator: found incorrect link to \"$id_name\" id: $id_number, changing to new link: $id_link in existing browser_application.txt file"
		    cp -f $org_brw_app_txt $new_brw_app_txt
		    sed -i -e "s#^$id_number.*#$id_number\t$id_link\t1\t1\t1\t1\t1\t1\t0\ten\t1\t1\t1\t1#g" $new_brw_app_txt
		    mv $org_brw_app_txt $bck_brw_app_txt
		    mv $new_brw_app_txt $org_brw_app_txt
		else
		    echo "OpenLGTV BCM-INFO: NetCast config generator: \"$id_name\" id: $id_number link: $id_link already exist in current browser_application.txt"
		fi
	    fi
	fi
    fi
else
    echo "OpenLGTV BCM-WARN: NetCast config generator: usage: `basename $0` /path/to/config.xml [add_openlgtv|enable_all] [/path/to/browser_application.txt]"
fi

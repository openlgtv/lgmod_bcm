#!/bin/sh
# OpenLGTV BCM NetCast config parser and regenerator
echo "OpenLGTV BCM-INFO: NetCast config parser and regenerator script."
if [ "$1" != "" ]
then
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
	    if [ -z "`grep openlgtv $org_cfgxml`" ]
	    then
		echo "OpenLGTV BCM-INFO: NetCast config generator: adding \"openlgtv\" id to exitsting config.xml"
		cat $org_cfgxml | sed 's#<country code=\(.*\)#<country code=\1\n\t\t\t\t\t<item id=\"openlgtv\" type=\"browser\" use_magic=\"true\" check_network=\"false\" resolution=\"1280*720\" use_com_ani=\"false\" mini_ver=\"\" >\r\n\t\t\t\t\t\t\t\t<exec_engine>/mnt/browser/run3556</exec_engine>\r\n\t\t\t\t\t\t\t\t<exec_app>254</exec_app>\r\n\t\t\t\t\t</item>\r\n#g' > $new_cfgxml
		mv $org_cfgxml $bck_cfgxml
		mv $new_cfgxml $org_cfgxml
	    else
		echo "OpenLGTV BCM-INFO: NetCast config generator: \"openlgtv\" id already exist in current config.xml"
	    fi
	fi
	if [ "$3" != "" ]
	then
	    org_brw_app_txt=$3
	    new_brw_app_txt=$3.new
	    bck_brw_app_txt=$3.backup
	    is_id_openlgtv="`grep ^254 $org_brw_app_txt | grep \"http://127.0.0.1/\"`"
	    if [ -z "$is_id_openlgtv" ]
	    then
		echo "OpenLGTV BCM-INFO: NetCast config generator: adding \"openlgtv\" id 254 to exitsting browser_application.txt file"
		cp -f $org_brw_app_txt $new_brw_app_txt
		echo '254\thttp://127.0.0.1/\t1\t1\t1\t1\t1\t1\t0\ten\t1\t1\t1\t1\r\n' >> $new_brw_app_txt
		mv $org_brw_app_txt $bck_brw_app_txt
		mv $new_brw_app_txt $org_brw_app_txt
	    else
		echo "OpenLGTV BCM-INFO: NetCast config generator: \"openlgtv\" id 254 already exist in current browser_application.txt"
	    fi
	fi
    fi
else
    echo "OpenLGTV BCM-WARN: NetCast config generator: usage: `basename $0` /path/to/config.xml [add_openlgtv|enable_all] [/path/to/browser_application.txt]"
fi

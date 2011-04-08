#!/bin/sh
# OpenLGTV BCM NetCast config parser and regenerator
echo "OpenLGTV BCM-INFO: NetCast config parser and regenerator script."
if [ "$1" != "" ]
then
    org_cfgxml=$1
    tmp_cfgxml=$org_cfgxml.tmp
    new_cfgxml=$org_cfgxml.new
    if [ "$2" = "enable_all" ]
    then
	echo "OpenLGTV BCM-INFO: NetCast generator: \"enable_all\" argument passed, regenerating new config.xml with all services"
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
	    echo "TODO"
	fi
    fi
else
    echo "OpenLGTV BCM-WARN: NetCast generator: usage: `basename $0` /path/to/config.xml [add_openlgtv|enable_all]"
fi

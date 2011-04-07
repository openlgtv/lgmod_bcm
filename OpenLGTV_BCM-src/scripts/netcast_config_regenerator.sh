#!/bin/sh
org_cfgxml=$1
tmp_cfgxml=$org_cfgxml.tmp
new_cfgxml=$org_cfgxml.new
cat $org_cfgxml | sed 's/\r//g' | sed 's/<!--//g' | sed 's/-->//g' | sed 's/^ *//g' | sed 's/^\t*//g' | grep -v "^$" | sed 's/^ *//g' | sed 's/>j$/>/g' | grep -v '<.*xml>' | grep -v '<.*country.*>' | tr -d '\n' | sed 's#</item><item#</item>\n<item#g' | sed 's/\"\([a-zA-Z]*\)=/\" \1=/g' | sort | uniq > $tmp_cfgxml
echo '<xml>\r' > $new_cfgxml
for cntry in `cat $org_cfgxml | grep 'country code=' | awk -F\" '{print $2}' | sort | uniq`
do
    echo "\t<country code=\"$cntry\">\r" >> $new_cfgxml
    cat $tmp_cfgxml | sed 's/^/\t\t/g'| sed 's/></>\r\n\t\t\t</g' | sed 's#\t</item>.*#</item>\r#g' >> $new_cfgxml
    echo "\t</country>\r" >> $new_cfgxml
    echo "\r" >> $new_cfgxml
done
echo "</xml>\r" >> $new_cfgxml
rm $tmp_cfgxml

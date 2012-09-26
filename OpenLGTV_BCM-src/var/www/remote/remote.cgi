#!/usr/bin/haserl
content-type: text/plain

<?
# get key code (K_5, K_MUTE ...)
action="$GET_key"

# pass key code to the send_key.sh script
if [ -n "$action" ]
then
    /scripts/send_key.sh "$action" &

    # return OK to the Web client
    # any other returned value will be considered as error
    echo "OK"
else
    echo "ERROR: no key value has been sent"
fi
?>
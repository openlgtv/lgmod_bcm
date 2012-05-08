#!/usr/bin/haserl
Content-type: application/octet-stream
<?
    [ -z "$FORM_type" ] && FORM_type="`stat -c "%F" "$FORM_file"`"
    [ "$FORM_type" = "directory" ] && filename="`basename "$FORM_file"`.tar" || filename="`basename "$FORM_file"`"
    echo "Content-Disposition: attachment; filename=\"$filename\""
    echo ""
    if [ "$FORM_type" = "directory" ]
    then
	tar cO "$FORM_file" 2>/dev/null
    else
	cat "$FORM_file" 2>/dev/null
    fi
?>
#!/usr/bin/haserl
Content-type: application/octet-stream
<?
echo "Content-Disposition: attachment; filename=\"`basename $FORM_file`\""
echo ""
cat "$FORM_file" ?>
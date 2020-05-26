#!/bin/sh

GENLIST=$(git shortlog -s -n | cut -f2 | sort -f)
GENLIST_W_MAIL=$(git shortlog -s -e -n | cut -f2 | sort -f)
AUTHORSFILE="$(dirname $0)/../AUTHORS"
TEMPAUTHORSFILE="/tmp/python-escpos-authorsfile"

if [ "$#" -eq 1 ]
    then
        echo "$GENLIST">$TEMPAUTHORSFILE
	echo "\nAuthorsfile in version control:\n"
	cat $AUTHORSFILE
	echo "\nNew authorsfile:\n"
	cat $TEMPAUTHORSFILE
	echo "\nUsing diff on files...\n"
	diff --suppress-common-lines -b --from-file $AUTHORSFILE $TEMPAUTHORSFILE
	echo "Authors with mail addresses:\n"
	echo "$GENLIST_W_MAIL"
    else
	echo "$GENLIST">$AUTHORSFILE
fi


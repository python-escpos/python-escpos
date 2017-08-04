#!/bin/sh

GENLIST=$(git shortlog -s -n | cut -f2 | sort)
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
        diff -q --from-file $AUTHORSFILE $TEMPAUTHORSFILE
    else
	echo "$GENLIST">$AUTHORSFILE
fi


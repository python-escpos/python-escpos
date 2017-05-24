#!/bin/sh

git shortlog -s -n | cut -f2 | sort

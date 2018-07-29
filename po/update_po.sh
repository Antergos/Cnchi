#!/bin/sh

find . -name "*.po" | while read i;
do
   msgmerge "$i" cnchi.pot -o new.po;
   mv new.po "$i";
done

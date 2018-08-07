#!/bin/sh

# You need lingua.
# sudo pip install lingua

cd /usr/share/cnchi/po
#rm Cnchi-0.14.x/utils/info.py
pot-create ../../cnchi/src
mv messages.pot cnchi.pot

find . -name "*.po" | while read i;
do
   msgmerge "$i" cnchi.pot -o new.po;
   mv new.po "$i";
done

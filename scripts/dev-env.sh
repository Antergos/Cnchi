#!/bin/bash

# If no repo argument is passed do not continue

if [ "$1" = "" ]; then
echo "You must specify a repo: 
         -a , --antergos = antergos/master
         -l , --lots0logs = lots0logs/master
         -k , --karasu = karasu/master" && exit 1;
fi

# Update mirrorlist
echo "Updating mirror list..."
su -c "reflector -l 10 -f 10 --save /etc/pacman.d/mirrorlist";

# Update pacman databases
echo "Updating package databases..."
su -c "pacman -Sy";

# Install git
echo "Installing git..."
su -c "pacman -S git --noconfirm";

# Clone Cnchi repo
echo "Cloning Cnchi repo"
git='git clone https://github.com/'
antergos='Antergos/Cnchi.git'
dustin='lots0logs/Cnchi.git'

if [ "$1" = "-a" ]; then
${git}${antergos};
elif [ "$1" = "-l" ]; then
${git}${dustin};
cd Cnchi
git config --global user.email "dustin@falgout.us";
git config --global user.name "Dustin Falgout";
git remote add upstream https://github.com/Antergos/Cnchi.git;
else
echo git clone unsuccessful exit 1;
fi



# Insert Cnchi into system
echo "Creating symlinks"
su -c "rm -R /usr/share/cnchi && ln -s /home/antergos/Cnchi /usr/share/cnchi"
su -c "sed -i 's%/usr/share/cnchi/cnchi.py%/usr/share/cnchi/cnchi.py -d i -v -p /home/antergos/Cnchi/data/packages.xml%g' /usr/bin/cnchi"

exit;

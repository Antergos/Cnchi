#!/bin/bash

previous="/tmp/dev-setup"
uefi="/sys/firmware/efi"
vbox_chk="$(hwinfo --gfxcard | grep -o -m 1 "VirtualBox")"
notify="$1"
notify_user () {

        notify-send -t 10000 -a "Cnchi" -i /usr/share/cnchi/data/antergos-icon.png "$1"
}

# Check if this is the first time we are executed.
if ! [ -f "${previous}" ]; then
	touch ${previous};
	# Find the best mirrors (fastest and latest)
    notify_user "Selecting the best mirrors..."
	echo "Selecting the best mirrors..."
	echo "Testing Arch mirrors..."
	reflector -p http -l 30 -f 5 --save /etc/pacman.d/mirrorlist;
	echo "Done."
	sudo -u antergos wget http://antergos.info/antergos-mirrorlist
	echo "Testing Antergos mirrors..."
	rankmirrors -n 0 -r antergos antergos-mirrorlist > /tmp/antergos-mirrorlist
	cp /tmp/antergos-mirrorlist /etc/pacman.d/
	echo "Done."
	# Install any packages that haven't been added to the iso yet but are needed.
	notify_user "Installing missing packages..."
	echo "Installing missing packages..."
	# Check if system is UEFI boot.
	if [ -d "${uefi}" ]; then
		pacman -Syy git efibootmgr --noconfirm --needed;
	else
		pacman -Syy git --noconfirm --needed;
	fi
	# Enable kernel modules and other services
	if [[ "${vbox_chk}" == "VirtualBox" ]] && [ -d "${uefi}" ]; then
		echo "VirtualBox detected. Checking kernel modules and starting services."
		modprobe -a vboxsf f2fs efivarfs dm-mod && systemctl restart vboxservice;
	elif [[ "${vbox_chk}" == "VirtualBox" ]]; then
		modprobe -a vboxsf f2fs dm-mod && systemctl restart vboxservice;
	else
		modprobe -a f2fs dm-mod;
	fi
	# Update Cnchi with latest testing code
	echo "Removing existing Cnchi..."
	rm -R /usr/share/cnchi;
	cd /usr/share;
	notify_user "Getting latest version of Cnchi from testing branch..."
	echo "Getting latest version of Cnchi from testing branch..."
	# Check commandline arguments to choose repo
	#if [ "$1" = "-d" ] || [ "$1" = "--dev-repo" ]; then
	#	git clone https://github.com/"$2"/Cnchi.git cnchi;
	#else
	#	git clone https://github.com/Antergos/Cnchi.git cnchi;
	#fi
	cd /tmp
	wget http://antergos.org/cnchi.tar
	tar -xvf cnchi.tar
	cp -R cnchi/tmp/cnchi /usr/share
	rm cnchi.tar && rm -Rf cnchi
	cd /usr/share/cnchi
	
else
    notify_user "Previous testing setup detected, skipping downloads..."
	echo "Previous testing setup detected, skipping downloads..."
	echo "Verifying that nothing is mounted from a previous install attempt."
	umount -lf /install/boot >/dev/null 2&>1
	umount -lf /install >/dev/null 2&>1
	# Check for changes on github since last time script was executed
	# Update Cnchi with latest testing code
	notify_user "Getting latest version of Cnchi from testing branch..."
	echo "Getting latest version of Cnchi from testing branch..."
	#cd /usr/share/cnchi
	#git pull origin master;
	cd /tmp
	wget http://antergos.org/cnchi.tar
	tar -xvf cnchi.tar
	cp -R cnchi/tmp/cnchi /usr/share
	cd /usr/share/cnchi
fi

# Start Cnchi with appropriate options
notify_user "Starting Cnchi..."
echo "Starting Cnchi..."
# Are we using an alternate PKG cache?
# TODO Remove this nonsense and use proper command argument processing
if [ "$1" != "-d" ] && [ "$1" != "--dev-repo" ] && [ "$1" != "" ]; then
    if [ "$1" = "-c" ] || [ "$1" = "--cache" ]; then
        if [ "$2" != "" ]; then
            if [ "$3" = "-z" ]; then
                cnchi -d -v -z -c "$2" -p /usr/share/cnchi/data/packages.xml & exit 0;
            else
                cnchi -d -v -c "$2" -p /usr/share/cnchi/data/packages.xml & exit 0;
            fi
        else
            cnchi -d -v -c /media/sf_data/PKG-CACHE/pkg/ -p /usr/share/cnchi/data/packages.xml & exit 0;
        fi
    fi
elif [ "$1" = "-d" ] || [ "$1" = "--dev-repo" ]; then
    cnchi -d -v -z -p /usr/share/cnchi/data/packages.xml & exit 0;
else
    cnchi -d -v &
    exit 0;
fi

exit 1;

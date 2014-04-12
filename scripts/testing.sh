#!/bin/bash

previous="/tmp/dev-setup"
uefi="/sys/firmware/efi"
vbox_chk="$(hwinfo --gfxcard | grep -o -m 1 "VirtualBox")"

# Check if this is the first time we are executed.
if ! [ -f "${previous}" ]; then
	touch ${previous};
	# Find the best mirrors (fastest and latest)
	echo "Updating mirrorlist..."
	reflector -p http -l 30 -f 5 --save /etc/pacman.d/mirrorlist;
	# Install any packages that haven't been added to the iso yet but are needed.
	echo "Installing missing packages..."
	# Check if system is UEFI boot.
	if [ -d "${uefi}" ]; then
		pacman -Sy git grub os-prober efibootmgr f2fs-tools --noconfirm --needed;
	else
		pacman -Sy git grub os-prober f2fs-tools --noconfirm --needed;
	fi
	# Enable kernel modules and other services
	if [[ "${vbox_chk}" == "VirtualBox" ]] && [ -d "${uefi}" ]; then
		echo "VirtualBox detected. Checking kernel modules and starting services."
		modprobe -a vboxsf f2fs efivarfs dm-mod && systemctl start vboxservice;
	elif [[ "${vbox_chk}" == "VirtualBox" ]]; then
		modprobe -a vboxsf f2fs dm-mod && systemctl start vboxservice;
	else
		modprobe -a f2fs dm-mod;
	fi
	# Update Cnchi with latest testing code
	echo "Removing existing Cnchi..."
	rm -R /usr/share/cnchi;
	cd /usr/share;
	echo "Getting latest version of Cnchi from testing branch..."
	# Check commandline arguments to choose repo
	if [ "$1" = "-d" ] || [ "$1" = "--dev-repo" ]; then
		git clone https://github.com/"$2"/Cnchi.git cnchi;
	else
		git clone https://github.com/Antergos/Cnchi.git cnchi;
	fi
	cd /usr/share/cnchi
	
else
	echo "Previous testing setup detected, skipping downloads"
	# Check for changes on github since last time script was executed
	# Update Cnchi with latest testing code
	echo "Getting latest version of Cnchi from testing branch..."
	# Check commandline arguments to choose repo
	cd /usr/share/cnchi
	git pull origin master;
fi

# Start Cnchi with appropriate options
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
    cnchi -d -v -p /usr/share/cnchi/data/packages.xml & exit 0;
fi

exit 1;
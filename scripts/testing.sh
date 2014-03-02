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
	if [ "$1" = "-a" ] || [ "$1" = "--antergos" ] || [ "$1" = "--Antergos" ]; then
		git clone https://github.com/Antergos/Cnchi.git cnchi;
	else
		git clone https://github.com/lots0logs/Cnchi.git cnchi;
	fi
	cd /usr/share/cnchi
	echo "Switching to testing branch..."
	git checkout testing;
else
	echo "Previous testing setup detected, skipping downloads"
	# Check for changes on github since last time script was executed
	cd /usr/share/cnchi
	echo "Checking github for changes since last run..."
	git pull origin testing;
fi

# Start Cnchi with appropriate options
echo "Starting Cnchi..."
# Are we using an alternate PKG cache?
if [ "$2" = "-c" ] || [ "$1" = "--cache" ]; then
    if [ "$3" != "" ]; then
        cnchi -d -v -z -c "$3" -p /usr/share/cnchi/data/packages.xml &
    else
        cnchi -d -v -z -c /media/sf_data/PKG-CACHE/pkg/ -p /usr/share/cnchi/data/packages.xml &
    fi
else
    cnchi -d -v -p /usr/share/cnchi/data/packages.xml &
fi

exit 0;

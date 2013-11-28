#! /bin/bash
set -e

# Set tab to 2.
# This script installs the GRUB2 theme in the themes sub-directory under GRUB's
# directory.
#
# Version 2.1
# Copyright (C) 2011,2012 Towheed Mohammed

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details at <http://www.gnu.org/licenses/>.

# Set properties of theme
# The theme will be installed in a dir with this name.
theme_name='Antergos-Bluez'

# Filename of theme definition file.
theme_definition_file='theme.txt'

# Filename of the image to use for the terminal background.
background_image='background.png'

# The resolution the theme was designed to show best at, 640x480, 1024x768 etc,
# or "any" for any resolution (resolution independent).
theme_resolution='any'

#Set variables for color.
bold='\E[1m'
red_bold='\E[1;31m'
blue_bold='\E[1;34m'
cyan_bold='\E[1;36m'
green_bold='\E[1;32m'
normal='\E[0m'

msg_yes_no="[${green_bold} y${normal}es ${green_bold}n${normal}o ] "
msg_overwrite_create="[${green_bold} o${normal}verwrite ${green_bold}c${normal}reate ] "

# Directory containing theme files to install.
self=$(dirname $0)

# ### DO NOT CHANGE THIS ### GRUB's minimum version for theme support.
let grub_min_version=198

# Default installtion of GRUB.
grub_prefix_default="/boot/grub"

# Check that the script is being run as root.
if [[ $(id -u) != 0 ]] ; then
	echo -e "${red_bold}Please run this script with root privileges.${normal}"
	exit 0
fi

# Write variables to <grub_sysconfdir/default/grub.
set_grub_var () {
	i=$(sed -n "s,^#\?\s\?$1,&,p" "${grub_conffile}")
	if [[ -z "$i" ]] ; then
		echo -e "\n$1$2" >> "${grub_conffile}"
	else
		sed -i.bak "s,^#\?\s\?$1.*,$3$1$2," "${grub_conffile}"
	fi
}

# Check that grub-mkconfig or grub2-mkconfig exists.
grub_mkconfig_script=$(echo $(which grub-mkconfig grub2-mkconfig 2>/dev/null))
if [[ -z "${grub_mkconfig_script}" ]] ; then
	echo -e "${red_bold}Could not locate grub-mkconfig or grub2-mkconfig in your path.${normal}"
	exit 0
fi

# Get GRUB's directory from grub(2)-mkconfig. This ensures we find GRUB's
# directory regardless of it's name across distros.
grub_prefix=$(sed -n "s,^GRUB_PREFIX=.*'\(.*\)'.*,\1,p" "${grub_mkconfig_script}" | \
						sed 's,//*,/,g')
# GRUB 2.00 does not set GRUB_PREFIX in grub-mkconfig.  
if [[ -z "${grub_prefix}" ]] ; then
	grub_prefix="${grub_prefix_default}"
fi
grub_cfg="${grub_prefix}/grub.cfg"

# Use the system configuration directory from grub(2)-mkconfig.
grub_sysconfdir=$(sed -n 's,^sysconfdir=,,p' "${grub_mkconfig_script}" | sed 's,",,g')
grub_conffile="${grub_sysconfdir}/default/grub"

# Get GRUB's version from grub(2)-mkconfig and exit the script if it's < 1.98.
grub_version=$(sed -n 's,^PACKAGE_VERSION=\([0-9]\).\([0-9]*\).*,\1\2,p' \
							${grub_mkconfig_script})
if (( "${grub_version}" < "${grub_min_version}" )) ; then
	echo -e "${red_bold}GRUB must be at least version ${grub_min_version:0:1}.\
${grub_min_version:1:2}.${normal}"
	exit 0
fi

# Check that /grub_sysconfdir/default/grub exists.
if [[ ! -f "${grub_conffile}" ]] ; then
	echo -e "${red_bold}Could not locate ${grub_conffile}.${normal}"
	exit 0
fi

# Create the theme's directory.  If directory already exists, ask the user if
# they would like to overwrite the contents with the new theme or create a new
# theme directory.
theme_dir="${grub_prefix}/themes/${theme_name}"
while [[ -d "${theme_dir}" ]] ; do
	echo -e "${blue_bold}Directory ${bold_cyan}${theme_dir}${bold_blue} already exists!${normal}"
	echo -en "Would you like to overwrite it's contents or create a new directory?\
 ${msg_overwrite_create}"
	read response
	case ${response} in
		c|create)
			echo -n "Please enter a new name for the theme's directory: "
			read response
			theme_dir="${grub_prefix}/themes/${response}";;
		o|overwrite)
			echo -e "${red_bold}This will delete all files in ${cyan_bold}${theme_dir}${normal}."
			echo -en "Are you sure? ${msg_yes_no}"
			read response
			case ${response} in
				y|yes)
					rm -r "${theme_dir}";;
				*)
					exit 0;;
			esac;;
		*)
			exit 0;;
	esac
done

mkdir -p "${theme_dir}"
echo -e "Installing theme to: ${cyan_bold}${theme_dir}${normal}."

# Copy the theme's files to the theme's directory.
for i in ${self}/* ; do
	cp -r "${i}" "${theme_dir}/$(basename "${i}")"
done

# Check whether an icons directory exists.  If icons are not included in this
# theme, check if one exists in <grub_prefix>/themes/icons.  If it exists, ask
# the user if they would like to use it.
if [[ ! -d "${self}/icons" && -d "${grub_prefix}/themes/icons" ]] ; then
	echo -e "${blue_bold}An icons directory was not included in this theme."
	echo -e "However, one was found in ${cyan_bold}${grub_prefix}/themes/icons\
${blue_bold} containing these files:${normal}"
	find "${grub_prefix}/themes/icons -type f"
	echo -en "Would you like to use these icons? ${msg_yes_no}"
	read response
	case ${response} in
		y|yes)
			cp -r "${grub_prefix}/themes/icons ${theme_dir}"/;;
		*)
			echo -e "${blue_bold}This theme will not show any icons.${normal}";;
	esac
elif [[ ! -d "${self}/icons" && ! -d "${grub_prefix}/themes/icons" ]] ; then
	echo -e "${blue_bold}Could not find an icons directory.  This theme will not \
show any icons.${normal}"
fi

# Ask the user if they would like to set the theme as their new theme.
#echo -en "Would you like to set this as your new theme? ${msg_yes_no}"
#read response
#if [[ ${response} = "yes" || ${response} = "y" ]] ; then
	# Set GRUB's resolution to match that of the theme.
	if [[ "${theme_resolution}" != "any" ]] ; then
		set_grub_var 'GRUB_GFXMODE=' "${theme_resolution}"
	fi
	# Set the background image.
	if [[ ! -z "${background_image}" ]] ; then
		set_grub_var 'GRUB_BACKGROUND=' $(echo "${theme_dir}/${background_image}")
	else
	  set_grub_var '#GRUB_BACKGROUND=' '' '#'
	fi
	# Set the theme.
	set_grub_var 'GRUB_THEME=' $(echo "${theme_dir}/${theme_definition_file}")

	# Generate new grub.cfg
	$("${grub_mkconfig_script}" -o "${grub_cfg}")
#fi
exit 0

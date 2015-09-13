#!/usr/bin/bash

# -*- coding: utf-8 -*-
#
#  postinstall.sh
#
#  Copyright © 2013-2015 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; If not, see <http://www.gnu.org/licenses/>.

set_xorg() {
	cp /usr/share/cnchi/scripts/postinstall/50-synaptics.conf ${CN_DESTDIR}/etc/X11/xorg.conf.d/50-synaptics.conf
	cp /usr/share/cnchi/scripts/postinstall/99-killX.conf ${CN_DESTDIR}/etc/X11/xorg.conf.d/99-killX.conf

	# Fix sensitivity for chromebooks
	if lsmod | grep -q cyapa; then
		cp /usr/share/cnchi/scripts/postinstall/50-cros-touchpad.conf ${CN_DESTDIR}/etc/X11/xorg.conf.d/50-cros-touchpad.conf
	fi
}

set_gsettings() {
	cp /usr/share/cnchi/scripts/set-settings "${CN_DESTDIR}/usr/bin/set-settings"
	chmod +x "${CN_DESTDIR}/usr/bin/set-settings"

	# I dont know why this isn't working but I don't have anymore time to mess with it right now
	#systemd-nspawn -D "${CN_DESTDIR}" -u "${CN_USER_NAME}" /usr/bin/set-settings "${CN_DESKTOP}" 2>&1

	mkdir -p "${CN_DESTDIR}/var/run/dbus"
	mount --rbind /var/run/dbus "${CN_DESTDIR}/var/run/dbus"
	chroot "${CN_DESTDIR}" sudo -u ${CN_USER_NAME} /usr/bin/set-settings ${CN_DESKTOP} > /dev/null 2>&1

	rm ${CN_DESTDIR}/usr/bin/set-settings
	umount -l "${CN_DESTDIR}/var/run/dbus"
}

gnome_settings() {
	# Set gsettings input-source
	if [[ "${CN_KEYBOARD_VARIANT}" != '' ]]; then
		sed -i "s/'us'/'${CN_KEYBOARD_LAYOUT}+${CN_KEYBOARD_VARIANT}'/" /usr/share/cnchi/scripts/set-settings
	else
		sed -i "s/'us'/'${CN_KEYBOARD_LAYOUT}'/" /usr/share/cnchi/scripts/set-settings
	fi

	# Set gsettings
	set_gsettings

	# Set gdm shell logo
	cp /usr/share/antergos/logo.png ${CN_DESTDIR}/usr/share/antergos/
	#systemd-nspawn -D "${CN_DESTDIR}" -u gdm -M CN_GDM gsettings set org.gnome.login-screen logo "/usr/share/antergos/logo.png" &
	#sleep 5;
	#machinectl poweroff CN_GDM

	## Set default directories
	chroot ${CN_DESTDIR} su -c xdg-user-dirs-update ${CN_USER_NAME}

	# Set skel directory
	cp -R ${CN_DESTDIR}/home/${CN_USER_NAME}/.config ${CN_DESTDIR}/etc/skel

	# xscreensaver config
	cp /usr/share/cnchi/scripts/postinstall/xscreensaver ${CN_DESTDIR}/home/${CN_USER_NAME}/.xscreensaver
	cp ${CN_DESTDIR}/home/${CN_USER_NAME}/.xscreensaver ${CN_DESTDIR}/etc/skel

	if [[ -f ${CN_DESTDIR}/etc/xdg/autostart/xscreensaver.desktop ]]; then
		rm ${CN_DESTDIR}/etc/xdg/autostart/xscreensaver.desktop
	fi

	# Ensure that Light Locker starts before gnome-shell
	sed -i 's|echo "X|/usr/bin/light-locker \&\nsleep 3; echo "X|g' ${CN_DESTDIR}/etc/lightdm/Xsession
}

cinnamon_settings() {
	# Set gsettings input-source
	if [[ "${CN_KEYBOARD_VARIANT}" != '' ]]; then
		sed -i "s/'us'/'${CN_KEYBOARD_LAYOUT}+${CN_KEYBOARD_VARIANT}'/" /usr/share/cnchi/scripts/set-settings
	else
		sed -i "s/'us'/'${CN_KEYBOARD_LAYOUT}'/" /usr/share/cnchi/scripts/set-settings
	fi
	# copy antergos menu icon
	mkdir -p ${CN_DESTDIR}/usr/share/antergos/
	cp /usr/share/antergos/antergos-menu.png ${CN_DESTDIR}/usr/share/antergos/antergos-menu.png

	# Set gsettings
	set_gsettings

	# Copy menu@cinnamon.org.json to set menu icon
	mkdir -p ${CN_DESTDIR}/home/${CN_USER_NAME}/.cinnamon/configs/menu@cinnamon.org/
	cp -f /usr/share/cnchi/scripts/postinstall/menu@cinnamon.org.json ${CN_DESTDIR}/home/${CN_USER_NAME}/.cinnamon/configs/menu@cinnamon.org/

	# Copy panel-launchers@cinnamon.org.json to set launchers
	if [[ firefox = "${CN_BROWSER}" ]]; then
		sed -i 's|chromium|firefox|g' /usr/share/cnchi/scripts/postinstall/panel-launchers@cinnamon.org.json
	fi
	mkdir -p ${CN_DESTDIR}/home/${CN_USER_NAME}/.cinnamon/configs/panel-launchers@cinnamon.org/
	cp -f /usr/share/cnchi/scripts/postinstall/panel-launchers@cinnamon.org.json ${CN_DESTDIR}/home/${CN_USER_NAME}/.cinnamon/configs/panel-launchers@cinnamon.org/

	# Set Cinnamon in .dmrc
	echo "[Desktop]" > ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	echo "Session=cinnamon" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	chroot ${CN_DESTDIR} chown ${CN_USER_NAME}:users /home/${CN_USER_NAME}/.dmrc

	# Set skel directory
	cp -R ${CN_DESTDIR}/home/${CN_USER_NAME}/.config ${CN_DESTDIR}/home/${CN_USER_NAME}/.cinnamon ${CN_DESTDIR}/etc/skel

	## Set default directories
	chroot ${CN_DESTDIR} su -c xdg-user-dirs-update ${CN_USER_NAME}

	# Populate our wallpapers in Cinnamon Settings
	chroot ${CN_DESTDIR} "ln -s /usr/share/antergos/wallpapers/ /home/${CN_USER_NAME}/.cinnamon/backgrounds/antergos" ${CN_USER_NAME}
}

xfce_settings() {
	# copy antergos menu icon
	mkdir -p ${CN_DESTDIR}/usr/share/antergos/
	cp /usr/share/antergos/antergos-menu.png ${CN_DESTDIR}/usr/share/antergos/antergos-menu.png

	# Set settings
	mkdir -p ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/xfce4/xfconf/xfce-perchannel-xml
	cp -R ${CN_DESTDIR}/etc/xdg/xfce4/panel ${CN_DESTDIR}/etc/xdg/xfce4/helpers.rc ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/xfce4
	if [[ ${CN_BROWSER} = "chromium" ]]; then
		sed -i "s/WebBrowser=firefox/WebBrowser=chromium/" ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/xfce4/helpers.rc
	fi
	chroot ${CN_DESTDIR} chown -R ${CN_USER_NAME}:users /home/${CN_USER_NAME}/.config
	set_gsettings

	# Set skel directory
	cp -R ${CN_DESTDIR}/home/${CN_USER_NAME}/.config ${CN_DESTDIR}/etc/skel

	## Set default directories
	chroot ${CN_DESTDIR} su -c xdg-user-dirs-update ${CN_USER_NAME}

	# Set xfce in .dmrc
	echo "[Desktop]" > ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	echo "Session=xfce" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	chroot ${CN_DESTDIR} chown ${CN_USER_NAME}:users /home/${CN_USER_NAME}/.dmrc

	echo "QT_STYLE_OVERRIDE=gtk" >> ${CN_DESTDIR}/etc/environment

	# Add lxpolkit to autostart apps
	cp /etc/xdg/autostart/lxpolkit.desktop ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/autostart

	# xscreensaver config
	cp /usr/share/cnchi/scripts/postinstall/xscreensaver ${CN_DESTDIR}/home/${CN_USER_NAME}/.xscreensaver
	cp ${CN_DESTDIR}/home/${CN_USER_NAME}/.xscreensaver ${CN_DESTDIR}/etc/skel

	rm ${CN_DESTDIR}/etc/xdg/autostart/xscreensaver.desktop

}

openbox_settings() {
	# Copy antergos menu icon
	mkdir -p ${CN_DESTDIR}/usr/share/antergos/
	cp /usr/share/antergos/antergos-menu.png ${CN_DESTDIR}/usr/share/antergos/antergos-menu.png

	# Setup user defaults
	chroot ${CN_DESTDIR} /usr/share/antergos-openbox-setup/install.sh ${CN_USER_NAME}

	# Set skel directory
	cp -R ${CN_DESTDIR}/home/${CN_USER_NAME}/.config ${CN_DESTDIR}/etc/skel

	# Set openbox in .dmrc
	echo "[Desktop]" > ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	echo "Session=openbox" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	chroot ${CN_DESTDIR} chown ${CN_USER_NAME}:users /home/${CN_USER_NAME}/.dmrc

	# xscreensaver config
	cp /usr/share/cnchi/scripts/postinstall/xscreensaver ${CN_DESTDIR}/home/${CN_USER_NAME}/.xscreensaver
	cp ${CN_DESTDIR}/home/${CN_USER_NAME}/.xscreensaver ${CN_DESTDIR}/etc/skel
	rm ${CN_DESTDIR}/etc/xdg/autostart/xscreensaver.desktop
}

lxqt_settings() {
	# Set theme
	mkdir -p ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/razor-panel
	echo "[General]" > ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/razor.conf
	echo "__userfile__=true" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/razor.conf
	echo "icon_theme=Numix" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/razor.conf
	echo "theme=ambiance" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/razor.conf

	# Set panel launchers
	echo "[quicklaunch]" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/razor-panel/panel.conf
	echo "apps\1\desktop=/usr/share/applications/razor-config.desktop" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/razor-panel/panel.conf
	echo "apps\size=3" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/razor-panel/panel.conf
	echo "apps\2\desktop=/usr/share/applications/kde4/konsole.desktop" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/razor-panel/panel.conf
	echo "apps\3\desktop=/usr/share/applications/chromium.desktop" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/razor-panel/panel.conf

	# Set Wallpaper
	echo "[razor]" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/desktop.conf
	echo "screens\size=1" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/desktop.conf
	echo "screens\1\desktops\1\wallpaper_type=pixmap" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/desktop.conf
	echo "screens\1\desktops\1\wallpaper=/usr/share/antergos/wallpapers/antergos-wallpaper.png" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/desktop.conf
	echo "screens\1\desktops\1\keep_aspect_ratio=false" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/desktop.conf
	echo "screens\1\desktops\size=1" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/razor/desktop.conf

	# Set Razor in .dmrc
	echo "[Desktop]" > ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	echo "Session=razor" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	chroot ${CN_DESTDIR} chown ${CN_USER_NAME}:users /home/${CN_USER_NAME}/.dmrc

	chroot ${CN_DESTDIR} chown -R ${CN_USER_NAME}:users /home/${CN_USER_NAME}/.config
}

kde4_settings() {
	# Set KDE in .dmrc
	echo "[Desktop]" > ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	echo "Session=kde-plasma" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	chroot ${CN_DESTDIR} chown ${CN_USER_NAME}:users /home/${CN_USER_NAME}/.dmrc

	# Force QtCurve to use our theme
	rm -R ${CN_DESTDIR}/usr/share/apps/QtCurve/

	# Setup user defaults
	chroot ${CN_DESTDIR} /usr/share/antergos-kde-setup/install.sh ${CN_USER_NAME}

	## # Get zip file from github, unzip it and copy all setup files in their right places.
	## wget -q -O /tmp/master.tar.xz "https://github.com/Antergos/kde-setup/raw/master/kde-setup-2014-25-05.tar.xz"
	## #xz -d -qq /tmp/master.tar.xz
	## #cd ${CN_DESTDIR}
	## cd /tmp
	## tar xfJ /tmp/master.tar.xz
	## chown -R root:root /tmp/etc
	## chown -R root:root /tmp/usr
	## cp -R /tmp/etc/* ${CN_DESTDIR}/etc
	## cp -R /tmp/usr/* ${CN_DESTDIR}/usr

	# Set User & Root environments
	## cp -R ${CN_DESTDIR}/etc/skel/.config ${CN_DESTDIR}/home/${CN_USER_NAME}
	## cp -R ${CN_DESTDIR}/etc/skel/.kde4 ${CN_DESTDIR}/home/${CN_USER_NAME}
	## cp ${CN_DESTDIR}/etc/skel/.gtkrc-2.0-kde4 ${CN_DESTDIR}/home/${CN_USER_NAME}
	## chroot ${CN_DESTDIR} "ln -s /home/${CN_USER_NAME}/.gtkrc-2.0-kde4 /home/${CN_USER_NAME}/.gtkrc-2.0" ${CN_USER_NAME}
	cp -R ${CN_DESTDIR}/etc/skel/.config ${CN_DESTDIR}/root
	cp -R ${CN_DESTDIR}/etc/skel/.kde4 ${CN_DESTDIR}/root
	cp ${CN_DESTDIR}/etc/skel/.gtkrc-2.0-kde4 ${CN_DESTDIR}/root
	chroot ${CN_DESTDIR} "ln -s /root/.gtkrc-2.0-kde4 /root/.gtkrc-2.0"

	# When applications transition to Qt5 they will look for config files in the standardized (XDG) locations. Create
	# symlinks during the transitional period until all apps are updated to use the new config file paths.
	link_config() {

		if [[ ${1} != "apps:" ]] && [[ ${1} != "" ]]; then
			app=${1:6}
			app_old="/home/${CN_USER_NAME}/.kde4/share/apps/${app}"
			app_new="/home/${CN_USER_NAME}/.local/share/${app}"
			chroot ${CN_DESTDIR} "ln -s ${app_old}${app_new}" ${CN_USER_NAME}
		fi
		if [[ ${2} != "conf:" ]] && [[ ${2} != "" ]]; then
			conf=${2:6}
			conf_old="/home/${CN_USER_NAME}/.kde4/share/config/${conf}"
			conf_new="/home/${CN_USER_NAME}/.config/${conf}"
			chroot ${CN_DESTDIR} "ln -s ${conf_old}${conf_new}" ${CN_USER_NAME}
		fi

	}

	for i in konsole; do
		link_config apps:${i};
	done
	for i in kdeglobals; do
		link_config apps: conf:kdeglobals;
	done

	## Set default directories
	chroot ${CN_DESTDIR} su -c xdg-user-dirs-update ${CN_USER_NAME}
}

plasma5_settings() {
	# Set KDE in .dmrc
	echo "[Desktop]" > ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	echo "Session=plasma" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	chroot ${CN_DESTDIR} chown ${CN_USER_NAME}:users /home/${CN_USER_NAME}/.dmrc

	# Force QtCurve to use our theme
	#rm -R ${CN_DESTDIR}/usr/share/apps/QtCurve/

	# Setup user defaults
	chroot ${CN_DESTDIR} /usr/share/antergos-kde-setup/install.sh ${CN_USER_NAME}

	## # Get zip file from github, unzip it and copy all setup files in their right places.
	## wget -q -O /tmp/master.tar.xz "https://github.com/Antergos/kde-setup/raw/master/kde-setup-2014-25-05.tar.xz"
	## #xz -d -qq /tmp/master.tar.xz
	## #cd ${CN_DESTDIR}
	## cd /tmp
	## tar xfJ /tmp/master.tar.xz
	## chown -R root:root /tmp/etc
	## chown -R root:root /tmp/usr
	## cp -R /tmp/etc/* ${CN_DESTDIR}/etc
	## cp -R /tmp/usr/* ${CN_DESTDIR}/usr

	## # Set User & Root environments
	## cp -R ${CN_DESTDIR}/etc/skel/.config ${CN_DESTDIR}/home/${CN_USER_NAME}
	## cp -R ${CN_DESTDIR}/etc/skel/.kde4 ${CN_DESTDIR}/home/${CN_USER_NAME}
	## cp ${CN_DESTDIR}/etc/skel/.gtkrc-2.0-kde4 ${CN_DESTDIR}/home/${CN_USER_NAME}
	## chroot ${CN_DESTDIR} "ln -s /home/${CN_USER_NAME}/.gtkrc-2.0-kde4 /home/${CN_USER_NAME}/.gtkrc-2.0" ${CN_USER_NAME}
	cp -R ${CN_DESTDIR}/etc/skel/.config ${CN_DESTDIR}/root
	cp -R ${CN_DESTDIR}/etc/skel/.kde4 ${CN_DESTDIR}/root
	cp ${CN_DESTDIR}/etc/skel/.gtkrc-2.0-kde4 ${CN_DESTDIR}/root
	chroot ${CN_DESTDIR} "ln -s /root/.gtkrc-2.0-kde4 /root/.gtkrc-2.0"

	## Set default directories
	chroot ${CN_DESTDIR} su -c xdg-user-dirs-update ${CN_USER_NAME}
}

mate_settings() {
	# Set MATE in .dmrc
	echo "[Desktop]" > ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	echo "Session=mate-session" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	chroot ${CN_DESTDIR} chown ${CN_USER_NAME}:users /home/${CN_USER_NAME}/.dmrc

	## Set default directories
	chroot ${CN_DESTDIR} su -c xdg-user-dirs-update ${CN_USER_NAME}

	# Set gsettings input-source
	if [[ "${CN_KEYBOARD_VARIANT}" != '' ]]; then
		sed -i "s/'us'/'${CN_KEYBOARD_LAYOUT}+${CN_KEYBOARD_VARIANT}'/" /usr/share/cnchi/scripts/set-settings
	else
		sed -i "s/'us'/'${CN_KEYBOARD_LAYOUT}'/" /usr/share/cnchi/scripts/set-settings
	fi
	# Fix for Zukitwo Metacity Theme
	cp ${CN_DESTDIR}/usr/share/themes/Zukitwo/metacity-1/metacity-theme-2.xml ${CN_DESTDIR}/usr/share/themes/Zukitwo/metacity-1/metacity-theme-1.xml

	# copy antergos menu icon
	mkdir -p ${CN_DESTDIR}/usr/share/antergos/
	cp /usr/share/antergos/antergos-menu.png ${CN_DESTDIR}/usr/share/antergos/antergos-menu.png
	chroot ${CN_DESTDIR} ln -sf /usr/share/antergos/antergos-menu.png /usr/share/icons/Numix/24x24/places/start-here.png

	# Set gsettings
	set_gsettings

	# Set MintMenu Favorites
	if [[ $CN_BROWSER = "firefox" ]]; then
		sed -i 's|chromium|firefox|g' /usr/share/cnchi/scripts/postinstall/applications.list
	fi
	cp /usr/share/cnchi/scripts/postinstall/applications.list ${CN_DESTDIR}/usr/lib/linuxmint/mintMenu/applications.list

	# Copy panel layout
	cp /usr/share/cnchi/scripts/antergos.layout ${CN_DESTDIR}/usr/share/mate-panel/layouts/antergos.layout
}

nox_settings() {
	echo "Done"
}

enlightenment_settings() {
	# http://git.enlightenment.org/core/enlightenment.git/plain/data/tools/enlightenment_remote
	# copy antergos menu icon
	mkdir -p ${CN_DESTDIR}/usr/share/antergos/
	cp /usr/share/antergos/antergos-menu.png ${CN_DESTDIR}/usr/share/antergos/antergos-menu.png

	# Setup user defaults
	chroot ${CN_DESTDIR} /usr/share/antergos-enlightenment-setup/install.sh ${CN_USER_NAME}

	# Set Keyboard layout
	E_CFG="/home/${CN_USER_NAME}/.e/e/config/standard/e.cfg"
	E_SRC="/home/${CN_USER_NAME}/.e/e/config/standard/e.src"

	${CN_DESTDIR}/usr/bin/eet -d ${E_CFG} config ${E_SRC}
	sed -i 's/"us"/"${CN_KEYBOARD_LAYOUT}"/' ${E_SRC}
	if [[ "${CN_KEYBOARD_VARIANT}" != '' ]]; then
		sed -i 's/"basic"/"${CN_KEYBOARD_VARIANT}"/' ${E_SRC}
	fi
	${CN_DESTDIR}/usr/bin/eet -e ${E_CFG} config ${E_SRC} 1

	# Set settings
	set_gsettings

	# Set skel directory
	cp -R ${CN_DESTDIR}/home/${CN_USER_NAME}/.config ${CN_DESTDIR}/etc/skel

	# Set default directories
	chroot ${CN_DESTDIR} su -c xdg-user-dirs-update ${CN_USER_NAME}

	# Set enlightenment in .dmrc
	echo "[Desktop]" > ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	echo "Session=enlightenment" >> ${CN_DESTDIR}/home/${CN_USER_NAME}/.dmrc
	chroot ${CN_DESTDIR} chown ${CN_USER_NAME}:users /home/${CN_USER_NAME}/.dmrc

	echo "QT_STYLE_OVERRIDE=gtk" >> ${CN_DESTDIR}/etc/environment

	# Add lxpolkit to autostart apps
	cp /etc/xdg/autostart/lxpolkit.desktop ${CN_DESTDIR}/home/${CN_USER_NAME}/.config/autostart

	# xscreensaver config
	cp /usr/share/cnchi/scripts/postinstall/xscreensaver ${CN_DESTDIR}/home/${CN_USER_NAME}/.xscreensaver
	cp ${CN_DESTDIR}/home/${CN_USER_NAME}/.xscreensaver ${CN_DESTDIR}/etc/skel
	rm ${CN_DESTDIR}/etc/xdg/autostart/xscreensaver.desktop
}

postinstall() {

	# Specific user configurations
	if [[ -f /usr/share/applications/firefox.desktop ]]; then
		export CN_BROWSER=firefox
	else
		export CN_BROWSER=chromium
	fi

	## Workaround for LightDM bug https://bugs.launchpad.net/lightdm/+bug/1069218
	chroot "${CN_DESTDIR}" sed -i 's|UserAccounts|UserList|g' /etc/lightdm/users.conf

	## Unmute alsa channels
	chroot "${CN_DESTDIR}" amixer -c 0 set Master playback 50% unmute 2>&1

	# Fix transmission leftover
	# What is this for? I think its old code.
	if [ -f "${CN_DESTDIR}/usr/lib/tmpfiles.d/transmission.conf" ]; then
		mv "${CN_DESTDIR}/usr/lib/tmpfiles.d/transmission.conf" "${CN_DESTDIR}/usr/lib/tmpfiles.d/transmission.conf.backup"
	fi

	# Configure touchpad. Skip with base installs
	if [[ base != "${CN_DESKTOP}" ]]; then
		set_xorg
	fi

	# Configure fontconfig
	if [ -f "${FONTCONFIG_FILE}" ]; then
		FONTCONFIG_FILE="/usr/share/cnchi/scripts/fonts.conf"
		FONTCONFIG_DIR="${CN_DESTDIR}/home/${CN_USER_NAME}/.config/fontconfig"
		mkdir -p "${FONTCONFIG_DIR}"
		cp "${FONTCONFIG_FILE}" "${FONTCONFIG_DIR}"
	fi

	# Set Antergos name in filesystem files
	cp /etc/arch-release "${CN_DESTDIR}/etc"
	cp /etc/os-release "${CN_DESTDIR}/etc"
	sed -i 's|Arch|Antergos|g' "${CN_DESTDIR}/etc/issue"

	## Set desktop-specific settings
	"${CN_DESKTOP}_settings"

	# Set BROWSER var
	echo "BROWSER=/usr/bin/${CN_BROWSER}" >> "${CN_DESTDIR}/etc/environment"
	echo "BROWSER=/usr/bin/${CN_BROWSER}" >> "${CN_DESTDIR}/etc/skel/.bashrc"
	echo "BROWSER=/usr/bin/${CN_BROWSER}" >> "${CN_DESTDIR}/etc/profile"

	# Configure makepkg so that it doesn't compress packages after building.
	# Most users are building packages to install them locally so there's no need for compression.
	sed -i "s|^PKGEXT='.pkg.tar.xz'|PKGEXT='.pkg.tar'|g" "${CN_DESTDIR}/etc/makepkg.conf"

	# Set lightdm-webkit2-greeter in lightdm.conf. This should have been done here (not in the pkg) all along.
	sed -i 's|#greeter-session=example-gtk-gnome|greeter-session=lightdm-webkit2-greeter|g' "${CN_DESTDIR}/etc/lightdm/lightdm.conf"

	## Ensure user permissions are set in /home
	chroot "${CN_DESTDIR}" chown -R "${CN_USER_NAME}:users" "/home/${CN_USER_NAME}"

	# Start vbox client services if we are installed in vbox
	if [[ ${CN_IS_VBOX} ]] || [[ ${CN_IS_VBOX} = 0 ]] || [[ ${CN_IS_VBOX} = "True" ]]; then
		sed -i 's|echo "X|/usr/bin/VBoxClient-all \&\necho "X|g' "${CN_DESTDIR}/etc/lightdm/Xsession"
	fi

}

touch /tmp/.postinstall.lock
echo "Called installation script with these parameters: [$1] [$2] [$3] [$4] [$5] [$6]" > /tmp/postinstall.log
CN_USER_NAME=$1
CN_DESTDIR=$2
CN_DESKTOP=$3
CN_IS_VBOX=$4
CN_KEYBOARD_LAYOUT=$5
CN_KEYBOARD_VARIANT=$6
{ postinstall; } >> /tmp/postinstall.log 2>&1
rm /tmp/.postinstall.lock

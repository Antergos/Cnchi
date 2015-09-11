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

set_xorg()
{
    cp /usr/share/cnchi/scripts/postinstall/50-synaptics.conf ${DESTDIR}/etc/X11/xorg.conf.d/50-synaptics.conf
    cp /usr/share/cnchi/scripts/postinstall/99-killX.conf ${DESTDIR}/etc/X11/xorg.conf.d/99-killX.conf

    # Fix sensitivity for chromebooks
    if lsmod | grep -q cyapa; then
        cp /usr/share/cnchi/scripts/postinstall/50-cros-touchpad.conf ${DESTDIR}/etc/X11/xorg.conf.d/50-cros-touchpad.conf
    fi
}

gnome_settings()
{
    # Set gsettings input-source
    if [[ "${KEYBOARD_VARIANT}" != '' ]]; then
        sed -i "s/'us'/'${KEYBOARD_LAYOUT}+${KEYBOARD_VARIANT}'/" /usr/share/cnchi/scripts/set-settings
    else
        sed -i "s/'us'/'${KEYBOARD_LAYOUT}'/" /usr/share/cnchi/scripts/set-settings
    fi

    # Set gsettings
    cp /usr/share/cnchi/scripts/set-settings ${DESTDIR}/usr/bin/set-settings
    mkdir -p ${DESTDIR}/var/run/dbus
    mount --bind /var/run/dbus ${DESTDIR}/var/run/dbus
    chroot ${DESTDIR} su -c "/usr/bin/set-settings ${DESKTOP}" ${USER_NAME} >> /tmp/postinstall.log 2>&1
    umount ${DESTDIR}/var/run/dbus
    rm ${DESTDIR}/usr/bin/set-settings

    # Set gdm shell logo
    cp /usr/share/antergos/logo.png ${DESTDIR}/usr/share/antergos/
    chroot ${DESTDIR} sudo -u gdm dbus-launch gsettings set org.gnome.login-screen logo "/usr/share/antergos/logo.png" > /dev/null 2>&1

    # Set skel directory
    cp -R ${DESTDIR}/home/${USER_NAME}/.config ${DESTDIR}/etc/skel

    ## Set default directories
    chroot ${DESTDIR} su -c xdg-user-dirs-update ${USER_NAME}

    # xscreensaver config
    cp /usr/share/cnchi/scripts/postinstall/xscreensaver ${DESTDIR}/home/${USER_NAME}/.xscreensaver
    cp ${DESTDIR}/home/${USER_NAME}/.xscreensaver ${DESTDIR}/etc/skel

    if [[ -f ${DESTDIR}/etc/xdg/autostart/xscreensaver.desktop ]]; then
      rm ${DESTDIR}/etc/xdg/autostart/xscreensaver.desktop
    fi

    # Ensure that Light Locker starts before gnome-shell
    sed -i 's|echo "X|/usr/bin/light-locker \&\nsleep 3; echo "X|g' ${DESTDIR}/etc/lightdm/Xsession
}

cinnamon_settings()
{
    # Set gsettings input-source
    if [[ "${KEYBOARD_VARIANT}" != '' ]]; then
        sed -i "s/'us'/'${KEYBOARD_LAYOUT}+${KEYBOARD_VARIANT}'/" /usr/share/cnchi/scripts/set-settings
    else
        sed -i "s/'us'/'${KEYBOARD_LAYOUT}'/" /usr/share/cnchi/scripts/set-settings
    fi
    # copy antergos menu icon
    mkdir -p ${DESTDIR}/usr/share/antergos/
    cp /usr/share/antergos/antergos-menu.png ${DESTDIR}/usr/share/antergos/antergos-menu.png

    # Set gsettings
    cp /usr/share/cnchi/scripts/set-settings ${DESTDIR}/usr/bin/set-settings
    mkdir -p ${DESTDIR}/var/run/dbus
    mount -o bind /var/run/dbus ${DESTDIR}/var/run/dbus
    chroot ${DESTDIR} su -c "/usr/bin/set-settings ${DESKTOP}" ${USER_NAME} > /dev/null 2>&1
    umount ${DESTDIR}/var/run/dbus
    rm ${DESTDIR}/usr/bin/set-settings

    # Copy menu@cinnamon.org.json to set menu icon
    mkdir -p ${DESTDIR}/home/${USER_NAME}/.cinnamon/configs/menu@cinnamon.org/
    cp -f /usr/share/cnchi/scripts/postinstall/menu@cinnamon.org.json ${DESTDIR}/home/${USER_NAME}/.cinnamon/configs/menu@cinnamon.org/

    # Copy panel-launchers@cinnamon.org.json to set launchers
    if [[ $_BROWSER = "firefox" ]]; then
        sed -i 's|chromium|firefox|g' /usr/share/cnchi/scripts/postinstall/panel-launchers@cinnamon.org.json
    fi
    mkdir -p ${DESTDIR}/home/${USER_NAME}/.cinnamon/configs/panel-launchers@cinnamon.org/
    cp -f /usr/share/cnchi/scripts/postinstall/panel-launchers@cinnamon.org.json ${DESTDIR}/home/${USER_NAME}/.cinnamon/configs/panel-launchers@cinnamon.org/

    # Set Cinnamon in .dmrc
    echo "[Desktop]" > ${DESTDIR}/home/${USER_NAME}/.dmrc
    echo "Session=cinnamon" >> ${DESTDIR}/home/${USER_NAME}/.dmrc
    chroot ${DESTDIR} chown ${USER_NAME}:users /home/${USER_NAME}/.dmrc

    # Set skel directory
    cp -R ${DESTDIR}/home/${USER_NAME}/.config ${DESTDIR}/home/${USER_NAME}/.cinnamon ${DESTDIR}/etc/skel

    ## Set default directories
    chroot ${DESTDIR} su -c xdg-user-dirs-update ${USER_NAME}

    # Populate our wallpapers in Cinnamon Settings
    chroot ${DESTDIR} "ln -s /usr/share/antergos/wallpapers/ /home/${USER_NAME}/.cinnamon/backgrounds/antergos" ${USER_NAME}
}

xfce_settings()
{
    # copy antergos menu icon
    mkdir -p ${DESTDIR}/usr/share/antergos/
    cp /usr/share/antergos/antergos-menu.png ${DESTDIR}/usr/share/antergos/antergos-menu.png

    # Set settings
    mkdir -p ${DESTDIR}/home/${USER_NAME}/.config/xfce4/xfconf/xfce-perchannel-xml
    cp -R ${DESTDIR}/etc/xdg/xfce4/panel ${DESTDIR}/etc/xdg/xfce4/helpers.rc ${DESTDIR}/home/${USER_NAME}/.config/xfce4
    if [[ ${_BROWSER} = "chromium" ]]; then
        sed -i "s/WebBrowser=firefox/WebBrowser=chromium/" ${DESTDIR}/home/${USER_NAME}/.config/xfce4/helpers.rc
    fi
    chroot ${DESTDIR} chown -R ${USER_NAME}:users /home/${USER_NAME}/.config
    cp /usr/share/cnchi/scripts/set-settings ${DESTDIR}/usr/bin/set-settings
    mkdir -p ${DESTDIR}/var/run/dbus
    mount -o bind /var/run/dbus ${DESTDIR}/var/run/dbus
    chroot ${DESTDIR} su -c "/usr/bin/set-settings ${DESKTOP}" ${USER_NAME} > /dev/null 2>&1
    umount ${DESTDIR}/var/run/dbus
    rm ${DESTDIR}/usr/bin/set-settings

    # Set skel directory
    cp -R ${DESTDIR}/home/${USER_NAME}/.config ${DESTDIR}/etc/skel

    ## Set default directories
    chroot ${DESTDIR} su -c xdg-user-dirs-update ${USER_NAME}

    # Set xfce in .dmrc
    echo "[Desktop]" > ${DESTDIR}/home/${USER_NAME}/.dmrc
    echo "Session=xfce" >> ${DESTDIR}/home/${USER_NAME}/.dmrc
    chroot ${DESTDIR} chown ${USER_NAME}:users /home/${USER_NAME}/.dmrc

    echo "QT_STYLE_OVERRIDE=gtk" >> ${DESTDIR}/etc/environment

    # Add lxpolkit to autostart apps
    cp /etc/xdg/autostart/lxpolkit.desktop ${DESTDIR}/home/${USER_NAME}/.config/autostart

    # xscreensaver config
    cp /usr/share/cnchi/scripts/postinstall/xscreensaver ${DESTDIR}/home/${USER_NAME}/.xscreensaver
    cp ${DESTDIR}/home/${USER_NAME}/.xscreensaver ${DESTDIR}/etc/skel

    rm ${DESTDIR}/etc/xdg/autostart/xscreensaver.desktop

}

openbox_settings()
{
    # Copy antergos menu icon
    mkdir -p ${DESTDIR}/usr/share/antergos/
    cp /usr/share/antergos/antergos-menu.png ${DESTDIR}/usr/share/antergos/antergos-menu.png

    # Setup user defaults
    chroot ${DESTDIR} /usr/share/antergos-openbox-setup/install.sh ${USER_NAME}

    # Set skel directory
    cp -R ${DESTDIR}/home/${USER_NAME}/.config ${DESTDIR}/etc/skel

    # Set openbox in .dmrc
    echo "[Desktop]" > ${DESTDIR}/home/${USER_NAME}/.dmrc
    echo "Session=openbox" >> ${DESTDIR}/home/${USER_NAME}/.dmrc
    chroot ${DESTDIR} chown ${USER_NAME}:users /home/${USER_NAME}/.dmrc

    # xscreensaver config
    cp /usr/share/cnchi/scripts/postinstall/xscreensaver ${DESTDIR}/home/${USER_NAME}/.xscreensaver
    cp ${DESTDIR}/home/${USER_NAME}/.xscreensaver ${DESTDIR}/etc/skel
    rm ${DESTDIR}/etc/xdg/autostart/xscreensaver.desktop
}

lxqt_settings()
{
    # Set theme
    mkdir -p ${DESTDIR}/home/${USER_NAME}/.config/razor/razor-panel
    echo "[General]" > ${DESTDIR}/home/${USER_NAME}/.config/razor/razor.conf
    echo "__userfile__=true" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/razor.conf
    echo "icon_theme=Numix" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/razor.conf
    echo "theme=ambiance" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/razor.conf

    # Set panel launchers
    echo "[quicklaunch]" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/razor-panel/panel.conf
    echo "apps\1\desktop=/usr/share/applications/razor-config.desktop" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/razor-panel/panel.conf
    echo "apps\size=3" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/razor-panel/panel.conf
    echo "apps\2\desktop=/usr/share/applications/kde4/konsole.desktop" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/razor-panel/panel.conf
    echo "apps\3\desktop=/usr/share/applications/chromium.desktop" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/razor-panel/panel.conf

    # Set Wallpaper
    echo "[razor]" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/desktop.conf
    echo "screens\size=1" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/desktop.conf
    echo "screens\1\desktops\1\wallpaper_type=pixmap" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/desktop.conf
    echo "screens\1\desktops\1\wallpaper=/usr/share/antergos/wallpapers/antergos-wallpaper.png" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/desktop.conf
    echo "screens\1\desktops\1\keep_aspect_ratio=false" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/desktop.conf
    echo "screens\1\desktops\size=1" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/desktop.conf

    # Set Razor in .dmrc
    echo "[Desktop]" > ${DESTDIR}/home/${USER_NAME}/.dmrc
    echo "Session=razor" >> ${DESTDIR}/home/${USER_NAME}/.dmrc
    chroot ${DESTDIR} chown ${USER_NAME}:users /home/${USER_NAME}/.dmrc

    chroot ${DESTDIR} chown -R ${USER_NAME}:users /home/${USER_NAME}/.config
}

kde4_settings()
{
    # Set KDE in .dmrc
    echo "[Desktop]" > ${DESTDIR}/home/${USER_NAME}/.dmrc
    echo "Session=kde-plasma" >> ${DESTDIR}/home/${USER_NAME}/.dmrc
    chroot ${DESTDIR} chown ${USER_NAME}:users /home/${USER_NAME}/.dmrc

    # Force QtCurve to use our theme
    rm -R ${DESTDIR}/usr/share/apps/QtCurve/

    # Setup user defaults
    chroot ${DESTDIR} /usr/share/antergos-kde-setup/install.sh ${USER_NAME}

    ## # Get zip file from github, unzip it and copy all setup files in their right places.
    ## wget -q -O /tmp/master.tar.xz "https://github.com/Antergos/kde-setup/raw/master/kde-setup-2014-25-05.tar.xz"
    ## #xz -d -qq /tmp/master.tar.xz
    ## #cd ${DESTDIR}
    ## cd /tmp
    ## tar xfJ /tmp/master.tar.xz
    ## chown -R root:root /tmp/etc
    ## chown -R root:root /tmp/usr
    ## cp -R /tmp/etc/* ${DESTDIR}/etc
    ## cp -R /tmp/usr/* ${DESTDIR}/usr

    # Set User & Root environments
    ## cp -R ${DESTDIR}/etc/skel/.config ${DESTDIR}/home/${USER_NAME}
    ## cp -R ${DESTDIR}/etc/skel/.kde4 ${DESTDIR}/home/${USER_NAME}
    ## cp ${DESTDIR}/etc/skel/.gtkrc-2.0-kde4 ${DESTDIR}/home/${USER_NAME}
    ## chroot ${DESTDIR} "ln -s /home/${USER_NAME}/.gtkrc-2.0-kde4 /home/${USER_NAME}/.gtkrc-2.0" ${USER_NAME}
    cp -R ${DESTDIR}/etc/skel/.config ${DESTDIR}/root
    cp -R ${DESTDIR}/etc/skel/.kde4 ${DESTDIR}/root
    cp ${DESTDIR}/etc/skel/.gtkrc-2.0-kde4 ${DESTDIR}/root
    chroot ${DESTDIR} "ln -s /root/.gtkrc-2.0-kde4 /root/.gtkrc-2.0"

    # When applications transition to Qt5 they will look for config files in the standardized (XDG) locations. Create
    # symlinks during the transitional period until all apps are updated to use the new config file paths.
    link_config() {

        if [[ ${1} != "apps:" ]] && [[ ${1} != "" ]]; then
            app=${1:6}
            app_old="/home/${USER_NAME}/.kde4/share/apps/${app}"
            app_new="/home/${USER_NAME}/.local/share/${app}"
            chroot ${DESTDIR} "ln -s ${app_old}${app_new}" ${USER_NAME}
        fi
        if [[ ${2} != "conf:" ]] && [[ ${2} != "" ]]; then
            conf=${2:6}
            conf_old="/home/${USER_NAME}/.kde4/share/config/${conf}"
            conf_new="/home/${USER_NAME}/.config/${conf}"
            chroot ${DESTDIR} "ln -s ${conf_old}${conf_new}" ${USER_NAME}
        fi

    }

    for i in konsole; do
        link_config apps:${i};
    done
    for i in kdeglobals; do
        link_config apps: conf:kdeglobals;
    done

    ## Set default directories
    chroot ${DESTDIR} su -c xdg-user-dirs-update ${USER_NAME}
}

plasma5_settings()
{
    # Set KDE in .dmrc
    echo "[Desktop]" > ${DESTDIR}/home/${USER_NAME}/.dmrc
    echo "Session=plasma" >> ${DESTDIR}/home/${USER_NAME}/.dmrc
    chroot ${DESTDIR} chown ${USER_NAME}:users /home/${USER_NAME}/.dmrc

    # Force QtCurve to use our theme
    #rm -R ${DESTDIR}/usr/share/apps/QtCurve/

    # Setup user defaults
    chroot ${DESTDIR} /usr/share/antergos-kde-setup/install.sh ${USER_NAME}

    ## # Get zip file from github, unzip it and copy all setup files in their right places.
    ## wget -q -O /tmp/master.tar.xz "https://github.com/Antergos/kde-setup/raw/master/kde-setup-2014-25-05.tar.xz"
    ## #xz -d -qq /tmp/master.tar.xz
    ## #cd ${DESTDIR}
    ## cd /tmp
    ## tar xfJ /tmp/master.tar.xz
    ## chown -R root:root /tmp/etc
    ## chown -R root:root /tmp/usr
    ## cp -R /tmp/etc/* ${DESTDIR}/etc
    ## cp -R /tmp/usr/* ${DESTDIR}/usr

    ## # Set User & Root environments
    ## cp -R ${DESTDIR}/etc/skel/.config ${DESTDIR}/home/${USER_NAME}
    ## cp -R ${DESTDIR}/etc/skel/.kde4 ${DESTDIR}/home/${USER_NAME}
    ## cp ${DESTDIR}/etc/skel/.gtkrc-2.0-kde4 ${DESTDIR}/home/${USER_NAME}
    ## chroot ${DESTDIR} "ln -s /home/${USER_NAME}/.gtkrc-2.0-kde4 /home/${USER_NAME}/.gtkrc-2.0" ${USER_NAME}
    cp -R ${DESTDIR}/etc/skel/.config ${DESTDIR}/root
    cp -R ${DESTDIR}/etc/skel/.kde4 ${DESTDIR}/root
    cp ${DESTDIR}/etc/skel/.gtkrc-2.0-kde4 ${DESTDIR}/root
    chroot ${DESTDIR} "ln -s /root/.gtkrc-2.0-kde4 /root/.gtkrc-2.0"

    ## Set default directories
    chroot ${DESTDIR} su -c xdg-user-dirs-update ${USER_NAME}
}

mate_settings()
{
    # Set MATE in .dmrc
    echo "[Desktop]" > ${DESTDIR}/home/${USER_NAME}/.dmrc
    echo "Session=mate-session" >> ${DESTDIR}/home/${USER_NAME}/.dmrc
    chroot ${DESTDIR} chown ${USER_NAME}:users /home/${USER_NAME}/.dmrc

    ## Set default directories
    chroot ${DESTDIR} su -c xdg-user-dirs-update ${USER_NAME}

    # Set gsettings input-source
    if [[ "${KEYBOARD_VARIANT}" != '' ]]; then
        sed -i "s/'us'/'${KEYBOARD_LAYOUT}+${KEYBOARD_VARIANT}'/" /usr/share/cnchi/scripts/set-settings
    else
        sed -i "s/'us'/'${KEYBOARD_LAYOUT}'/" /usr/share/cnchi/scripts/set-settings
    fi
    # Fix for Zukitwo Metacity Theme
    cp ${DESTDIR}/usr/share/themes/Zukitwo/metacity-1/metacity-theme-2.xml ${DESTDIR}/usr/share/themes/Zukitwo/metacity-1/metacity-theme-1.xml

    # copy antergos menu icon
    mkdir -p ${DESTDIR}/usr/share/antergos/
    cp /usr/share/antergos/antergos-menu.png ${DESTDIR}/usr/share/antergos/antergos-menu.png
    chroot ${DESTDIR} ln -sf /usr/share/antergos/antergos-menu.png /usr/share/icons/Numix/24x24/places/start-here.png

    # Set gsettings
    cp /usr/share/cnchi/scripts/set-settings ${DESTDIR}/usr/bin/set-settings
    mkdir -p ${DESTDIR}/var/run/dbus
    mount -o bind /var/run/dbus ${DESTDIR}/var/run/dbus
    chroot ${DESTDIR} su -l -c "/usr/bin/set-settings ${DESKTOP}" ${USER_NAME} > /dev/null 2>&1
    umount ${DESTDIR}/var/run/dbus
    rm ${DESTDIR}/usr/bin/set-settings

    # Set MintMenu Favorites
    if [[ $_BROWSER = "firefox" ]]; then
        sed -i 's|chromium|firefox|g' /usr/share/cnchi/scripts/postinstall/applications.list
    fi
    cp /usr/share/cnchi/scripts/postinstall/applications.list ${DESTDIR}/usr/lib/linuxmint/mintMenu/applications.list

    # Copy panel layout
    cp /usr/share/cnchi/scripts/antergos.layout ${DESTDIR}/usr/share/mate-panel/layouts/antergos.layout
}

nox_settings()
{
    echo "Done"
}

enlightenment_settings()
{
    # http://git.enlightenment.org/core/enlightenment.git/plain/data/tools/enlightenment_remote
    # copy antergos menu icon
    mkdir -p ${DESTDIR}/usr/share/antergos/
    cp /usr/share/antergos/antergos-menu.png ${DESTDIR}/usr/share/antergos/antergos-menu.png

    # Setup user defaults
    chroot ${DESTDIR} /usr/share/antergos-enlightenment-setup/install.sh ${USER_NAME}

    # Set Keyboard layout
    E_CFG="/home/${USER_NAME}/.e/e/config/standard/e.cfg"
    E_SRC="/home/${USER_NAME}/.e/e/config/standard/e.src"

    ${DESTDIR}/usr/bin/eet -d ${E_CFG} config ${E_SRC}
    sed -i 's/"us"/"${KEYBOARD_LAYOUT}"/' ${E_SRC}
  	if [[ "${KEYBOARD_VARIANT}" != '' ]]; then
  			sed -i 's/"basic"/"${KEYBOARD_VARIANT}"/' ${E_SRC}
  	fi
    ${DESTDIR}/usr/bin/eet -e ${E_CFG} config ${E_SRC} 1

    # Set settings
    cp /usr/share/cnchi/scripts/set-settings ${DESTDIR}/usr/bin/set-settings
    mkdir -p ${DESTDIR}/var/run/dbus
    mount -o bind /var/run/dbus ${DESTDIR}/var/run/dbus
    chroot ${DESTDIR} su -c "/usr/bin/set-settings ${DESKTOP}" ${USER_NAME} > /dev/null 2>&1
    umount ${DESTDIR}/var/run/dbus
    rm ${DESTDIR}/usr/bin/set-settings

    # Set skel directory
    cp -R ${DESTDIR}/home/${USER_NAME}/.config ${DESTDIR}/etc/skel

    # Set default directories
    chroot ${DESTDIR} su -c xdg-user-dirs-update ${USER_NAME}

    # Set enlightenment in .dmrc
    echo "[Desktop]" > ${DESTDIR}/home/${USER_NAME}/.dmrc
    echo "Session=enlightenment" >> ${DESTDIR}/home/${USER_NAME}/.dmrc
    chroot ${DESTDIR} chown ${USER_NAME}:users /home/${USER_NAME}/.dmrc

    echo "QT_STYLE_OVERRIDE=gtk" >> ${DESTDIR}/etc/environment

    # Add lxpolkit to autostart apps
    cp /etc/xdg/autostart/lxpolkit.desktop ${DESTDIR}/home/${USER_NAME}/.config/autostart

    # xscreensaver config
    cp /usr/share/cnchi/scripts/postinstall/xscreensaver ${DESTDIR}/home/${USER_NAME}/.xscreensaver
    cp ${DESTDIR}/home/${USER_NAME}/.xscreensaver ${DESTDIR}/etc/skel
    rm ${DESTDIR}/etc/xdg/autostart/xscreensaver.desktop
}

postinstall()
{
    USER_NAME=$1
    DESTDIR=$2
    DESKTOP=$3
    IS_VBOX=$4
    KEYBOARD_LAYOUT=$5
    KEYBOARD_VARIANT=$6

    # Specific user configurations
    if [[ -f /usr/share/applications/firefox.desktop ]]; then
        export _BROWSER=firefox
    else
        export _BROWSER=chromium
    fi

    ## Set desktop-specific settings
    "${DESKTOP}_settings"

    ## Workaround for LightDM bug https://bugs.launchpad.net/lightdm/+bug/1069218
    chroot ${DESTDIR} sed -i 's|UserAccounts|UserList|g' /etc/lightdm/users.conf

    ## Unmute alsa channels
    chroot ${DESTDIR} amixer -c 0 set Master playback 50% unmute > /dev/null 2>&1

    # Fix transmission leftover
    if [ -f ${DESTDIR}/usr/lib/tmpfiles.d/transmission.conf ]; then
        mv ${DESTDIR}/usr/lib/tmpfiles.d/transmission.conf ${DESTDIR}/usr/lib/tmpfiles.d/transmission.conf.backup
    fi

    # Configure touchpad. Skip with base installs
    if [[ $DESKTOP != 'base' ]]; then
        set_xorg
    fi

    # Configure fontconfig
    FONTCONFIG_FILE="/usr/share/cnchi/scripts/fonts.conf"
    FONTCONFIG_DIR="${DESTDIR}/home/${USER_NAME}/.config/fontconfig"
    if [ -f ${FONTCONFIG_FILE} ]; then
        mkdir -p ${FONTCONFIG_DIR}
        cp ${FONTCONFIG_FILE} ${FONTCONFIG_DIR}
    fi

    # Set Antergos name in filesystem files
    cp /etc/arch-release ${DESTDIR}/etc
    cp /etc/os-release ${DESTDIR}/etc
    #cp /etc/lsb-release ${DESTDIR}/etc
    sed -i 's|Arch|Antergos|g' ${DESTDIR}/etc/issue

    # Set BROWSER var
    echo "BROWSER=/usr/bin/${_BROWSER}" >> ${DESTDIR}/etc/environment
    echo "BROWSER=/usr/bin/${_BROWSER}" >> ${DESTDIR}/etc/skel/.bashrc
    echo "BROWSER=/usr/bin/${_BROWSER}" >> ${DESTDIR}/etc/profile

    # Configure makepkg so that it doesn't compress packages after building.
    # Most users are building packages to install them locally so there's no need for compression.
    sed -i "s|^PKGEXT='.pkg.tar.xz'|PKGEXT='.pkg.tar'|g" /etc/makepkg.conf

    # Set lightdm-webkit2-greeter in lightdm.conf. This should have been done here (not in the pkg) all along.
    sed -i 's|#greeter-session=example-gtk-gnome|greeter-session=lightdm-webkit2-greeter|g' ${DESTDIR}/etc/lightdm/lightdm.conf

    ## Ensure user permissions are set in /home
    chroot ${DESTDIR} chown -R ${USER_NAME}:users /home/${USER_NAME}

    # Start vbox client services if we are installed in vbox
    if [[ $IS_VBOX ]] || [[ $IS_VBOX = 0 ]] || [[ $IS_VBOX = "True" ]]; then
        sed -i 's|echo "X|/usr/bin/VBoxClient-all \&\necho "X|g' ${DESTDIR}/etc/lightdm/Xsession
    fi

}

touch /tmp/.postinstall.lock
echo "Called installation script with these parameters: [$1] [$2] [$3] [$4] [$5] [$6]" > /tmp/postinstall.log 2>&1
postinstall $1 $2 $3 $4 $5 $6 >> /tmp/postinstall.log 2>&1
rm /tmp/.postinstall.lock

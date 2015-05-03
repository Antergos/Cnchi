#!/usr/bin/bash

# -*- coding: utf-8 -*-
#
#  postinstall.sh
#
#  Copyright © 2013,2014 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

set_xorg()
{
    cp /usr/share/cnchi/scripts/postinstall/50-synaptics.conf ${DESTDIR}/etc/X11/xorg.conf.d/50-synaptics.conf
    cp /usr/share/cnchi/scripts/postinstall/99-killX.conf ${DESTDIR}/etc/X11/xorg.conf.d/99-killX.conf
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
    mount -o bind /var/run/dbus ${DESTDIR}/var/run/dbus
    chroot ${DESTDIR} su -c "/usr/bin/set-settings ${DESKTOP}" ${USER_NAME} > /dev/null 2>&1

    # Set gdm shell logo
    cp /usr/share/antergos/logo.png ${DESTDIR}/usr/share/antergos/
    chroot ${DESTDIR} sudo -u gdm dbus-launch gsettings set org.gnome.login-screen logo "/usr/share/antergos/logo.png" > /dev/null 2>&1

    rm ${DESTDIR}/usr/bin/set-settings

    # Set skel directory
    cp -R ${DESTDIR}/home/${USER_NAME}/.config ${DESTDIR}/etc/skel

    ## Set defaults directories
    chroot ${DESTDIR} su -c xdg-user-dirs-update ${USER_NAME}

    # xscreensaver config
    cp /usr/share/cnchi/scripts/postinstall/xscreensaver ${DESTDIR}/home/${USER_NAME}/.xscreensaver
    cp ${DESTDIR}/home/${USER_NAME}/.xscreensaver ${DESTDIR}/etc/skel

    rm ${DESTDIR}/etc/xdg/autostart/xscreensaver.desktop

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
    rm ${DESTDIR}/usr/bin/set-settings

    # Copy menu@cinnamon.org.json to set menu icon
    mkdir -p ${DESTDIR}/home/${USER_NAME}/.cinnamon/configs/menu@cinnamon.org/
    cp -f /usr/share/cnchi/scripts/menu@cinnamon.org.json ${DESTDIR}/home/${USER_NAME}/.cinnamon/configs/menu@cinnamon.org/

    # Copy panel-launchers@cinnamon.org.json to set launchers
    if [[ $_BROWSER = "firefox" ]]; then
        sed -i 's|chromium|firefox|g' /usr/share/cnchi/scripts/panel-launchers@cinnamon.org.json
    fi
    mkdir -p ${DESTDIR}/home/${USER_NAME}/.cinnamon/configs/panel-launchers@cinnamon.org/
    cp -f /usr/share/cnchi/scripts/panel-launchers@cinnamon.org.json ${DESTDIR}/home/${USER_NAME}/.cinnamon/configs/panel-launchers@cinnamon.org/

    # Set Cinnamon in .dmrc
    echo "[Desktop]" > ${DESTDIR}/home/${USER_NAME}/.dmrc
    echo "Session=cinnamon" >> ${DESTDIR}/home/${USER_NAME}/.dmrc
    chroot ${DESTDIR} chown ${USER_NAME}:users /home/${USER_NAME}/.dmrc


    # Set skel directory
    cp -R ${DESTDIR}/home/${USER_NAME}/.config ${DESTDIR}/home/${USER_NAME}/.cinnamon ${DESTDIR}/etc/skel

    ## Set defaults directories
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
    rm ${DESTDIR}/usr/bin/set-settings

    # Set skel directory
    cp -R ${DESTDIR}/home/${USER_NAME}/.config ${DESTDIR}/etc/skel

    ## Set defaults directories
    chroot ${DESTDIR} su -c xdg-user-dirs-update ${USER_NAME}

    # Set xfce in .dmrc
    echo "[Desktop]" > ${DESTDIR}/home/${USER_NAME}/.dmrc
    echo "Session=xfce" >> ${DESTDIR}/home/${USER_NAME}/.dmrc
    chroot ${DESTDIR} chown ${USER_NAME}:users /home/${USER_NAME}/.dmrc

    echo "QT_STYLE_OVERRIDE=gtk" >> ${DESTDIR}/etc/environment

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

    # Get zip file from github, unzip it and copy all setup files in their right places.
    wget -q -O /tmp/master.zip "https://github.com/Antergos/openbox-setup/archive/master.zip"
    unzip -o -qq /tmp/master.zip -d /tmp

    ## Copy slim theme
    #mkdir -p ${DESTDIR}/usr/share/slim/themes/antergos-slim
    #cp ${DESTDIR}/tmp/openbox-setup-master/antergos-slim/* ${DESTDIR}/usr/share/slim/themes/antergos-slim

    # Copy home files
    cp /tmp/openbox-setup-master/gtkrc-2.0 ${DESTDIR}/home/${USER_NAME}/.gtkrc-2.0
    chroot ${DESTDIR} chown -R ${USER_NAME}:users /home/${USER_NAME}/.gtkrc-2.0
    cp /tmp/openbox-setup-master/xinitrc ${DESTDIR}/home/${USER_NAME}/.xinitrc
    chroot ${DESTDIR} chown -R ${USER_NAME}:users /home/${USER_NAME}/.xinitrc

    # Copy .config files
    mkdir -p ${DESTDIR}/home/${USER_NAME}/.config
    cp -R /tmp/openbox-setup-master/config/* ${DESTDIR}/home/${USER_NAME}/.config

    # Copy /etc setup files
    cp -R /tmp/openbox-setup-master/etc/* ${DESTDIR}/etc
    chroot ${DESTDIR} chown -R ${USER_NAME}:users /home/${USER_NAME}/.config

    # Copy oblogout icons
    mkdir -p ${DESTDIR}/usr/share/themes/Numix/oblogout
    cp -R /tmp/openbox-setup-master/oblogout/* ${DESTDIR}/usr/share/themes/Numix/oblogout

    # Set settings
    cp /usr/share/cnchi/scripts/set-settings ${DESTDIR}/usr/bin/set-settings
    mkdir -p ${DESTDIR}/var/run/dbus
    mount -o bind /var/run/dbus ${DESTDIR}/var/run/dbus
    chroot ${DESTDIR} su -c "/usr/bin/set-settings ${DESKTOP}" ${USER_NAME} > /dev/null 2>&1
    rm ${DESTDIR}/usr/bin/set-settings

    # Set skel directory
    cp -R ${DESTDIR}/home/${USER_NAME}/.config ${DESTDIR}/etc/skel

    ## Set defaults directories
    #chroot ${DESTDIR} su -c xdg-user-dirs-update ${USER_NAME}

    # Set openbox in .dmrc
    echo "[Desktop]" > ${DESTDIR}/home/${USER_NAME}/.dmrc
    echo "Session=openbox" >> ${DESTDIR}/home/${USER_NAME}/.dmrc
    chroot ${DESTDIR} chown ${USER_NAME}:users /home/${USER_NAME}/.dmrc

    # xscreensaver config
    cp /usr/share/cnchi/scripts/postinstall/xscreensaver ${DESTDIR}/home/${USER_NAME}/.xscreensaver
    cp ${DESTDIR}/home/${USER_NAME}/.xscreensaver ${DESTDIR}/etc/skel
    rm ${DESTDIR}/etc/xdg/autostart/xscreensaver.desktop
}

lxde_settings()
{
    # FIXME: This is just a copy of openbox settings.
    # TODO: Adapt this to LXDE

    # Copy antergos menu icon
    mkdir -p ${DESTDIR}/usr/share/antergos/
    cp /usr/share/antergos/antergos-menu.png ${DESTDIR}/usr/share/antergos/antergos-menu.png

    # Get zip file from github, unzip it and copy all setup files in their right places.
    wget -q -O /tmp/master.zip "https://github.com/Antergos/openbox-setup/archive/master.zip"
    unzip -o -qq /tmp/master.zip -d /tmp

    ## Copy slim theme
    #mkdir -p ${DESTDIR}/usr/share/slim/themes/antergos-slim
    #cp ${DESTDIR}/tmp/openbox-setup-master/antergos-slim/* ${DESTDIR}/usr/share/slim/themes/antergos-slim

    # Copy home files
    cp /tmp/openbox-setup-master/gtkrc-2.0 ${DESTDIR}/home/${USER_NAME}/.gtkrc-2.0
    chroot ${DESTDIR} chown -R ${USER_NAME}:users /home/${USER_NAME}/.gtkrc-2.0
    cp /tmp/openbox-setup-master/xinitrc ${DESTDIR}/home/${USER_NAME}/.xinitrc
    chroot ${DESTDIR} chown -R ${USER_NAME}:users /home/${USER_NAME}/.xinitrc

    # Copy .config files
    mkdir -p ${DESTDIR}/home/${USER_NAME}/.config
    cp -R /tmp/openbox-setup-master/config/* ${DESTDIR}/home/${USER_NAME}/.config

    # Copy /etc setup files
    cp -R /tmp/openbox-setup-master/etc/* ${DESTDIR}/etc
    chroot ${DESTDIR} chown -R ${USER_NAME}:users /home/${USER_NAME}/.config

    # Copy oblogout icons
    mkdir -p ${DESTDIR}/usr/share/themes/Numix/oblogout
    cp -R /tmp/openbox-setup-master/oblogout/* ${DESTDIR}/usr/share/themes/Numix/oblogout

    # Set settings
    cp /usr/share/cnchi/scripts/set-settings ${DESTDIR}/usr/bin/set-settings
    mkdir -p ${DESTDIR}/var/run/dbus
    mount -o bind /var/run/dbus ${DESTDIR}/var/run/dbus
    chroot ${DESTDIR} su -c "/usr/bin/set-settings ${DESKTOP}" ${USER_NAME} > /dev/null 2>&1
    rm ${DESTDIR}/usr/bin/set-settings

    # Set skel directory
    cp -R ${DESTDIR}/home/${USER_NAME}/.config ${DESTDIR}/etc/skel

    ## Set defaults directories
    #chroot ${DESTDIR} su -c xdg-user-dirs-update ${USER_NAME}

    # Set openbox in .dmrc
    echo "[Desktop]" > ${DESTDIR}/home/${USER_NAME}/.dmrc
    echo "Session=openbox" >> ${DESTDIR}/home/${USER_NAME}/.dmrc
    chroot ${DESTDIR} chown ${USER_NAME}:users /home/${USER_NAME}/.dmrc
}

lxqt_settings()
{
    # Set theme
    mkdir -p ${DESTDIR}/home/${USER_NAME}/.config/razor/razor-panel
    echo "[General]" > ${DESTDIR}/home/${USER_NAME}/.config/razor/razor.conf
    echo "__userfile__=true" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/razor.conf
    echo "icon_theme=Faenza" >> ${DESTDIR}/home/${USER_NAME}/.config/razor/razor.conf
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

kde_settings()
{
    # Set KDE in .dmrc
    echo "[Desktop]" > ${DESTDIR}/home/${USER_NAME}/.dmrc
    echo "Session=kde-plasma" >> ${DESTDIR}/home/${USER_NAME}/.dmrc
    chroot ${DESTDIR} chown ${USER_NAME}:users /home/${USER_NAME}/.dmrc

    # Force QtCurve to use our theme
    rm -R ${DESTDIR}/usr/share/apps/QtCurve/

    # Get zip file from github, unzip it and copy all setup files in their right places.
    wget -q -O /tmp/master.tar.xz "https://github.com/Antergos/kde-setup/raw/master/kde-setup-2014-25-05.tar.xz"
    #xz -d -qq /tmp/master.tar.xz
    #cd ${DESTDIR}
    cd /tmp
    tar xfJ /tmp/master.tar.xz
    chown -R root:root /tmp/etc
    chown -R root:root /tmp/usr
    cp -R /tmp/etc/* ${DESTDIR}/etc
    cp -R /tmp/usr/* ${DESTDIR}/usr

    # Set User & Root environments
    cp -R ${DESTDIR}/etc/skel/.config ${DESTDIR}/home/${USER_NAME}
    cp -R ${DESTDIR}/etc/skel/.kde4 ${DESTDIR}/home/${USER_NAME}
    cp ${DESTDIR}/etc/skel/.gtkrc-2.0-kde4 ${DESTDIR}/home/${USER_NAME}
    cp -R ${DESTDIR}/etc/skel/.config ${DESTDIR}/root
    cp -R ${DESTDIR}/etc/skel/.kde4 ${DESTDIR}/root
    cp ${DESTDIR}/etc/skel/.gtkrc-2.0-kde4 ${DESTDIR}/root
    chroot ${DESTDIR} "ln -s /home/${USER_NAME}/.gtkrc-2.0-kde4 /home/${USER_NAME}/.gtkrc-2.0" ${USER_NAME}
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

    ## Set defaults directories
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

    # Get zip file from github, unzip it and copy all setup files in their right places.
    wget -q -O /tmp/master.tar.xz "https://github.com/Antergos/kde-setup/raw/master/kde-setup-2014-25-05.tar.xz"
    #xz -d -qq /tmp/master.tar.xz
    #cd ${DESTDIR}
    cd /tmp
    tar xfJ /tmp/master.tar.xz
    chown -R root:root /tmp/etc
    chown -R root:root /tmp/usr
    cp -R /tmp/etc/* ${DESTDIR}/etc
    cp -R /tmp/usr/* ${DESTDIR}/usr

    # Set User & Root environments
    cp -R ${DESTDIR}/etc/skel/.config ${DESTDIR}/home/${USER_NAME}
    cp -R ${DESTDIR}/etc/skel/.kde4 ${DESTDIR}/home/${USER_NAME}
    cp ${DESTDIR}/etc/skel/.gtkrc-2.0-kde4 ${DESTDIR}/home/${USER_NAME}
    cp -R ${DESTDIR}/etc/skel/.config ${DESTDIR}/root
    cp -R ${DESTDIR}/etc/skel/.kde4 ${DESTDIR}/root
    cp ${DESTDIR}/etc/skel/.gtkrc-2.0-kde4 ${DESTDIR}/root
    chroot ${DESTDIR} "ln -s /home/${USER_NAME}/.gtkrc-2.0-kde4 /home/${USER_NAME}/.gtkrc-2.0" ${USER_NAME}
    chroot ${DESTDIR} "ln -s /root/.gtkrc-2.0-kde4 /root/.gtkrc-2.0"

    ## Set defaults directories
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
    echo "TODO"
}

postinstall()
{
    USER_NAME=$1
    DESTDIR=$2
    DESKTOP=$3
    KEYBOARD_LAYOUT=$4
    KEYBOARD_VARIANT=$5
    # Specific user configurations
    if [[ -f /usr/share/applications/firefox.desktop ]]; then
        export _BROWSER=firefox
    else
        export _BROWSER=chromium
    fi

    ## Set desktop-specific settings
    "${DESKTOP}_settings"

    ## Ensure user permissions are set in /home
    chroot ${DESTDIR} chown -R ${USER_NAME}:users /home/${USER_NAME}

    ## Workaround for LightDM bug https://bugs.launchpad.net/lightdm/+bug/1069218
    chroot ${DESTDIR} sed -i 's|UserAccounts|UserList|g' /etc/lightdm/users.conf

    ## Unmute alsa channels
    chroot ${DESTDIR} amixer -c 0 set Master playback 50% unmute > /dev/null 2>&1

    # Fix transmission leftover
    if [ -f ${DESTDIR}/usr/lib/tmpfiles.d/transmission.conf ]; then
        mv ${DESTDIR}/usr/lib/tmpfiles.d/transmission.conf ${DESTDIR}/usr/lib/tmpfiles.d/transmission.conf.backup
    fi

    # Configure touchpad. Skip with base installs
    if [[ $DESKTOP != 'nox' ]]; then
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
}

touch /tmp/.postinstall.lock
postinstall $1 $2 $3 $4 $5 $6 > /tmp/postinstall.log 2>&1
rm /tmp/.postinstall.lock

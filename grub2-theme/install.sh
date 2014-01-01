grub2-theme-install(){
    DESTDIR=$1

    THEME_NAME='Antergos-Default'

    # Filename of theme definition file.
    THEME_DEF_FILE='theme.txt'

    # Filename of the image to use for the terminal background.
    BG_IMG='background.png'

    # The resolution the theme was designed to show best at, 640x480, 1024x768 etc,
    # or "any" for any resolution (resolution independent).
    THEME_RES='1600x1200x24,any'

    # Directory containing theme files to install.
    SELF=$(dirname $0)

    DEFAULT_PREFIX="${DESTDIR}/boot/grub"


    # Write variables to <grub_sysconfdir/default/grub.
    SET_GRUB_VAR () {
	    i=$(sed -n "s,^#\?\s\?$1,&,p" "${GRUB_CONF}")
	    if [[ -z "$i" ]] ; then
		    echo -e "\n$1$2" >> "${GRUB_CONF}"
	    else
		    sed -i.bak "s,^#\?\s\?$1.*,$3$1$2," "${GRUB_CONF}"
	    fi
    }

    if [ ! -d "${DEFAULT_PREFIX}" ]; then
    GRUB_PREFIX="${DESTDIR}/boot/efi/grub";
    else GRUB_PREFIX="${DEFAULT_PREFIX}"
    fi

    GRUB_CFG="${GRUB_PREFIX}/grub.cfg"

    GRUB_CONF="${DESTDIR}/etc/default/grub"

    # Create the theme's directory.
    THEME_DIR="${GRUB_PREFIX}/themes/${THEME_NAME}"
    if [[ -d "${THEME_DIR}" ]] ; then
    rm -r "${THEME_DIR}"
    fi

    mkdir -p "${THEME_DIR}"
    echo -e "Installing theme to: ${THEME_DIR}."

    # Copy the theme's files to the theme's directory.
    for i in ${self}/* ; do
	cp -r "${i}" "${THEME_DIR}/$(basename "${i}")"
    done


	# Set GRUB's resolution to match that of the theme.

	SET_GRUB_VAR 'GRUB_GFXMODE=' "${THEME_RES}"

    # Set the theme.
	SET_GRUB_VAR 'GRUB_THEME=' $(echo "${THEME_DIR}/${THEME_DEF_FILE}")

	# Generate new grub.cfg
	$(grub-mkconfig -o "${GRUB_CFG}")
	
}

touch /tmp/.grub2-theme-install.lock
grub2-theme-install $1
rm /tmp/.grub2-theme-install.lock

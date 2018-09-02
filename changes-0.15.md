# Cnchi 0.15.x (development)

## Changes

- Big code cleanup (PEP8, remove duplicated code, reduce complexity, remove unused code...)
- Rankmirrors modifications.
- Fix https://github.com/Antergos/Cnchi/issues/907
- Fixed download_requests (now uses the same mirror)
- Added cache page
- Set LTS Kernel as default in GRUB (if selected)
- Sphinx documentation in docs folder
- Check sha256 sum of packages by default if possible. Use md5 if not.
- Show logs in color when logging to stdout.
- Store logs in /var/log/cnchi instead of /tmp
- Removed self update code (we use pacman to update cnchi)
- Split advanced.py in several files (and classes).
- Added GeoIP database checking in timezone module.
- Added an "energy" feature.
- Rearranged pages (user's page before summary page).
- User is created along with its group (it does not use users group).
- Update metalink creation and error checking (metalink.py)
- Use defusedxml
- Updated Readme.md
- Split ZFS code in two modules for better readability (zfs, zfs_manager)
- Changed ZFS disk structure
- Use sha256 sum when checking downloaded files (instead of md5)
- Merged lembrame code
- Install yay as AUR helper
- Move LUKS code from auto_partition to its own module (luks)
- Move mount functions from auto_partition to its own module (mount)
- Split mkinitcpio code into several functions
- New class Events to manage... events. Removed queue_events function from several modules.
- Do not use meta packages in packages.xml
- Added i3 and Budgie to available desktops
- Use /var/tmp instead of /tmp
- self.ui got renamed to self.gui
- Be able to boot when /usr is in a separate partition
- Removed apply button in avatar choosing dialog (just double click on the wanted image)
- Once the packages list is created, check that there is no removed/renamed package in that list that will break the installation
- Set MIN_SIZE for the installation to 16GB (instead of 8GB)
- Fix user_info when going back and forth
- Set valign to center in some screens (maybe we can set it to top and make cnchi window smaller...)
- Get Cnchi latest stable version from antergos repository database (antergos.db)

## Not ready
- Encrypt home folder using gocryptfs (untested, not enabled).
- Webcam in user page (untested, not enabled).

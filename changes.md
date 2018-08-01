# Cnchi 0.16.x

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

## Not ready
- Encrypt home folder using gocryptfs (untested, not enabled).
- Webcam in user page (untested, not enabled).

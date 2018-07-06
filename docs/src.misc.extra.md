<h1 id="src.misc.extra">src.misc.extra</h1>

Extra functions
<h2 id="src.misc.extra.copytree">copytree</h2>

```python
copytree(src_dir, dst_dir, symlinks=False, ignore=None)
```
Copy an entire tree with files and folders
<h2 id="src.misc.extra.utf8">utf8</h2>

```python
utf8(my_string, errors='strict')
```
Decode a string as UTF-8 if it isn't already Unicode.
<h2 id="src.misc.extra.is_swap">is_swap</h2>

```python
is_swap(device)
```
Check if device is a swap device
<h2 id="src.misc.extra.set_groups_for_uid">set_groups_for_uid</h2>

```python
set_groups_for_uid(uid)
```
Set groups for user id uid
<h2 id="src.misc.extra.get_uid_gid">get_uid_gid</h2>

```python
get_uid_gid()
```
Returns uid and gid from SUDO_* env vars
and sets groups for that uid
<h2 id="src.misc.extra.drop_all_privileges">drop_all_privileges</h2>

```python
drop_all_privileges()
```
Drop root privileges
<h2 id="src.misc.extra.drop_privileges">drop_privileges</h2>

```python
drop_privileges()
```
Drop privileges
<h2 id="src.misc.extra.regain_privileges">regain_privileges</h2>

```python
regain_privileges()
```
Regain root privileges
<h2 id="src.misc.extra.drop_privileges_save">drop_privileges_save</h2>

```python
drop_privileges_save()
```
Drop the real UID/GID as well, and hide them in saved IDs.
<h2 id="src.misc.extra.regain_privileges_save">regain_privileges_save</h2>

```python
regain_privileges_save()
```
Recover our real UID/GID after calling drop_privileges_save.
<h2 id="src.misc.extra.raised_privileges">raised_privileges</h2>

```python
raised_privileges()
```
As regain_privileges/drop_privileges, but in context manager style.
<h2 id="src.misc.extra.raise_privileges">raise_privileges</h2>

```python
raise_privileges(func)
```
As raised_privileges, but as a function decorator.
<h2 id="src.misc.extra.is_removable">is_removable</h2>

```python
is_removable(device)
```
Checks if device is removable
<h2 id="src.misc.extra.mount_info">mount_info</h2>

```python
mount_info(path)
```
Return filesystem name, type, and ro/rw for a given mountpoint.
<h2 id="src.misc.extra.udevadm_info">udevadm_info</h2>

```python
udevadm_info(args)
```
Helper function to run udevadm
<h2 id="src.misc.extra.partition_to_disk">partition_to_disk</h2>

```python
partition_to_disk(partition)
```
Convert a partition device to its disk device, if any.
<h2 id="src.misc.extra.cdrom_mount_info">cdrom_mount_info</h2>

```python
cdrom_mount_info()
```
Return mount information for /cdrom.
This is the same as mount_info, except that the partition is converted to
its containing disk, and we don't care whether the mount point is
writable.
<h2 id="src.misc.extra.format_size">format_size</h2>

```python
format_size(size)
```
Format a partition size.
<h2 id="src.misc.extra.create_bool">create_bool</h2>

```python
create_bool(text)
```
Creates a bool from a str type
<h2 id="src.misc.extra.dmimodel">dmimodel</h2>

```python
dmimodel()
```
Use dmidecode to get hardware info
dmidecode is a tool for dumping a computer's DMI (some say SMBIOS) table
contents in a human-readable format. This table contains a description of
the system's hardware components, as well as other useful pieces of
information such as serial numbers and BIOS revision
<h2 id="src.misc.extra.get_prop">get_prop</h2>

```python
get_prop(obj, iface, prop)
```
Get network interface property
<h2 id="src.misc.extra.is_wireless_enabled">is_wireless_enabled</h2>

```python
is_wireless_enabled()
```
Networkmanager. Checks if wireless is enabled
<h2 id="src.misc.extra.get_nm_state">get_nm_state</h2>

```python
get_nm_state()
```
Checks Networkmanager connection status
<h2 id="src.misc.extra.has_connection">has_connection</h2>

```python
has_connection()
```
Checks if we have an Internet connection
<h2 id="src.misc.extra.add_connection_watch">add_connection_watch</h2>

```python
add_connection_watch(func)
```
Add connection watch to Networkmanager
<h2 id="src.misc.extra.get_network">get_network</h2>

```python
get_network()
```
Get our own network ip
<h2 id="src.misc.extra.sort_list">sort_list</h2>

```python
sort_list(my_list, my_locale='')
```
Sorts list using locale specifics
<h2 id="src.misc.extra.gtk_refresh">gtk_refresh</h2>

```python
gtk_refresh()
```
Tell Gtk loop to run pending events
<h2 id="src.misc.extra.remove_temp_files">remove_temp_files</h2>

```python
remove_temp_files()
```
Remove Cnchi temporary files
<h2 id="src.misc.extra.set_cursor">set_cursor</h2>

```python
set_cursor(cursor_type)
```
Set mouse cursor
<h2 id="src.misc.extra.partition_exists">partition_exists</h2>

```python
partition_exists(partition)
```
Check if a partition already exists
<h2 id="src.misc.extra.is_partition_extended">is_partition_extended</h2>

```python
is_partition_extended(partition)
```
Check if a partition is of extended type
<h2 id="src.misc.extra.get_partitions">get_partitions</h2>

```python
get_partitions()
```
Get all system partitions
<h2 id="src.misc.extra.check_pid">check_pid</h2>

```python
check_pid(pid)
```
Check For the existence of a unix pid.
<h2 id="src.misc.extra.random_generator">random_generator</h2>

```python
random_generator(size=4, chars='abcdefghijklmnopqrstuvwxyz0123456789')
```
Generates a random string.
<h2 id="src.misc.extra.select_combobox_value">select_combobox_value</h2>

```python
select_combobox_value(combobox, value)
```
Force combobox to select a specific value
<h2 id="src.misc.extra.select_first_combobox_item">select_first_combobox_item</h2>

```python
select_first_combobox_item(combobox)
```
Automatically select the first entry
<h2 id="src.misc.extra.InstallError">InstallError</h2>

```python
InstallError(self, message)
```
Exception class called upon an installer error

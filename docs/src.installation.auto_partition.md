<h1 id="src.installation.auto_partition">src.installation.auto_partition</h1>

AutoPartition module, used by automatic installation
<h2 id="src.installation.auto_partition.printk">printk</h2>

```python
printk(enable)
```
Enables / disables printing kernel messages to console
<h2 id="src.installation.auto_partition.unmount">unmount</h2>

```python
unmount(directory)
```
Unmount
<h2 id="src.installation.auto_partition.unmount_all_in_directory">unmount_all_in_directory</h2>

```python
unmount_all_in_directory(dest_dir)
```
Unmounts all devices that are mounted inside dest_dir
<h2 id="src.installation.auto_partition.unmount_all_in_device">unmount_all_in_device</h2>

```python
unmount_all_in_device(device)
```
Unmounts all partitions from device
<h2 id="src.installation.auto_partition.remove_lvm">remove_lvm</h2>

```python
remove_lvm(device)
```
Remove all previous LVM volumes
(it may have been left created due to a previous failed installation)
<h2 id="src.installation.auto_partition.close_antergos_luks_devices">close_antergos_luks_devices</h2>

```python
close_antergos_luks_devices()
```
Close LUKS devices (they may have been left open because of a previous
failed installation)
<h2 id="src.installation.auto_partition.setup_luks">setup_luks</h2>

```python
setup_luks(luks_device, luks_name, luks_pass=None, luks_key=None)
```
Setups a luks device
<h2 id="src.installation.auto_partition.AutoPartition">AutoPartition</h2>

```python
AutoPartition(self, dest_dir, auto_device, use_luks, luks_password, use_lvm, use_home, bootloader, callback_queue)
```
Class used by the automatic installation method

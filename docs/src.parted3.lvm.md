<h1 id="src.parted3.lvm">src.parted3.lvm</h1>

Manage lvm volumes
<h2 id="src.parted3.lvm.get_lvm_partitions">get_lvm_partitions</h2>

```python
get_lvm_partitions()
```
Get all partition volumes
<h2 id="src.parted3.lvm.get_volume_groups">get_volume_groups</h2>

```python
get_volume_groups()
```
Get all volume groups
<h2 id="src.parted3.lvm.get_logical_volumes">get_logical_volumes</h2>

```python
get_logical_volumes(volume_group)
```
Get all logical volumes from a volume group
<h2 id="src.parted3.lvm.remove_logical_volume">remove_logical_volume</h2>

```python
remove_logical_volume(logical_volume)
```
Removes a logical volume
<h2 id="src.parted3.lvm.remove_volume_group">remove_volume_group</h2>

```python
remove_volume_group(volume_group)
```
Removes an entire volume group
<h2 id="src.parted3.lvm.remove_physical_volume">remove_physical_volume</h2>

```python
remove_physical_volume(physical_volume)
```
Removes a physical volume

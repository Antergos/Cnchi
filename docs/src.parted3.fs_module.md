<h1 id="src.parted3.fs_module">src.parted3.fs_module</h1>

Functions to work with file systems
<h2 id="src.parted3.fs_module.get_uuid">get_uuid</h2>

```python
get_uuid(part)
```
Get partition UUID
<h2 id="src.parted3.fs_module.get_label">get_label</h2>

```python
get_label(part)
```
Get partition label
<h2 id="src.parted3.fs_module.get_info">get_info</h2>

```python
get_info(part)
```
Get partition info using blkid
<h2 id="src.parted3.fs_module.get_type">get_type</h2>

```python
get_type(part)
```
Get partition filesystem type
<h2 id="src.parted3.fs_module.get_pknames">get_pknames</h2>

```python
get_pknames()
```
PKNAME: internal parent kernel device name
<h2 id="src.parted3.fs_module.label_fs">label_fs</h2>

```python
label_fs(fstype, part, label)
```
Get filesystem label
<h2 id="src.parted3.fs_module.create_fs">create_fs</h2>

```python
create_fs(part, fstype, label='', other_opts='')
```
Create filesystem using mkfs
<h2 id="src.parted3.fs_module.is_ssd">is_ssd</h2>

```python
is_ssd(disk_path)
```
Checks if given disk is actually a ssd disk.
<h2 id="src.parted3.fs_module.resize">resize</h2>

```python
resize(part, fs_type, new_size_in_mb)
```
Resize partition
<h2 id="src.parted3.fs_module.resize_ntfs">resize_ntfs</h2>

```python
resize_ntfs(part, new_size_in_mb)
```
Resize a ntfs partition
<h2 id="src.parted3.fs_module.resize_fat">resize_fat</h2>

```python
resize_fat(_part, _new_size_in_mb)
```
Resize a fat partition
<h2 id="src.parted3.fs_module.resize_ext">resize_ext</h2>

```python
resize_ext(part, new_size_in_mb)
```
Resize an ext partition

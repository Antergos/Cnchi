<h1 id="src.parted3.partition_module">src.parted3.partition_module</h1>

Interacts with pyparted
<h2 id="src.parted3.partition_module.get_devices">get_devices</h2>

```python
get_devices()
```
Get all devices
<h2 id="src.parted3.partition_module.make_new_disk">make_new_disk</h2>

```python
make_new_disk(dev_path, new_type)
```
Make a new disk
<h2 id="src.parted3.partition_module.get_partitions">get_partitions</h2>

```python
get_partitions(diskob)
```
Get partitions from disk object
<h2 id="src.parted3.partition_module.delete_partition">delete_partition</h2>

```python
delete_partition(diskob, part)
```
Remove partition from disk object
<h2 id="src.parted3.partition_module.get_partition_size">get_partition_size</h2>

```python
get_partition_size(diskob, part)
```
Get disk object's partition size
<h2 id="src.parted3.partition_module.get_size_txt">get_size_txt</h2>

```python
get_size_txt(length, sector_size)
```
Get size string
<h2 id="src.parted3.partition_module.create_partition">create_partition</h2>

```python
create_partition(diskob, part_type, geom)
```
Create a new partition
<h2 id="src.parted3.partition_module.geom_builder">geom_builder</h2>

```python
geom_builder(diskob, first_sector, last_sector, size_in_mbytes, beginning=True)
```
Helper function to calculate geometry.
OK, two new specs.  First, you must specify the first sector
and the last sector of the free space.  This way we can prevent out of
bound and math problems.  Currently, I use 5 sectors to 'round' to limits
We can change later to be the minimum allowed size for partition
However, if user is advanced and purposely wants to NOT include some
area of disk between 5 and smallest allowed partition, we should let him.

'beginning' defaults to True.  This starts partition at beginning of
free space.  Specify to False to instead start at end
let's use kb = 1000b, mb = 10000000b, etc etc
<h2 id="src.parted3.partition_module.check_mounted">check_mounted</h2>

```python
check_mounted(part)
```
" Simple check to see if partition is mounted (or busy)
<h2 id="src.parted3.partition_module.get_used_space">get_used_space</h2>

```python
get_used_space(part)
```
Get partition used space
<h2 id="src.parted3.partition_module.get_used_space_from_path">get_used_space_from_path</h2>

```python
get_used_space_from_path(path)
```
Get partition used space
<h2 id="src.parted3.partition_module.get_largest_size">get_largest_size</h2>

```python
get_largest_size(diskob, part)
```
Call this to set the initial size of new partition in frontend, but also
the MAX to which user may enter.
<h2 id="src.parted3.partition_module.set_flag">set_flag</h2>

```python
set_flag(flagno, part)
```
Set partition flag
<h2 id="src.parted3.partition_module.unset_flag">unset_flag</h2>

```python
unset_flag(flagno, part)
```
Remove partition flag
<h2 id="src.parted3.partition_module.get_flags">get_flags</h2>

```python
get_flags(part)
```
Get partition flags
<h2 id="src.parted3.partition_module.get_flag">get_flag</h2>

```python
get_flag(part, flag)
```
Get partition flag
<h2 id="src.parted3.partition_module.finalize_changes">finalize_changes</h2>

```python
finalize_changes(diskob)
```
Store all changes (we won't be able to undo them!)
<h2 id="src.parted3.partition_module.order_partitions">order_partitions</h2>

```python
order_partitions(partdic)
```
Pass the result of get_partitions here and it will return list
of partitions in order as they are on disk
<h2 id="src.parted3.partition_module.split_partition">split_partition</h2>

```python
split_partition(device_path, partition_path, new_size_in_mb)
```
Shrinks partition and splits it in two.
ALERT: The file system must be resized before trying this!
<h2 id="src.parted3.partition_module.example">example</h2>

```python
example()
```
Usage example

<h1 id="src.installation.wrapper">src.installation.wrapper</h1>

Helper module to run some disk/partition related utilities
<h2 id="src.installation.wrapper.wipefs">wipefs</h2>

```python
wipefs(device, fatal=True)
```
Wipe fs from device
<h2 id="src.installation.wrapper.run_dd">run_dd</h2>

```python
run_dd(input_device, output_device, bytes_block=512, count=2048, seek=0)
```
Helper function to call dd
Copy a file, converting and formatting according to the operands.
<h2 id="src.installation.wrapper.sgdisk">sgdisk</h2>

```python
sgdisk(command, device)
```
Helper function to call sgdisk (GPT)
<h2 id="src.installation.wrapper.sgdisk_new">sgdisk_new</h2>

```python
sgdisk_new(device, part_num, label, size, hex_code)
```
Helper function to call sgdisk --new (GPT)
<h2 id="src.installation.wrapper.parted_set">parted_set</h2>

```python
parted_set(device, number, flag, state)
```
Helper function to call set parted command
<h2 id="src.installation.wrapper.parted_mkpart">parted_mkpart</h2>

```python
parted_mkpart(device, ptype, start, end, filesystem='')
```
Helper function to call mkpart parted command
<h2 id="src.installation.wrapper.parted_mklabel">parted_mklabel</h2>

```python
parted_mklabel(device, label_type='msdos')
```
Helper function to call mktable parted command

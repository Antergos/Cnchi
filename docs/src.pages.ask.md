<h1 id="src.pages.ask">src.pages.ask</h1>

Asks which type of installation the user wants to perform
<h2 id="src.pages.ask.check_alongside_disk_layout">check_alongside_disk_layout</h2>

```python
check_alongside_disk_layout()
```
Alongside can only work if user has followed the recommended
BIOS-Based Disk-Partition Configurations shown in
http://technet.microsoft.com/en-us/library/dd744364(v=ws.10).aspx
<h2 id="src.pages.ask.load_zfs">load_zfs</h2>

```python
load_zfs()
```
Load ZFS kernel module
<h2 id="src.pages.ask.InstallationAsk">InstallationAsk</h2>

```python
InstallationAsk(self, params, prev_page='mirrors', next_page=None)
```
Asks user which type of installation wants to perform

<h1 id="src.download.metalink">src.download.metalink</h1>

Operations with metalinks
<h2 id="src.download.metalink.get_info">get_info</h2>

```python
get_info(metalink)
```
Reads metalink xml info and returns it
<h2 id="src.download.metalink.create">create</h2>

```python
create(alpm, package_name, pacman_conf_file)
```
Creates a metalink to download package_name and its dependencies
<h2 id="src.download.metalink.download_queue_to_metalink">download_queue_to_metalink</h2>

```python
download_queue_to_metalink(download_queue)
```
Converts a download_queue object to a metalink
<h2 id="src.download.metalink.Metalink">Metalink</h2>

```python
Metalink(self)
```
Metalink class
<h2 id="src.download.metalink.PkgSet">PkgSet</h2>

```python
PkgSet(self, pkgs=None)
```
Represents a set of packages
<h2 id="src.download.metalink.DownloadQueue">DownloadQueue</h2>

```python
DownloadQueue(self)
```
Represents a download queue
<h2 id="src.download.metalink.parse_args">parse_args</h2>

```python
parse_args(args)
```
Parse arguments to build_download_queue function
These arguments mimic pacman ones
<h2 id="src.download.metalink.get_antergos_repo_pkgs">get_antergos_repo_pkgs</h2>

```python
get_antergos_repo_pkgs(alpm_handle)
```
Returns pkgs from Antergos groups (cinnamon, mate, mate-extra) and
the antergos db info
<h2 id="src.download.metalink.resolve_deps">resolve_deps</h2>

```python
resolve_deps(alpm_handle, other, alldeps)
```
Resolve dependencies
<h2 id="src.download.metalink.create_package_set">create_package_set</h2>

```python
create_package_set(requested, repo_pkgs, antdb, alpm_handle)
```
Create package set from requested set
<h2 id="src.download.metalink.build_download_queue">build_download_queue</h2>

```python
build_download_queue(alpm, args=None)
```
Function to build a download queue.
Needs a pkgname in args
<h2 id="src.download.metalink.get_checksum">get_checksum</h2>

```python
get_checksum(path, typ)
```
Returns checksum of a file
<h2 id="src.download.metalink.check_cache">check_cache</h2>

```python
check_cache(conf, pkgs)
```
Checks package checksum in cache
<h2 id="src.download.metalink.needs_sig">needs_sig</h2>

```python
needs_sig(siglevel, insistence, prefix)
```
Determines if a signature should be downloaded.
The siglevel is the pacman.conf SigLevel for the given repo.
The insistence is an integer. Anything below 1 will return false,
anything above 1 will return true, and 1 will check if the
siglevel is required or optional.
The prefix is either "Database" or "Package".
<h2 id="src.download.metalink.test_module">test_module</h2>

```python
test_module()
```
Module test function

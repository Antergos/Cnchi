<h1 id="src.download.download_requests">src.download.download_requests</h1>

Module to download packages using requests library
<h2 id="src.download.download_requests.get_md5">get_md5</h2>

```python
get_md5(file_name)
```
Gets md5 hash from a file
<h2 id="src.download.download_requests.CopyToCache">CopyToCache</h2>

```python
CopyToCache(self, origin, xz_cache_dirs)
```
Class thread to copy a xz file to the user's
provided cache directory
<h2 id="src.download.download_requests.Download">Download</h2>

```python
Download(self, pacman_cache_dir, xz_cache_dirs, callback_queue, proxies=None)
```
Class to download packages using requests
This class tries to previously download all necessary packages for
Antergos installation using requests

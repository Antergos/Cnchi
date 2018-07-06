<h1 id="src.misc.osextras">src.misc.osextras</h1>

Module with some os helper functions
<h2 id="src.misc.osextras.realpath_root">realpath_root</h2>

```python
realpath_root(root, filename)
```
Like os.path.realpath, but resolved relative to root.
filename must be absolute.
<h2 id="src.misc.osextras.find_on_path_root">find_on_path_root</h2>

```python
find_on_path_root(root, command)
```
Is command on the executable search path relative to root?
<h2 id="src.misc.osextras.find_on_path">find_on_path</h2>

```python
find_on_path(command)
```
Is command on the executable search path?
<h2 id="src.misc.osextras.unlink_force">unlink_force</h2>

```python
unlink_force(path)
```
Unlink path, without worrying about whether it exists.
<h2 id="src.misc.osextras.glob_root">glob_root</h2>

```python
glob_root(root, pathname)
```
Like glob.iglob, but resolved relative to root.
pathname must be absolute.

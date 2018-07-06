<h1 id="src.pacman.pkginfo">src.pacman.pkginfo</h1>


Package information formatting

This module defines utility functions to format package information
for terminal output.

<h2 id="src.pacman.pkginfo.get_term_size">get_term_size</h2>

```python
get_term_size()
```
Gets terminal width in chars
<h2 id="src.pacman.pkginfo.format_attr">format_attr</h2>

```python
format_attr(attrname, value, attrformat=None)
```
Formats string from value
<h2 id="src.pacman.pkginfo.format_attr_oneperline">format_attr_oneperline</h2>

```python
format_attr_oneperline(attrname, value)
```
Formats string from value (one value per line)
<h2 id="src.pacman.pkginfo.display_pkginfo">display_pkginfo</h2>

```python
display_pkginfo(pkg, level=1, style='local')
```

Displays pretty-printed package information.

Args :
  pkg -- the package to display
  level -- the level of detail (1 or 2)
  style -- 'local' or 'sync'

<h2 id="src.pacman.pkginfo.get_pkginfo">get_pkginfo</h2>

```python
get_pkginfo(pkg, level=1, style='local')
```
Stores package info into a dictonary

<h1 id="src.pages.mirrors">src.pages.mirrors</h1>

Let advanced users manage mirrorlist files
<h2 id="src.pages.mirrors.MirrorListBoxRow">MirrorListBoxRow</h2>

```python
MirrorListBoxRow(self, url, active, switch_cb, drag_cbs)
```
Represents a mirror
<h2 id="src.pages.mirrors.MirrorListBox">MirrorListBox</h2>

```python
MirrorListBox(self, mirrors_file_path, settings)
```
List that stores all mirrors
<h2 id="src.pages.mirrors.Mirrors">Mirrors</h2>

```python
Mirrors(self, params, prev_page='cache', next_page='installation_ask')
```
Page that shows mirrolists so the user can arrange them manually

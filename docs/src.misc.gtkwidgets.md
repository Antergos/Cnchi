<h1 id="src.misc.gtkwidgets">src.misc.gtkwidgets</h1>

Additional GTK widgets (some are borrowed from Ubiquity)
<h2 id="src.misc.gtkwidgets.refresh">refresh</h2>

```python
refresh()
```
Tell Gtk loop to run pending events
<h2 id="src.misc.gtkwidgets.draw_round_rect">draw_round_rect</h2>

```python
draw_round_rect(context, rounded, start_x, start_y, width, height)
```
Draw a rectangle with rounded corners
<h2 id="src.misc.gtkwidgets.gtk_to_cairo_color">gtk_to_cairo_color</h2>

```python
gtk_to_cairo_color(gtk_color)
```
Converts gtk color to cairo color format
<h2 id="src.misc.gtkwidgets.StylizedFrame">StylizedFrame</h2>

```python
StylizedFrame(self)
```
Frame with rounded corners
<h2 id="src.misc.gtkwidgets.DiskBox">DiskBox</h2>

```python
DiskBox(self, *args, **kwargs)
```
Disk Box widget
<h2 id="src.misc.gtkwidgets.PartitionBox">PartitionBox</h2>

```python
PartitionBox(self, title='', extra='', icon_name='', icon_file='')
```
Widget to contain partition info
<h2 id="src.misc.gtkwidgets.ResizeWidget">ResizeWidget</h2>

```python
ResizeWidget(self, part_size, min_size, max_size)
```
Widget used to resize partitions
<h2 id="src.misc.gtkwidgets.StateBox">StateBox</h2>

```python
StateBox(self, text='')
```
Widget used to show any kind of information
<h2 id="src.misc.gtkwidgets.Builder">Builder</h2>

```python
Builder(self)
```
GtkBuilder should have .get_object_ids() method

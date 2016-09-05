# UI
### Overview
This directory houses Cnchi's UI code. Cnchi is designed to support a pluggable UI. What that means is that its possible to use other toolkits/frameworks for the UI without having to make major modifications to the rest of the codebase. Currently, the HTML/JavaScript UI is the focus of all active development as it is the default.
### What's Inside
|File/Dir|Description|
|:---|:---|
|**gtk**|Contains code specific to a GTK based UI.|
|**html**|Contains code specific to the HTML/JavaScript based UI.|
|**tpl**|All template files go here.|
|base_widgets.py|Contains base classes that are subclassed by the UIs.|
|controller.py|As it's name suggests, it contains Cnchi's UI controller class.|

### 
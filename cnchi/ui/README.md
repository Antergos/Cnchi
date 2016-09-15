# UI
### Overview
This directory houses Cnchi's UI code. Cnchi is designed with a pluggable UI. That means its possible to use other toolkits/frameworks for the UI without having to make major modifications to the rest of the codebase. Currently, the ReactJS UI is the default so its the focus of active development.
### What's Inside
|File/Dir|Description|
|:---|:---|
|**gtk**|GTK+ based UI.|
|~~**html**~~|~~HTML/JavaScript based UI.~~|
|**react**|ReactJS based UI rendered by WebKitGTK+|
|**tpl**|All template files go here.|
|base_widgets.py|Contains base classes that are subclassed by the UI modules.|
|controller.py|As it's name suggests, it contains Cnchi's UI controller class.|

### Implementation Details
All UI classes should be derived from `BaseWidget` which in turn is derived from `BaseObject`. This approach ensure that all of Cnchi's runtime data including user input is easily accessible throughout the codebase.

UI "modules" (for lack of a better term), must provide the following classes at minimum:
* {{ui dirname}}Controller
  - eg. `ReactController(BaseObject)`

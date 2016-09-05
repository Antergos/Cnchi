# HTML/JavaScript UI
### Overview
This directory contains the default UI "module" which is driven by HTML/JavaScript that is rendered by Webkit via WebKitGTK+. 
### What's Inside
|File/Dir|Description|
|:---|:---|
|**pages**|Cnchi's workflow is comprised of a series of pages. They are housed here.|
|container.py|`MainContainer` - Handles the WebKitWebView.|
|controller.py|`HTMLController` - The main entry point for this UI "module".|
|main_window.py|`MainWindow` - The application's main window.|
|pages_helper.py|`PagesHelper` - Provides helper methods for dealing with pages.|

### Development
#### Requirements
* npm
* nodejs-grunt-cli

#### Running Cnchi
Before you can run Cnchi in a local environment you need to run the following commands from within this directory:

```sh
$ npm install
$ grunt
```
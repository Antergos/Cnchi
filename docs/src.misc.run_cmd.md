<h1 id="src.misc.run_cmd">src.misc.run_cmd</h1>

Chroot related functions. Used in the installation process
<h2 id="src.misc.run_cmd.ensured_executable">ensured_executable</h2>

```python
ensured_executable(cmd)
```

Ensures file is executable before attempting to execute it.

Args:
    cmd (list): The command to check.

Returns:
    True if successful, False otherwise.


<h2 id="src.misc.run_cmd.log_exception_info">log_exception_info</h2>

```python
log_exception_info()
```
This function logs information about the exception that is currently
being handled. The information returned is specific both to the current
thread and to the current stack frame.
<h2 id="src.misc.run_cmd.call">call</h2>

```python
call(cmd, warning=True, error=False, fatal=False, msg=None, timeout=None, stdin=None, debug=True)
```
Helper function to make a system call
warning: If true will log a warning message if an error is detected
error: If true will log an error message if an error is detected
fatal: If true will log an error message AND will raise an InstallError exception
msg: Error message to log (if empty the command called will be logged)
<h2 id="src.misc.run_cmd.chroot_call">chroot_call</h2>

```python
chroot_call(cmd, chroot_dir='/install', fatal=False, msg=None, timeout=None, stdin=None)
```
Runs command inside the chroot
<h2 id="src.misc.run_cmd.popen">popen</h2>

```python
popen(cmd, warning=True, error=False, fatal=False, msg=None, stdin=-1)
```
Helper function that calls Popen (useful if we need to use pipes)

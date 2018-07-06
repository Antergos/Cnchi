<h1 id="src.misc.validation">src.misc.validation</h1>

Validation module
<h2 id="src.misc.validation.check_grub_device">check_grub_device</h2>

```python
check_grub_device(device)
```
Check that the user entered a valid boot device.
@return True if the device is valid, False if it is not.
<h2 id="src.misc.validation.check">check</h2>

```python
check(element, value)
```
Check element value
<h2 id="src.misc.validation.check_username">check_username</h2>

```python
check_username(name)
```
Check the correctness of a proposed user name.

@return empty list (valid) or list of:
    - C{NAME_LENGTH} wrong length.
    - C{NAME_BADCHAR} contains invalid characters.
    - C{NAME_BADHYPHEN} starts or ends with a hyphen.
    - C{NAME_BADDOTS} contains consecutive/initial/final dots.
<h2 id="src.misc.validation.check_hostname">check_hostname</h2>

```python
check_hostname(name)
```
Check the correctness of a proposed host name.

@return empty list (valid) or list of:
    - C{NAME_LENGTH} wrong length.
    - C{NAME_BADCHAR} contains invalid characters.
    - C{NAME_BADHYPHEN} starts or ends with a hyphen.
    - C{NAME_BADDOTS} contains consecutive/initial/final dots.
<h2 id="src.misc.validation.password_strength">password_strength</h2>

```python
password_strength(password)
```
Checks password strength
<h2 id="src.misc.validation.human_password_strength">human_password_strength</h2>

```python
human_password_strength(password)
```
Converts password strength to a human message
<h2 id="src.misc.validation.check_password">check_password</h2>

```python
check_password(password, verified_password, password_ok, password_error_label, strength, allow_empty=False)
```
Check user password
This function expects Gtk widgets as parameters

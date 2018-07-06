<h1 id="src.installation.lemp">src.installation.lemp</h1>


LEMP stack is a group of open source software to get web servers up
and running. The acronym stands for Linux, nginx (pronounced Engine x),
MySQL, and PHP. Since the server is already running Antergos, the linux
part is taken care of.

<h2 id="src.installation.lemp.setup">setup</h2>

```python
setup()
```
Main configuration function
<h2 id="src.installation.lemp.mariadb_setup">mariadb_setup</h2>

```python
mariadb_setup()
```
Setup MariaDB database server
<h2 id="src.installation.lemp.nginx_setup">nginx_setup</h2>

```python
nginx_setup()
```
Setup Nginx web server
<h2 id="src.installation.lemp.php_setup">php_setup</h2>

```python
php_setup()
```
Setup /etc/php/php.ini

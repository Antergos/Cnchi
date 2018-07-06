<h1 id="src.misc.i18n">src.misc.i18n</h1>

Internationalisation helper functions (read languagelist.data)
<h2 id="src.misc.i18n.utf8">utf8</h2>

```python
utf8(my_string, errors='strict')
```
Decode a string as UTF-8 if it isn't already Unicode.
<h2 id="src.misc.i18n.get_languages">get_languages</h2>

```python
get_languages(language_list='data/languagelist.data.gz', current_language_index=-1)
```
Returns a tuple of (current language, sorted choices, display map).

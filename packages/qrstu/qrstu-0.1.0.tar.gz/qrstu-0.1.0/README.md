# Q – Rainer Schwarzbach’s Text Utilities

_Test conversion and transcoding utilities_


## Installation from PyPI

```
pip install qrstu
```

Installation in a virtual environment is strongly recommended.


## Usage

### reduce

The **reduce** module can be used to reduce Unicode text
in Latin script to ASCII encodable Unicode text,
similar to **[Unidecode](https://pypi.org/project/Unidecode/)**
but taking a different approach
(ie. mostly wrapping functionality from the standard library module
**[unicodedata](https://docs.python.org/3/library/unicodedata.html)**).
Unlike **Unidecode** which also transliterates characters from non-Latin scripts,
**reduce** stubbornly refuses to handle these.

You can, however, specify an optional `errors=` argument in the
**reduce.reduce_text()** call, which is passed to the internally used
**[codecs.encode()](https://docs.python.org/3/library/codecs.html#codecs.encode)**
function, thus taking advance of the codecs module errors handling.

```python
>>> from qrstu import reduce
>>> # Vietnamese text
>>> reduce.reduce_text("Chào mừng đến với Hà Nội!")
'Chao mung dhen voi Ha Noi!'
>>>
>>> # Trying the Unidecode examples …
>>> reduce.reduce_text('kožušček')
'kozuscek'
>>> reduce.reduce_text('30 \U0001d5c4\U0001d5c6/\U0001d5c1')
'30 km/h'
>>> reduce.reduce_text('\u5317\u4EB0')
Traceback (most recent call last):
  File "…/qrstu/src/qrstu/reduce.py", line 354, in reduce_text
    chunk = translations[character.nfc]
            ~~~~~~~~~~~~^^^^^^^^^^^^^^^
KeyError: '北'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "…/qrstu/src/qrstu/reduce.py", line 276, in reduce
    collector.append(PRESET_CHARACTER_REDUCTIONS[codepoint])
                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
KeyError: 21271

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "…/qrstu/src/qrstu/reduce.py", line 356, in reduce_text
    chunk = character.reduce(errors=errors)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "…/qrstu/src/qrstu/reduce.py", line 278, in reduce
    encoded = codecs.encode(
              ^^^^^^^^^^^^^^
UnicodeEncodeError: 'ascii' codec can't encode character '\u5317' in position 0: ordinal not in range(128)
>>> reduce.reduce_text('\u5317\u4EB0', errors="ignore")
''
>>> reduce.reduce_text('\u5317\u4EB0', errors="replace")
'??'
>>> reduce.reduce_text('\u5317\u4EB0', errors="backslashreplace")
'\\u5317\\u4eb0'
>>> reduce.reduce_text('\u5317\u4EB0', errors="xmlcharrefreplace")
'&#21271;&#20144;'
>>> reduce.reduce_text('\u5317\u4EB0', errors="namereplace")
'\\N{CJK UNIFIED IDEOGRAPH-5317}\\N{CJK UNIFIED IDEOGRAPH-4EB0}'
>>>

```


## Further reading

Please see the documentation at <https://blackstream-x.gitlab.io/qrstu>
for detailed usage information.

If you found a bug or have a feature suggestion,
please open an issue [here](https://gitlab.com/blackstream-x/qrstu/-/issues)


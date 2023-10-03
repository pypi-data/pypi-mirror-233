# shushlog

![PyPI](https://img.shields.io/pypi/v/shushlog?logo=python)
![PyPI - License](https://img.shields.io/pypi/l/shushlog)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/shushlog)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)


Async-compatible, dependency-less, simple log suppression and filtering lib

## Install

```shell
pip install shushlog
```

## TLDR

- supress all logs

```python
>>> import logging
>>> import shush
>>> logging.basicConfig()
>>> logger = logging.getLogger("some_logger")
>>> logger.setLevel(logging.INFO)
>>> @shush.suppress
>>> def suppressed_func():
>>>     logger.info("this should not be logged")
>>> def normal_func():
>>>     logger.info("this should be logged")
>>> suppressed_func()
>>> normal_func()
INFO:some_logger:this should be logged
```

- muzzle text
```python
>>> import logging
>>> import shush
>>> logging.basicConfig()
>>> logger = logging.getLogger("some_logger")
>>> logger.setLevel(logging.INFO)
>>> @shush.muzzle("foo")
>>> def muzzled_func():
>>>     logger.info("this contains `foo`, so it should be muzzled out")
>>>     logger.info("this doesn't contain it, so it should be showing")
>>> muzzled_func()
INFO:some_logger:this doesn't contain it, so it should be showing
```

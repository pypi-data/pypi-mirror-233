# pyAlice

pyAlice - framework for simplifying work with Yandex Alice

## Getting started

```
pip install pyaliceya
```

[example of an empty dialog](https://github.com/sergey200519/pyAlice-project)

[detailed documentation](https://sergey200519.github.io/pyAlice-documentation/)

## Handler

example of the "handler" function

```
from pyAlice.py_alice import PyAlice
import settings

def handler(event, context):
  return PyAlice(params_alice=event, settings=settings).get_params_for_alice()
```
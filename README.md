# Python system utility toolkit

This module contains various small utility methods and common classes for working in python.

These classes have moved from *systematic* and *cli-toolkit* modules to this module.

## Installing

This module has minimal dependencies (PyYAML) and should install with *pip* on any recent
python version. The module has been tested with python 3.9 and python 3.10.

## Running unit tests and linters

All tests are run with *tox*.

Run unit tests, flake8 and pylint:

```bash
make
```

Run unit tests:

```bash
make test
```

Run flake8 and pylint:

```bash
make lint
```

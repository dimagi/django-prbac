# Releasing on PyPI

We follow https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
(Oct 2019 version).


## One-time setup

Make sure your `~/.pypirc` is set up like this

```bash
[distutils]
index-servers=
    pypi
    test

[test]
repository = https://test.pypi.org/legacy/
username = <your test user name goes here>

[pypi]
username = __token__
```

## Build
```bash
rm -rf build dist
python -m pep517.build .
```

## Push to PyPI staging server

```bash
twine upload -r test --sign dist/*
```

In a different virtualenv, test that you can install it:

```bash
pip install -i https://testpypi.python.org/pypi django-prbac --upgrade
```


## Push to PyPI

```bash
twine upload -r pypi --sign dist/*
```

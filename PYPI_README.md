# Releasing on PyPI

## Push to PyPI staging server

Update the build version in `django_prbac/__init__.py`. Push changes to Github
and go through the process to get them merged into master. A new version will
automatically be pushed to https://test.pypi.org/project/django-prbac/

In a different virtualenv, test that you can install it:

```bash
pip install -i https://testpypi.python.org/pypi django-prbac --upgrade
```


## Push to PyPI

Add a version tag formatted as `vX.Y.Z` to the commit on master that you want
to publish. Push the tag to Github with `git push --tags`. Wait for the
[PyPI workflow](https://github.com/dimagi/django-prbac/actions/workflows/tests.yml)
to complete. Confirm that the package has been pushed to
[PyPI](https://pypi.org/project/django-prbac/).

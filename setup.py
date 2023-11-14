import os
import re
from io import open
from setuptools import setup, find_packages

THISDIR = os.path.dirname(os.path.abspath(__file__))


def get_version():
    version_re = re.compile(r"""^__version__ = (['"])(.*?)\1$""", re.M)
    path = os.path.join(THISDIR, "django_prbac/__init__.py")
    with open(path, encoding="utf-8") as fh:
        return version_re.search(fh.read()).group(2)


def get_readme():
    path = os.path.join(THISDIR, "README.rst")
    with open(path, encoding="utf-8") as fh:
        return fh.read()


setup(
    name='django-prbac',
    version=get_version(),
    description='Parameterized Role-Based Access Control for Django',
    long_description=get_readme(),
    author='Dimagi',
    author_email='dev@dimagi.com',
    url='http://github.com/dimagi/django-prbac',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        # avoid django 3 < 3.0.7
        # https://github.com/advisories/GHSA-hmr4-m2h5-33qx
        'django>=3.0.7,<5',
        'jsonfield>=1.0.3,<4',
        'simplejson',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    options={"bdist_wheel": {"universal": "1"}},
)

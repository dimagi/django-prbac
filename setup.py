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
        'django>=1.8,<2.1',
        'jsonfield>=1.0.3',
        'simplejson',
        'six',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

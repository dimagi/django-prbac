import os
import re
from setuptools import setup, find_packages

def get_version():
    version_re = re.compile(r"""^__version__ = (['"])(.*?)\1$""", re.M)
    thisdir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(thisdir, "django_prbac/__init__.py")
    with open(path) as fh:
        return version_re.search(fh.read()).group(2)

setup(
    name='django-prbac',
    version=get_version(),
    description='Parameterized Role-Based Access Control for Django',
    author='Dimagi',
    author_email='dev@dimagi.com',
    url='http://github.com/dimagi/django-prbac',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'django>=1.8,<1.11',
        'jsonfield>=1.0.3',
        'simplejson',
        'six',
    ],
)

from setuptools import setup, find_packages

setup(
    name='django-prbac',
    version='0.0.3',
    description='Parameterized Role-Based Access Control for Django',
    author='Dimagi',
    author_email='dev@dimagi.com',
    url='http://github.com/dimagi/django-prbac',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'django>=1.10,<1.11',
        'jsonfield>=1.0.3',
        'simplejson',
        'six',
    ],
)

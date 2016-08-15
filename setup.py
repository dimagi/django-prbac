from setuptools import setup, find_packages

setup(
    name='django-prbac',
    version='0.0.2',
    description='Parameterized Role-Based Access Control for Django',
    author='Dimagi',
    author_email='dev@dimagi.com',
    url='http://github.com/dimagi/django-prbac',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'django>=1.7a,<1.9',
        'jsonfield>=1.0.3',
        'simplejson',
        'six',
    ],
)

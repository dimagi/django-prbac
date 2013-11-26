from setuptools import setup

setup(
    name='django-prbac',
    version='0.0.2',
    description='Parameterized Role-Based Access Control for Django',
    author='Dimagi',
    author_email='information@dimagi.com',
    url='http://github.com/dimagi/django-prbac',
    packages=['django_prbac'],
    install_requires=[
        'django>=1.3.7',
        'django-json-field>=0.5.5',
        'simplejson',
        'South',
    ],
)

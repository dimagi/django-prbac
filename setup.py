from setuptools import setup

setup(
    name='django-prbac',
    version='0.0.2',
    description='Parameterized Role-Based Access Control for Django',
    author='Dimagi',
    author_email='information@dimagi.com',
    url='http://github.com/dimagi/django-prbac',
    packages=['django_prbac'],
    zip_safe=False,
    install_requires=[
        'django>=1.7a,<1.9',
        'django-json-field>=0.5.5',
        'simplejson'
    ],
)

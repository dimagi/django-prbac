
Installation and Set Up
=======================

There are no special steps to set up `django_prbac` beyond those for any Django app.

The first step is to install the Python package via `pip` or `easy_install`::

    $ pip install django-prbac

Then add `django_prbac` to the `INSTALLED_APPS` in your settings module
(this will be `settings.py` for default projects)::

    # in setting.py
    INSTALLED_APPS = [
        ...
        'django_prbac',
    ]

Set up the database by running the migrations::

    $ python manage.py migrate django_prbac

If you wish, you can run the tests to check the health of your installation. This will not modify any
of your data::

    $ python manage.py test django_prbac --settings django_prbac.mock_settings

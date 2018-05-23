Django PRBAC
============

(Parameterized Role-Based Access Control)

https://github.com/dimagi/django-prbac

|Build Status| |Test coverage| |PyPi version|

About RBAC and PRBAC
--------------------

**Role-based access control (RBAC)** is the standard method for access control in large systems.
With RBAC, you grant *privileges* to *roles*. For example you
might grant the privilege ``Reporting`` to the role ``Analyst``. In most
systems, you can nest roles as deeply as you want, and give users however many roles. A good
example of this in practice is `PostgreSQL roles and privileges
<http://www.postgresql.org/docs/devel/static/user-manag.html>`_.

The roles and privileges are whatever abstract concepts make sense for your system. It is up
to application code to determine what actions to take based on the privileges granted. This
can, of course, be implemented in terms of a lower-level permission system such as
row-level or object-level access control lists (ACLs).

**Parameterized role-based access control (PRBAC)** adds parameters
to roles and privileges. Now, for example, you might grant ``"Reporting(organization="Dimagi",area="Finance")``
to ``FinancialAnalyst(organization="Dimagi")``. If you don't use parameters, then it is just RBAC.
If you use parameters with finite sets of choice, then it is exponentially more powerful. If you
use parameters with infinitely many choices (such as strings or integers) then it is
infinitely more powerful. A good example of limited parameterization is how particular privileges
(``SELECT``, ``UPDATE``, etc) in PostgreSQL may be parameterized by an object. In PRBAC
this parameterization is pervasive.


In-depth documentation
----------------------

To learn more about parameterized role-based access control as implemented in this library, please
visit http://django-prbac.readthedocs.org/


Access Control for Django
-------------------------

* `django.contrib.auth <https://docs.djangoproject.com/en/dev/topics/auth/>`_: This app, shipped with Django, provides unix-style access control (users, groups, permissions) 
  with an extensible set of permissions that are implicitly parameterized by a content type. This is
  fundamentally different than role-based access control. It is only worth mentioning because it comes
  with Django and everyone is going to want to know "why did you reimplement the wheel?". If ``django.contrib.auth``
  is the wheel, then RBAC is the car and PRBAC is a transformer. I leave it as an exercise to the reader to
  attempt to implement PRBAC using ``django.contrib.auth`` :-)

* `django-rbac <https://bitbucket.org/nabucosound/django-rbac/>`_: This project appears defunct and is not
  parameterized in any rate.
  
* `django-role-permissions <https://github.com/vintasoftware/django-role-permissions>`_: This app implements a sort of
  RBAC where roles are statically defined in code.
  
* Others can be perused at https://www.djangopackages.com/grids/g/perms/. Many offer object-level permissions,
  which is as orthogonal to role-based access control as unix permissions. In fact, this is probably true of 
  anything using the term "permissions".


Quick Start
-----------

To install, use pip:

::

    $ pip install django-prbac

License
-------

Django-prbac is distributed under the MIT license. (See the LICENSE file for details)

.. |Build Status| image:: https://travis-ci.org/dimagi/django-prbac.png?branch=master
   :target: https://travis-ci.org/dimagi/django-prbac
.. |Test coverage| image:: https://coveralls.io/repos/dimagi/django-prbac/badge.png?branch=master
   :target: https://coveralls.io/r/dimagi/django-prbac
.. |PyPi version| image:: https://img.shields.io/pypi/v/django-prbac.svg
   :target: https://pypi.python.org/pypi/django-prbac
.. |PyPi downloads| image:: https://img.shields.io/pypi/dm/django-prbac.svg
   :target: https://pypi.python.org/pypi/django-prbac

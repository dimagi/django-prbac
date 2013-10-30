.. django-prbac documentation master file, created by
   sphinx-quickstart on Tue Oct 29 17:06:26 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Parameterized Role-Based Access Control for Django
==================================================

The django-prbac package provides the basic components of parameterized role-based
access control for Django. The entirety of the system is contained in two classes
of objects:

1. :class:`~django_prbac.models.Role` (representing users, groups, capabilities, and privileges)
2. :class:`~django_prbac.models.Grant` (representing memberships, containment, and permissions)

If you are familiar with role-based access control (RBAC) then this is a minor, though
foundational, enhancement to the non-parameterized version. It will often make the
role graph much smaller and simpler, and will definitely allow much more
powerful administration of the graph.

Contents:

.. toctree::
    :glob:
    :maxdepth: 2

    setup
    tutorial
    apidoc/django_prbac

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


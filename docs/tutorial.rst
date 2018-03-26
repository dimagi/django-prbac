.. django-prbac documentation master file, created by
   sphinx-quickstart on Tue Oct 29 17:06:26 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django PRBAC Tutorial
=====================

Models of class |Role| represent capabilities, which may
intuitively map to users, privileges, groups, and collections of privileges.

Models of class |Grant| represent adding a user to a group,
including a group in another group, and granting privileges to
a user or group.


Users
-----

This library does not replace or modify the Django user system -- too many projects
muck around with that, so it is safer and more flexible to leave it alone. Instead,
you may give each user a corresponding |Role|::

    >>> from django.contrib.auth.models import User
    >>> for user in User.objects.all():
            Role.objects.create(
                name=user.username,
                slug=user.username,
                description='Role for django user: %s' % user.username
            )

This is very easy to automate with triggers or via the `UserProfile` feature of Django.


Privileges
----------

A privilege is an actual thing that a user may do in the system. It is up to you
to decide what these are and give them meaningful names and descriptions.
For example, perhaps there is a granular permission of "may view reports"::

    >>> may_view_reports = Role.objects.create(name='may_view_reports', slug='may_view_reports', description='May view reports')

    >>> biyeun = Role.objects.get(name='biyeun')
    >>> kenn = Role.objects.get(name='kenn')

    >>> Grant.objects.create(from_role=biyeun, to_role=may_view_reports)

    >>> biyeun.has_privilege(may_view_reports)
    True

    >>> kenn.has_privilege(may_view_reports)
    False

All of this is normal for RBAC (without parameterization) but with PRBAC we can make this
privilege more granular::

    >>> may_view_report = Role.objects.create(name='may_view_report', slug='may_view_report', parameters=set(['report_name']))

    >>> Grant.objects.create(from_role=biyeun, to_role=may_view_report, assignment={'report_name': 'active_users'})
    >>> Grant.objects.create(from_role=kenn, to_role=may_view_report, assignment={'report_name': 'submissions'})

    >>> biyeun.has_privilege(may_view_report.instantiate({'report_name': 'active_users'}))
    True

    >>> biyeun.has_privilege(may_view_report.instantiate({'report_name': 'submissions'}))
    False

    >>> kenn.has_privilege(may_view_report.instantiate({'report_name': 'active_users'}))
    False

    >>> kenn.has_privilege(may_view_report.instantiate({'report_name': 'submissions'}))
    True


Groups
------

A group of users may be represented as a |Role| as well::

    >>> dimagineers = Role.objects.create(name='dimagineers', slug='dimagineers', description='Dimagi Engineers')

    >>> Grant.objects.create(from_role=kenn, to_role=dimagineers)
    >>> Grant.objects.create(from_role=biyeun, to_role=dimagineers)

Now both `kenn` and `biyeun` are members of role `dimagineers`.

    >>> kenn.has_privilege(dimagineers)
    True
    >>> biyeun.has_privilege(dimagineers)
    True

But groups can also be useful when parameterized, for granting a variety
of parameterized privileges to a group of people.

    >>> may_edit_report = Role.objects.create(
            name='may_edit_report',
            description='May edit report',
            slug='may_edit_report',
            parameters=set(['report_name']),
        )

    >>> report_superusers = Role.objects.create(
            name='report_superusers',
            description='Report Superusers',
            slug='report_superusers',
            parameters=set(['report_name']),
        )

    >>> Grant.objects.create(from_role=report_superusers, to_role=may_edit_report)
    >>> Grant.objects.create(from_role=report_superusers, to_role=may_view_report)
    >>> Grant.objects.create(
            from_role=kenn,
            to_role=report_superusers,
            assignment={'report_name': 'dashboard'},
        )

    >>> kenn.has_privilege(may_view_report.instantiate({'report_name': 'dashboard'}))
    True
    >>> kenn.has_privilege(may_edit_report.instantiate({'report_name': 'dashboard'}))
    True

.. |Role| :class:`~django_prbac.models.Role`
.. |Grant| :class:`~django_prbac.models.Grant`

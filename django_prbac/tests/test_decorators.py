# Use Modern Python
from __future__ import unicode_literals, absolute_import, print_function

# Django imports
from django.utils.unittest.case import TestCase
from django.http import HttpRequest

# Local imports
from django_prbac.decorators import requires_privilege
from django_prbac.exceptions import PermissionDenied
from django_prbac import arbitrary

class TestDecorators(TestCase):

    def setUp(self):
        self.zazzle_privilege = arbitrary.role(name=arbitrary.unique_name('zazzle'), parameters=set(['domain']))

    def test_requires_privilege_no_current_role(self):
        """
        When a privilege is required but there is no role attached
        to the current request, permission is denied. No crashing.
        """
        @requires_privilege(self.zazzle_privilege.name, domain='zizzle')
        def view(request, *args, **kwargs):
            pass

        request = HttpRequest()
        with self.assertRaises(PermissionDenied):
            view(request)

    def test_requires_privilege_no_such(self):
        """
        When a required privilege is not even defined in the database,
        permission is denied; no crashing.
        """
        @requires_privilege('bomboozle', domain='zizzle')
        def view(request, *args, **kwargs):
            pass


        requestor_role = arbitrary.role()
        request = HttpRequest()
        request.role = requestor_role
        with self.assertRaises(PermissionDenied):
            view(request)

    def test_requires_privilege_denied(self):
        """
        When a privilege exists but the current
        role does not have access to it, permission
        is denied
        """

        @requires_privilege(self.zazzle_privilege.name, domain='zizzle')
        def view(request, *args, **kwargs):
            pass

        requestor_role = arbitrary.role()

        request = HttpRequest()
        request.role = requestor_role.instantiate({})
        with self.assertRaises(PermissionDenied):
            view(request)


    def test_requires_privilege_ok(self):

        @requires_privilege(self.zazzle_privilege.name, domain='zizzle')
        def view(request, *args, **kwargs):
            pass

        requestor_role = arbitrary.role()
        arbitrary.grant(from_role=requestor_role, to_role=self.zazzle_privilege, assignment=dict(domain='zizzle'))

        request = HttpRequest()
        request.role = requestor_role.instantiate({})
        view(request)


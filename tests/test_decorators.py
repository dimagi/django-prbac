from django.test import TestCase
from django.http import HttpRequest

from django_prbac.decorators import requires_privilege
from django_prbac.exceptions import PermissionDenied
from django_prbac.models import Role
from django_prbac import arbitrary


class TestDecorators(TestCase):

    def setUp(self):
        Role.get_cache().clear()
        self.zazzle_privilege = arbitrary.role(slug=arbitrary.unique_slug('zazzle'), parameters=set(['domain']))

    def test_requires_privilege_no_current_role(self):
        """
        When a privilege is required but there is no role attached
        to the current request, permission is denied. No crashing.
        """
        @requires_privilege(self.zazzle_privilege.slug, domain='zizzle')
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

        @requires_privilege(self.zazzle_privilege.slug, domain='zizzle')
        def view(request, *args, **kwargs):
            pass

        requestor_role = arbitrary.role()

        request = HttpRequest()
        request.role = requestor_role.instantiate({})
        with self.assertRaises(PermissionDenied):
            view(request)

    def test_requires_privilege_wrong_param(self):

       @requires_privilege(self.zazzle_privilege.slug, domain='zizzle')
       def view(request, *args, **kwargs):
           pass

       requestor_role = arbitrary.role()
       arbitrary.grant(from_role=requestor_role, to_role=self.zazzle_privilege, assignment=dict(domain='whapwhap'))

       request = HttpRequest()
       request.role = requestor_role.instantiate({})
       with self.assertRaises(PermissionDenied):
           view(request)

    def test_requires_privilege_ok(self):

        @requires_privilege(self.zazzle_privilege.slug, domain='zizzle')
        def view(request, *args, **kwargs):
            pass

        requestor_role = arbitrary.role()
        arbitrary.grant(from_role=requestor_role, to_role=self.zazzle_privilege, assignment=dict(domain='zizzle'))

        request = HttpRequest()
        request.role = requestor_role.instantiate({})
        view(request)

    def test_requires_privilege_role_on_user_ok(self):
        """
        Verify that privilege is recognized when the request user has the prbac_role, but request.role is not set.
        """

        @requires_privilege(self.zazzle_privilege.slug, domain='zizzle')
        def view(request, *args, **kwargs):
            pass

        user = arbitrary.user()
        requestor_role = arbitrary.role()
        arbitrary.grant(from_role=requestor_role, to_role=self.zazzle_privilege, assignment=dict(domain='zizzle'))
        arbitrary.user_role(user=user, role=requestor_role)

        request = HttpRequest()
        request.user = user
        view(request)

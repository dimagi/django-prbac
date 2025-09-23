from django.test import TestCase  # https://code.djangoproject.com/ticket/20913

from django_prbac.models import Role
from django_prbac import arbitrary


class TestRole(TestCase):

    def setUp(self):
        Role.get_cache().clear()

    def test_has_permission_immediate_no_params(self):
        subrole = arbitrary.role()
        superrole1 = arbitrary.role()
        superrole2 = arbitrary.role()
        arbitrary.grant(to_role=superrole1, from_role=subrole)

        # A few ways of saying the same thing
        self.assertTrue(subrole.instantiate({}).has_privilege(superrole1.instantiate({})))
        self.assertTrue(subrole.has_privilege(superrole1.instantiate({})))
        self.assertTrue(subrole.instantiate({}).has_privilege(superrole1))
        self.assertTrue(subrole.has_privilege(superrole1))

        self.assertFalse(subrole.instantiate({}).has_privilege(superrole2.instantiate({})))
        self.assertFalse(subrole.has_privilege(superrole2.instantiate({})))
        self.assertFalse(subrole.instantiate({}).has_privilege(superrole2))
        self.assertFalse(subrole.has_privilege(superrole2))

    def test_has_permission_transitive_no_params(self):
        subrole = arbitrary.role()
        midrole = arbitrary.role()
        superrole1 = arbitrary.role()
        superrole2 = arbitrary.role()
        arbitrary.grant(to_role=midrole, from_role=subrole)
        arbitrary.grant(to_role=superrole1, from_role=midrole)

        # A few ways of saying the same thing
        self.assertTrue(subrole.instantiate({}).has_privilege(superrole1.instantiate({})))
        self.assertTrue(subrole.has_privilege(superrole1.instantiate({})))
        self.assertTrue(subrole.instantiate({}).has_privilege(superrole1))
        self.assertTrue(subrole.has_privilege(superrole1))

        self.assertFalse(subrole.instantiate({}).has_privilege(superrole2.instantiate({})))
        self.assertFalse(subrole.has_privilege(superrole2.instantiate({})))
        self.assertFalse(subrole.instantiate({}).has_privilege(superrole2))
        self.assertFalse(subrole.has_privilege(superrole2))

    def test_has_permission_far_transitive_no_params(self):
        subrole = arbitrary.role()
        superrole1 = arbitrary.role()
        superrole2 = arbitrary.role()

        midroles = [arbitrary.role() for __ in range(0, 10)]

        arbitrary.grant(subrole, midroles[0])
        arbitrary.grant(midroles[-1], superrole1)

        # Link up all roles in the list that are adjacent
        for midsubrole, midsuperrole in zip(midroles[:-1], midroles[1:]):
            arbitrary.grant(from_role=midsubrole, to_role=midsuperrole)

        self.assertTrue(subrole.instantiate({}).has_privilege(superrole1.instantiate({})))
        self.assertFalse(subrole.instantiate({}).has_privilege(superrole2.instantiate({})))

    def test_has_permission_immediate_params(self):
        subrole = arbitrary.role()
        superrole1 = arbitrary.role(parameters=set(['one']))
        arbitrary.grant(to_role=superrole1, from_role=subrole, assignment=dict(one='foo'))

        self.assertTrue(subrole.instantiate({}).has_privilege(superrole1.instantiate(dict(one='foo'))))
        self.assertFalse(subrole.instantiate({}).has_privilege(superrole1.instantiate(dict(one='baz'))))

    def test_unsaved_role_does_not_have_permission(self):
        role1 = Role()
        role2 = arbitrary.role()
        self.assertFalse(role1.has_privilege(role2))
        self.assertFalse(role2.has_privilege(role1))


class TestGrant(TestCase):

    def test_instantiated_to_role_smoke_test(self):
        """
        Basic smoke test:
        1. grant.instantiated_role({})[param] == grant.assignment[param] if param is free for the role
        2. grant.instantiated_role({})[param] does not exist if param is not free for the role
        """

        parameters = ['one']

        superrole = arbitrary.role(parameters=parameters)
        grant = arbitrary.grant(to_role=superrole, assignment={'one': 'hello'})
        self.assertEqual(grant.instantiated_to_role({}).assignment, {'one': 'hello'})

        grant = arbitrary.grant(to_role=superrole, assignment={'two': 'goodbye'})
        self.assertEqual(grant.instantiated_to_role({}).assignment, {})


class TestUserRole(TestCase):

    def setUp(self):
        Role.get_cache().clear()

    def test_user_role_integration(self):
        """
        Basic smoke test of integration of PRBAC with django.contrib.auth
        """
        user = arbitrary.user()
        role = arbitrary.role()
        priv = arbitrary.role()
        arbitrary.grant(from_role=role, to_role=priv)
        user_role = arbitrary.user_role(user=user, role=role)

        self.assertEqual(user.prbac_role, user_role)
        self.assertTrue(user.prbac_role.has_privilege(role))
        self.assertTrue(user.prbac_role.has_privilege(priv))

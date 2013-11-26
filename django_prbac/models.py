# Use modern Python
from __future__ import unicode_literals, absolute_import, print_function

# Standard Library Imports

# Django imports
from django.db import models

# External Library imports
import json_field

# Local imports
from django_prbac.fields import StringListField, StringSetField


__all__ = [
    'Role',
    'Grant',
    'RoleInstance',
]

class ValidatingModel(object):
    def save(self, force_insert=False, force_update=False, **kwargs):
        if not (force_insert or force_update):
            self.full_clean() # Will raise ValidationError if needed
        super(ValidatingModel, self).save(force_insert, force_update, **kwargs)

class Role(ValidatingModel, models.Model):
    """
    A PRBAC role, aka a Role parameterized by a set of named variables. Roles
    also model privileges:  They differ only in that privileges only refer
    to real-world consequences when all parameters are instantiated.
    """


    # Databaes fields
    # ---------------

    slug = models.CharField(
        max_length=256,
        help_text='The formal slug for this role, which should be unique',
        unique=True,
    )

    name = models.CharField(
        max_length=256,
        help_text='The friendly name for this role to present to users; this need not be unique.',
    )

    description = models.TextField(
        help_text='A long-form description of the intended semantics of this role.',
        blank=True,
        default='',
    )

    parameters = StringSetField(
        help_text='A set of strings which are the parameters for this role. Entered as a JSON list.',
        blank=True,
        default=[],
    )


    # Methods
    # -------


    def instantiate(self, assignment):
        """
        An instantiation of this role with some parameters fixed via the provided assignments.
        """
        filtered_assignment = dict([(key, assignment[key]) for key in self.parameters & set(assignment.keys())])
        return RoleInstance(self, filtered_assignment)


    def has_privilege(self, privilege):
        """
        Shortcut for checking privileges easily for roles with no params (aka probably users)
        """

        return self.instantiate({}).has_privilege(privilege)

    @property
    def assignment(self):
        """
        A Role stored in the database always has an empty assignment.
        """

        return {}

    def __repr__(self):
        return 'Role(%r, parameters=%r)' % (self.slug, self.parameters)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.slug)


class Grant(ValidatingModel, models.Model):
    """
    A parameterized membership between a sub-role and super-role.
    The parameters applied to the super-role are all those.
    """


    # Database Fields
    # ---------------

    from_role = models.ForeignKey(
        'Role',
        help_text='The sub-role begin granted membership or permission',
        related_name='memberships_granted',
    )

    to_role = models.ForeignKey(
        'Role',
        help_text='The super-role or permission being given',
        related_name='members',
    )

    assignment = json_field.JSONField(
        help_text='Assignment from parameters (strings) to values (any JSON-compatible value)',
        blank=True,
        default={},
    )


    # Methods
    # -------

    def instantiated_to_role(self, assignment):
        """
        Returns the super-role instantiated with the parameters of the membership
        composed with the `parameters` passed in.
        """
        filtered_assignment = dict([(key, assignment[key]) for key in self.to_role.parameters & set(assignment.keys())])
        composed_assignment = {}
        composed_assignment.update(filtered_assignment)
        composed_assignment.update(self.assignment)
        return self.to_role.instantiate(composed_assignment)

    def __repr__(self):
        return 'Grant(from_role=%r, to_role=%r, assignment=%r)' % (self.from_role, self.to_role, self.assignment)

class RoleInstance(object):
    """
    A parameterized role along with some parameters that are fixed. Note that this is
    not a model but only a transient Python object.
    """


    def __init__(self, role, assignment):
        self.role = role
        self.assignment = assignment
        self.slug = self.role.slug
        self.name = self.role.name
        self.parameters = self.role.parameters - set(self.assignment.keys())


    def instantiate(self, assignment):
        """
        This role further instantiated with the additional assignment.
        Note that any parameters that are already fixed are not actually
        available for being assigned, so will _not_ change.
        """
        filtered_assignment = dict([(key, assignment[key]) for key in self.parameters & set(assignment.keys())])
        composed_assignment = {}
        composed_assignment.update(filtered_assignment)
        composed_assignment.update(self.assignment)
        return RoleInstance(composed_assignment)


    def has_privilege(self, privilege):
        """
        True if this instantiated role is allowed the privilege passed in,
        (which is itself an RoleInstance)
        """

        if self == privilege:
            return True

        for membership in self.role.memberships_granted.all():
            if membership.instantiated_to_role(self.assignment).has_privilege(privilege):
                return True

        return False


    def __eq__(self, other):
        return self.slug == other.slug and self.assignment == other.assignment


    def __repr__(self):
        return 'RoleInstance(%r, parameters=%r, assignment=%r)' % (self.slug, self.parameters, self.assignment)

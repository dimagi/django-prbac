import time
import weakref

from django import VERSION
from django.db import models
from django.conf import settings
if VERSION[0] < 3:
    from django.utils.encoding import python_2_unicode_compatible
else:
    def python_2_unicode_compatible(fn):
        return fn

import jsonfield

from django_prbac.fields import StringSetField


__all__ = [
    'Role',
    'Grant',
    'RoleInstance',
    'UserRole',
]


class ValidatingModel(object):
    def save(self, force_insert=False, force_update=False, **kwargs):
        if not (force_insert or force_update):
            self.full_clean()   # Will raise ValidationError if needed
        super(ValidatingModel, self).save(force_insert, force_update, **kwargs)


@python_2_unicode_compatible
class Role(ValidatingModel, models.Model):
    """
    A PRBAC role, aka a Role parameterized by a set of named variables. Roles
    also model privileges:  They differ only in that privileges only refer
    to real-world consequences when all parameters are instantiated.
    """

    PRIVILEGES_BY_SLUG = "DJANGO_PRBAC_PRIVELEGES"
    ROLES_BY_ID = "DJANGO_PRBAC_ROLES"
    _default_instance = lambda s:None

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
        default=set,
    )

    class Meta:
        app_label = 'django_prbac'

    # Methods
    # -------

    @classmethod
    def get_cache(cls):
        try:
            cache = cls.cache
        except AttributeError:
            timeout = getattr(settings, 'DJANGO_PRBAC_CACHE_TIMEOUT', 60)
            cache = cls.cache = DictCache(timeout)
        return cache

    @classmethod
    def update_cache(cls):
        roles = cls.objects.prefetch_related('memberships_granted').all()
        roles = {role.id: role for role in roles}
        for role in roles.values():
            role._granted_privileges = privileges = []
            # Prevent extra queries by manually linking grants and roles
            # because Django 1.6 isn't smart enough to do this for us
            for membership in role.memberships_granted.all():
                membership.to_role = roles[membership.to_role_id]
                membership.from_role = roles[membership.from_role_id]
                privileges.append(membership.instantiated_to_role({}))
        cache = cls.get_cache()
        cache.set(cls.ROLES_BY_ID, roles)
        cache.set(cls.PRIVILEGES_BY_SLUG,
            {role.slug: role.instantiate({}) for role in roles.values()})

    @classmethod
    def get_privilege(cls, slug, assignment=None):
        """
        Optimized lookup of privilege by slug

        This optimization is specifically geared toward cases where
        `assignments` is empty.
        """
        cache = cls.get_cache()
        if cache.disabled:
            roles = Role.objects.filter(slug=slug)
            if roles:
                return roles[0].instantiate(assignment or {})
            return None
        privileges = cache.get(cls.PRIVILEGES_BY_SLUG)
        if privileges is None:
            cls.update_cache()
            privileges = cache.get(cls.PRIVILEGES_BY_SLUG)
        privilege = privileges.get(slug)
        if privilege is None:
            return None
        if assignment:
            return privilege.role.instantiate(assignment)
        return privilege

    def get_cached_role(self):
        """
        Optimized lookup of role by id
        """
        cache = self.get_cache()
        if cache.disabled:
            return self
        roles = cache.get(self.ROLES_BY_ID)
        if roles is None or self.id not in roles:
            self.update_cache()
            roles = cache.get(self.ROLES_BY_ID)
        return roles.get(self.id, self)

    def get_privileges(self, assignment):
        if not assignment:
            try:
                return self._granted_privileges
            except AttributeError:
                pass
        return [membership.instantiated_to_role(assignment)
                for membership in self.memberships_granted.all()]

    def instantiate(self, assignment):
        """
        An instantiation of this role with some parameters fixed via the provided assignments.
        """
        if assignment:
            filtered_assignment = {key: assignment[key]
                for key in self.parameters & set(assignment.keys())}
        else:
            value = self._default_instance()
            if value is not None:
                return value
            filtered_assignment = assignment
        value = RoleInstance(self, filtered_assignment)
        if not filtered_assignment:
            self._default_instance = weakref.ref(value)
        return value

    def has_privilege(self, privilege):
        """
        Shortcut for checking privileges easily for roles with no params (aka probably users)
        """
        role = self.get_cached_role()
        return role.instantiate({}).has_privilege(privilege)

    @property
    def assignment(self):
        """
        A Role stored in the database always has an empty assignment.
        """
        return {}

    def __repr__(self):
        return 'Role(%r, parameters=%r)' % (self.slug, self.parameters)

    def __str__(self):
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
        on_delete=models.CASCADE,
    )

    to_role = models.ForeignKey(
        'Role',
        help_text='The super-role or permission being given',
        related_name='members',
        on_delete=models.CASCADE,
    )

    assignment = jsonfield.JSONField(
        help_text='Assignment from parameters (strings) to values (any JSON-compatible value)',
        blank=True,
        default=dict,
    )

    class Meta:
        app_label = 'django_prbac'

    # Methods
    # -------

    def instantiated_to_role(self, assignment):
        """
        Returns the super-role instantiated with the parameters of the membership
        composed with the `parameters` passed in.
        """
        composed_assignment = {}
        if assignment:
            for key in self.to_role.parameters & set(assignment.keys()):
                composed_assignment[key] = assignment[key]
        if self.assignment:
            composed_assignment.update(self.assignment)
        return self.to_role.instantiate(composed_assignment)

    def __repr__(self):
        return 'Grant(from_role=%r, to_role=%r, assignment=%r)' % (self.from_role, self.to_role, self.assignment)


class UserRole(ValidatingModel, models.Model):
    """
    A link between a django.contrib.auth.models.User and
    a django_prbac.models.Role. They are kept to
    one-to-one fields to make their use extremely simple:

    request.user.prbac_role.has_privilege(...)
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='prbac_role', on_delete=models.CASCADE)
    role = models.OneToOneField(Role, related_name='user_role', on_delete=models.CASCADE)

    class Meta:
        app_label = 'django_prbac'

    def has_privilege(self, privilege):
        return self.role.has_privilege(privilege)

    def __eq__(self, other):
        return self.user == other.user and self.role == other.role

    def __repr__(self):
        return 'UserRole(user=%r, role=%r)' % (self.user, self.role)


class RoleInstance(object):
    """
    A parameterized role along with some parameters that are fixed. Note that this is
    not a model but only a transient Python object.
    """

    def __init__(self, role, assignment):
        self.role = role
        self.assignment = assignment
        self.slug = role.slug
        self.name = role.name
        self.parameters = role.parameters - set(assignment.keys())

    def instantiate(self, assignment):
        """
        This role further instantiated with the additional assignment.
        Note that any parameters that are already fixed are not actually
        available for being assigned, so will _not_ change.
        """
        composed_assignment = {}
        if assignment:
            for key in self.parameters & set(assignment.keys()):
                composed_assignment[key] = assignment[key]
        if self.assignment:
            composed_assignment.update(self.assignment)
        # this seems like a bug (wrong arguments). is this method ever called?
        return RoleInstance(composed_assignment)

    def has_privilege(self, privilege):
        """
        True if this instantiated role is allowed the privilege passed in,
        (which is itself an RoleInstance)
        """

        if self == privilege:
            return True

        return any(p.has_privilege(privilege)
                   for p in self.role.get_privileges(self.assignment))

    def __eq__(self, other):
        return self.slug == other.slug and self.assignment == other.assignment

    def __repr__(self):
        return 'RoleInstance(%r, parameters=%r, assignment=%r)' % (self.slug, self.parameters, self.assignment)


class DictCache(object):
    """A simple in-memory dict cache

    :param timeout: Number of seconds until an item in the cache expires.
    """

    def __init__(self, timeout=60):
        self.timeout = timeout
        self.data = {}

    @property
    def disabled(self):
        return self.timeout == 0

    def get(self, key, default=None):
        now = time.time()
        value, expires = self.data.get(key, (default, now))
        if now > expires:
            self.data.pop(key)
            return default
        return value

    def set(self, key, value):
        self.data[key] = (value, time.time() + self.timeout)

    def clear(self):
        self.data.clear()

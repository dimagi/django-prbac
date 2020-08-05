import uuid
from random import choice

from django.contrib.auth.models import User

from django_prbac.models import *

__all__ = [
    'role',
    'grant',
    'unique_name',
]


def instantiate(generator_or_value):
    """
    Dynamic typing hack to try to call generators if provided,
    otherwise return the value directly if not callable. This will
    break badly if used for values that can be callable.
    """

    if callable(generator_or_value):
        return generator_or_value()
    else:
        return generator_or_value


def arbitrary_slug():
    return choice(['foo', 'bar', 'baz', 'zizzle', 'zazzle'])


def arbitrary_unique_slug(prefix=None, suffix=None):
    prefix = instantiate(prefix or '')
    suffix = instantiate(suffix or '')
    return prefix + arbitrary_slug() + uuid.uuid4().hex + suffix


def arbitrary_user(username=None, password=None, email=None, save=True, **kwargs):
    username = instantiate(username or arbitrary_unique_slug)[:74]
    password = instantiate(password or arbitrary_unique_slug)[:74]
    email = instantiate(email) if email is not None else ('%s@%s.com' % (arbitrary_unique_slug(), arbitrary_unique_slug()))[:74]

    user = User(username=username,
                password=password,
                email=email,
                **kwargs)

    if save:
        user.save()

    return user


def arbitrary_role(slug=None, name=None, save=True, **kwargs):
    slug = instantiate(slug or arbitrary_unique_slug)
    name = instantiate(name or arbitrary_slug)

    role = Role(
        slug=slug,
        name=name,
        **kwargs
    )

    if save:
        role.save()

    return role


def arbitrary_grant(from_role=None, to_role=None, save=True, **kwargs):
    from_role = instantiate(from_role if from_role is not None else arbitrary_role)
    to_role = instantiate(to_role if to_role is not None else arbitrary_role)

    grant = Grant(
        from_role=from_role,
        to_role=to_role,
        **kwargs
    )

    if save:
        grant.save()

    return grant


def arbitrary_user_role(user=None, role=None, save=True, **kwargs):
    user = instantiate(user or arbitrary_user)
    role = instantiate(role or arbitrary_role)

    user_role = UserRole(user=user,
                         role=role,
                         **kwargs)

    if save:
        user_role.save()

    return user_role


role = arbitrary_role
grant = arbitrary_grant
unique_slug = arbitrary_unique_slug
user = arbitrary_user
user_role = arbitrary_user_role

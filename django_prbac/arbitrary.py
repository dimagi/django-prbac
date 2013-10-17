# Use modern Python
from __future__ import unicode_literals, absolute_import, print_function

# Standard Library Imports
from random import choice
import uuid

# Local Imports
from django_prbac.models import *

__all__ = [
    'role',
    'grant',
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

def arbitrary_name():
    return choice(['foo', 'bar', 'baz', 'zizzle', 'zazzle'])


def arbitrary_unique_name():
    return arbitrary_name() + '-' + uuid.uuid4().hex


def arbitrary_role(name=None, friendly_name=None, save=True, **kwargs):
    name = instantiate(name or arbitrary_unique_name)
    friendly_name = instantiate(friendly_name or arbitrary_name)

    role = Role(
        name=name,
        friendly_name=friendly_name,
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

role = arbitrary_role
grant = arbitrary_grant

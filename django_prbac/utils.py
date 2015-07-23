# Use modern Python
from __future__ import unicode_literals, absolute_import, print_function
import warnings

# Local Imports
from django_prbac.exceptions import PermissionDenied
from django_prbac.models import Role, UserRole


def has_privilege(request, slug, **assignment):
    """
    Returns true if the request has the privilege specified by slug,
    otherwise false
    """
    if not hasattr(request, 'role'):
        return False

    privilege = Role.get_privilege(slug, assignment)
    if privilege is None:
        return False

    if request.role.has_privilege(privilege):
        return True

    if not hasattr(request, 'user') or not hasattr(request.user, 'prbac_role'):
        return False
    try:
        request.user.prbac_role
    except UserRole.DoesNotExist:
        return False

    return request.user.prbac_role.has_privilege(privilege)


def ensure_request_has_privilege(request, slug, **assignment):
    """
    DEPRECATED
    """
    warnings.warn(
        '`ensure_request_has_privilege` is deprecated. You likely want '
        '`has_permission` or one of the `requires_privilege` decorators',
        DeprecationWarning
    )
    if not has_privilege(request, slug, **assignment):
        raise PermissionDenied()

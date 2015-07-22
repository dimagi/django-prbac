# Use modern Python
from __future__ import unicode_literals, absolute_import, print_function

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

    roles = Role.objects.filter(slug=slug)
    if not roles:
        return False

    privilege = roles[0].instantiate(assignment)
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

    You most likely want `has_permission` or one of the
    `requires_privilege` decorators.
    """
    if not has_privilege(request, slug, **assignment):
        raise PermissionDenied()

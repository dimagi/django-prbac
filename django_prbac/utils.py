import warnings

from django_prbac.exceptions import PermissionDenied
from django_prbac.models import Role, UserRole


def has_privilege(request, slug, **assignment):
    """
    Returns true if the request has the privilege specified by slug,
    otherwise false
    """
    privilege = Role.get_privilege(slug, assignment)
    if privilege is None:
        return False

    if hasattr(request, 'role'):
        if request.role.has_privilege(privilege):
            return True

    if hasattr(request, 'user') and hasattr(request.user, 'prbac_role'):
        try:
            request.user.prbac_role
        except UserRole.DoesNotExist:
            return False
        return request.user.prbac_role.has_privilege(privilege)

    return False


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

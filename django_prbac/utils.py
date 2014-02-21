# Use modern Python
from __future__ import unicode_literals, absolute_import, print_function

# Local Imports
from django_prbac.exceptions import PermissionDenied
from django_prbac.models import Role, UserRole


def ensure_request_has_privilege(request, slug, **assignment):
    """
    Ensures that an HttpRequest object has the privilege specified by slug.
    If it does not, it throws a PermissionDenied Exception.
    """
    if not hasattr(request, 'role'):
        raise PermissionDenied()

    roles = Role.objects.filter(slug=slug)
    if not roles:
        raise PermissionDenied()

    privilege = roles[0].instantiate(assignment)
    if request.role.has_privilege(privilege):
        return

    if not hasattr(request, 'user') or not hasattr(request.user, 'prbac_role'):
        raise PermissionDenied()

    try:
        request.user.prbac_role
    except UserRole.DoesNotExist:
        raise PermissionDenied()

    if not request.user.prbac_role.has_privilege(privilege):
        raise PermissionDenied()

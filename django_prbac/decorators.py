# Use modern Python
from __future__ import unicode_literals, absolute_import, print_function

# Local Imports
from django.http import Http404
from django_prbac.exceptions import PermissionDenied
from django_prbac.models import Role, UserRole


def requires_privilege(slug, **assignment):
    def decorate(fn):
        """
        Returns a function equivalent to `fn` but that requires
        a role with slug `slug` to be reachable from `request.role`
        or `request.user.prbac_role`
        with the parameters specified in `assignment`
        (in a parameterized fashion)
        """
        def wrapped(request, *args, **kwargs):

            if not hasattr(request, 'role'):
                raise PermissionDenied()

            roles = Role.objects.filter(slug=slug)
            if not roles:
                raise PermissionDenied()

            privilege = roles[0].instantiate(assignment)
            if request.role.has_privilege(privilege):
                return fn(request, *args, **kwargs)

            if not hasattr(request, 'user'):
                raise PermissionDenied()

            try:
                request.user.prbac_role
            except UserRole.DoesNotExist:
                raise PermissionDenied()

            if not request.user.prbac_role.has_privilege(privilege):
                raise PermissionDenied()

            return fn(request, *args, **kwargs)

        return wrapped

    return decorate


def requires_privilege_raise404(slug, **assignment):
    """
    A version of the requires_privilege decorator which raises an Http404
    if PermissionDenied is raised.
    """
    def decorate(fn):
        def wrapped(request, *args, **kwargs):
            try:
                return requires_privilege(slug, **assignment)(fn)(request, *args, **kwargs)
            except PermissionDenied:
                raise Http404()
        return wrapped
    return decorate

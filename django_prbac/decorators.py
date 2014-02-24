# Use modern Python
from __future__ import unicode_literals, absolute_import, print_function

# Local Imports
from django.http import Http404
from django_prbac.exceptions import PermissionDenied
from django_prbac.utils import ensure_request_has_privilege


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
            ensure_request_has_privilege(request, slug, **assignment)
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

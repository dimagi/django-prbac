from functools import wraps

from django.http import Http404
from django_prbac.exceptions import PermissionDenied
from django_prbac.utils import has_privilege


def requires_privilege(slug, **assignment):
    def decorate(fn):
        """
        Returns a function equivalent to `fn` but that requires
        a role with slug `slug` to be reachable from `request.role`
        or `request.user.prbac_role`
        with the parameters specified in `assignment`
        (in a parameterized fashion)
        """
        @wraps(fn)
        def wrapped(request, *args, **kwargs):
            if not has_privilege(request, slug, **assignment):
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
        @wraps(fn)
        def wrapped(request, *args, **kwargs):
            if not has_privilege(request, slug, **assignment):
                raise Http404()
            return fn(request, *args, **kwargs)
        return wrapped
    return decorate

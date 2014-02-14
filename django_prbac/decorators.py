# Use modern Python
from __future__ import unicode_literals, absolute_import, print_function

# Local Imports
from django.http import Http404
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
                raise Http404()

            roles = Role.objects.filter(slug=slug)
            if not roles:
                raise Http404()

            privilege = roles[0].instantiate(assignment)
            if request.role.has_privilege(privilege):
                return fn(request, *args, **kwargs)

            try:
                request.user.prbac_role
            except UserRole.DoesNotExist:
                raise Http404()

            if not request.user.prbac_role.has_privilege(privilege):
                raise Http404()

            return fn(request, *args, **kwargs)

        return wrapped

    return decorate

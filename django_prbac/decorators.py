# Use modern Python
from __future__ import unicode_literals, absolute_import, print_function

# Local Imports
from django_prbac.exceptions import PermissionDenied
from django_prbac.models import Role

def requires_privilege(role_name, **assignment):
    def decorate(fn):
        """
        Returns a function equivalent to `fn` but that requires
        a role with name `role_name` to be reachable from `request.role`
        with the parameters specified in `assignment`
        (in a parameterizes fashion)
        """
        def wrapped(request, *args, **kwargs):

            if not hasattr(request, 'role'):
                raise PermissionDenied()

            roles = Role.objects.filter(name=role_name)
            if not roles:
                raise PermissionDenied()

            privilege = roles[0].instantiate(assignment)
            if not request.role.has_privilege(privilege):
                raise PermissionDenied()

            return fn(request, *args, **kwargs)

        return wrapped

    return decorate


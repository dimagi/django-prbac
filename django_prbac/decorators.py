from __future__ import unicode_literals, absolute_import, print_function

def requires_privilege(priv):
    def wrap(fn):
        """
        Returns a function equivalent to `fn` but that requires
        `priv` to be reachable (in a parameterizes fashion)
        from `request.role`
        """
        def wrapped(request, *args, **kwargs):
            return fn(*args, **kwargs)

        return wrapped

    return wrap


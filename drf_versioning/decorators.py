from functools import wraps

from django.http import Http404

from drf_versioning.version import Version


def versioned_view(original_func=None, introduced_in: Version = None, removed_in: Version = None):
    if introduced_in is None and removed_in is None:
        raise ValueError("You need to pass either introduced_in or removed_in")

    def decorate(function):
        @wraps(function)
        def wrapper(viewset, request, *args, **kwargs):
            if introduced_in and request.version < introduced_in:
                raise Http404()
            if removed_in and request.version >= removed_in:
                raise Http404()
            output = function(viewset, request, *args, **kwargs)
            return output

        return wrapper

    return decorate(original_func) if original_func else decorate

from functools import wraps

from django.http import Http404

from drf_versioning.decorators.utils import get_min_version, get_max_version
from drf_versioning.exceptions import VersionsNotDeclaredError
from drf_versioning.versions import Version


def versioned_view(original_obj=None, introduced_in: Version = None, removed_in: Version = None):
    def decorate(obj):
        if introduced_in is None and removed_in is None:
            raise VersionsNotDeclaredError(obj)

        @wraps(obj)
        def func_wrapper(*args, **kwargs):
            # if it's a bound method which we decorated dynamically:
            # handler = versioned_view(handler, ...)
            if hasattr(obj, "__self__"):
                request = args[0]
                viewset = obj.__self__

            # if it's an unbound function we decorated statically at class definition:
            # @versioned_view(...)
            # def list(...):
            #     ...
            else:
                viewset, request = args

            viewset_introduced_in = getattr(viewset, "introduced_in", None)
            viewset_removed_in = getattr(viewset, "removed_in", None)
            min_version = get_min_version(introduced_in, viewset_introduced_in)
            max_version = get_max_version(removed_in, viewset_removed_in)
            if min_version and request.version < min_version:
                raise Http404()
            if max_version and request.version >= max_version:
                raise Http404()
            output = obj(*args, **kwargs)
            return output

        if introduced_in:
            introduced_in.view_methods_introduced.append(func_wrapper)

        if removed_in:
            removed_in.view_methods_removed.append(func_wrapper)

        return func_wrapper

    return decorate(original_obj) if original_obj else decorate

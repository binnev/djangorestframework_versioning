from functools import wraps

from django.http import Http404

from drf_versioning.decorators.utils import get_min_version, get_max_version
from drf_versioning.version import Version


def versioned_view(original_obj=None, introduced_in: Version = None, removed_in: Version = None):
    if introduced_in is None and removed_in is None:
        raise ValueError("You need to pass either introduced_in or removed_in")

    def decorate(obj):
        @wraps(obj)
        def func_wrapper(viewset, request, *args, **kwargs):
            viewset_introduced_in = getattr(viewset, "introduced_in", None)
            viewset_removed_in = getattr(viewset, "removed_in", None)
            min_version = get_min_version(introduced_in, viewset_introduced_in)
            max_version = get_max_version(removed_in, viewset_removed_in)
            if request.version < min_version or request.version >= max_version:
                raise Http404()
            output = obj(viewset, request, *args, **kwargs)
            return output

        return func_wrapper

    return decorate(original_obj) if original_obj else decorate

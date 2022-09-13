import abc
from inspect import isabstract
from typing import Optional

from rest_framework import viewsets, mixins, decorators
from rest_framework.response import Response

from .decorators import versioned_view
from .exceptions import VersionsNotDeclaredError
from .settings import versioning_settings
from .version import Version
from .version.serializers import VersionSerializer


class VersionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = VersionSerializer
    queryset = versioning_settings.VERSION_LIST

    @decorators.action(methods=["GET"], detail=False)
    def my_version(self, request, *args, **kwargs):
        version = Version.get(request.version)
        return Response(data=self.get_serializer(instance=version).data, status=200)


class VersionedViewSetMeta(type):
    """Detect if the introduced_in / removed_in class attributes have been set on a
    VersionedViewSet subclass, and register it with the Version instance if necessary."""

    def __new__(cls, name, bases, dct):
        subclass = super().__new__(cls, name, bases, dct)
        introduced_in_version = getattr(subclass, "introduced_in", None)
        removed_in_version = getattr(subclass, "removed_in", None)

        # Check that all subclasses of VersionedViewSet (but not VersionedViewSet itself) declare
        # introduced_in and/or removed_in. This is a bit janky because a subclass named
        # VersionedViewSet could bypass this check, but 1) that's an unlikely edge case and 2) I
        # don't have a better solution right now.
        if name != "VersionedViewSet" and not (introduced_in_version or removed_in_version):
            raise VersionsNotDeclaredError(subclass.__name__)

        # if introduced_in and/or removed_in are declared, add the reverse relationship on the
        # Version instance.
        if removed_in_version:
            removed_in_version.viewsets_removed.append(subclass)
        if introduced_in_version:
            introduced_in_version.viewsets_introduced.append(subclass)
        return subclass


class VersionedViewSet(viewsets.GenericViewSet, metaclass=VersionedViewSetMeta):
    introduced_in: Optional[Version] = None
    removed_in: Optional[Version] = None

    def dispatch(self, request, *args, **kwargs):
        request_method = request.method.lower()
        if request_method in self.http_method_names:
            handler = getattr(self, request_method, self.http_method_not_allowed)
            handler = versioned_view(
                handler, introduced_in=self.introduced_in, removed_in=self.removed_in
            )
            setattr(self, request_method, handler)
        return super().dispatch(request, *args, **kwargs)

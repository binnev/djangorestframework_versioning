from typing import Optional

from rest_framework import viewsets, mixins, decorators
from rest_framework.response import Response

from .decorators import versioned_view
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


class VersionedViewSet(viewsets.GenericViewSet):
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

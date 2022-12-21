from rest_framework import viewsets, mixins, decorators
from rest_framework.response import Response

from ..settings import versioning_settings
from ..versions import Version
from ..versions.serializers import VersionSerializer


class VersionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Serializes all the Versions in the VERSION_LIST."""

    serializer_class = VersionSerializer
    queryset = tuple(sorted(versioning_settings.VERSION_LIST, reverse=True))

    @decorators.action(methods=["GET"], detail=False)
    def my_version(self, request, *args, **kwargs):
        version = Version.get(request.version)
        return Response(data=self.get_serializer(instance=version).data, status=200)

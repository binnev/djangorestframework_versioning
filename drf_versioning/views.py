from rest_framework import viewsets, mixins, decorators
from rest_framework.response import Response

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

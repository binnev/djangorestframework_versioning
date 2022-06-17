from rest_framework import viewsets, mixins, decorators
from rest_framework.response import Response

from src.drf_versioning.version import Version
from src.drf_versioning.version.serializers import VersionSerializer


class VersionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = VersionSerializer

    def get_queryset(self):
        return Version.list()

    @decorators.action(methods=["GET"], detail=False)
    def my_version(self, request, *args, **kwargs):
        version = request.version
        return Response(data=self.get_serializer(instance=version).data, status=200)

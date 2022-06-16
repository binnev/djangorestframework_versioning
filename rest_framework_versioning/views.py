from rest_framework import viewsets, mixins, decorators
from rest_framework.response import Response

from .version.serializers import VersionSerializer


class VersionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = VersionSerializer

    def get_queryset(self):
        raise NotImplementedError(
            "You need to subclass this viewset and provide a get_queryset method"
        )

    @decorators.action(methods=["GET"], detail=False)
    def my_version(self, request, *args, **kwargs):
        version = request.version
        return Response(data=self.get_serializer(instance=version).data, status=200)

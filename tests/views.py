from typing import Optional

from rest_framework import viewsets, decorators
from rest_framework.response import Response

from drf_versioning.decorators import versioned_view
from drf_versioning.version import Version
from tests import versions
from tests.models import Thing
from tests.serializers import ThingSerializer


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


class ThingViewSet(
    VersionedViewSet,
    viewsets.ModelViewSet,
):
    serializer_class = ThingSerializer
    queryset = Thing.objects.all()
    introduced_in = versions.VERSION_1_0_0
    removed_in = versions.VERSION_2_2_0

    @versioned_view(introduced_in=versions.VERSION_2_0_0)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @versioned_view(removed_in=versions.VERSION_2_1_0)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @versioned_view(introduced_in=versions.VERSION_2_1_0)
    @decorators.action(methods=["GET"], detail=True)
    def get_name(self, request, *args, **kwargs):
        obj = self.get_object()
        return Response(data={"name": obj.name})

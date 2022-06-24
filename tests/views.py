from rest_framework import viewsets

from tests.models import Thing
from tests.serializers import ThingSerializer


class ThingViewSet(viewsets.ModelViewSet):
    serializer_class = ThingSerializer
    queryset = Thing.objects.all()

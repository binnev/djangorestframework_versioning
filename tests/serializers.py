from rest_framework import serializers

from drf_versioning.transform.serializers import VersioningSerializer
from tests.models import Thing


class ThingSerializer(VersioningSerializer, serializers.ModelSerializer):
    transform_base = "tests.transforms.ThingTransform"

    class Meta:
        model = Thing
        fields = [
            "id",
            "name",
            "number",
        ]

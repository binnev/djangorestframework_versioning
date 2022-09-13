from rest_framework import serializers

from drf_versioning.transform.serializers import VersioningSerializer, import_transforms
from tests.models import Thing


class ThingSerializer(VersioningSerializer, serializers.ModelSerializer):
    transforms = import_transforms("tests.transforms")

    class Meta:
        model = Thing
        fields = [
            "id",
            "name",
            "number",
            "status",
        ]

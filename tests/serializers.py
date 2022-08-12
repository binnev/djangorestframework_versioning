from rest_framework import serializers

from drf_versioning.transform.serializers import VersioningSerializer, import_transforms
from tests.models import Thing


class ThingSerializer(VersioningSerializer, serializers.ModelSerializer):
    transforms = import_transforms("tests.transforms")
    # todo: now just get a metaclass to do this
    # todo: metaclass to also check transform_base is declared

    class Meta:
        model = Thing
        fields = [
            "id",
            "name",
            "number",
        ]

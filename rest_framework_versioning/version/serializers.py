from rest_framework import serializers

from . import Version


class VersionSerializer(serializers.Serializer):
    version = serializers.CharField(source="base_version")
    notes = serializers.ListField()

    def to_representation(self, instance: Version):
        data = super().to_representation(instance)
        data["notes"] += [transform.description for transform in instance.transforms]
        return data

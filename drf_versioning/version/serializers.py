from rest_framework import serializers


class TransformSerializer(serializers.Serializer):
    description = serializers.CharField(source="*")


class AddViewSetActionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return f"Introduced {instance}"


class RemoveViewSetActionSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return f"Removed {instance}"


class ViewMethodSerializer(serializers.Serializer):
    viewsets_introduced = AddViewSetActionSerializer(many=True)
    viewsets_removed = RemoveViewSetActionSerializer(many=True)
    view_methods_introduced = AddViewSetActionSerializer(many=True)
    view_methods_removed = RemoveViewSetActionSerializer(many=True)


class VersionSerializer(serializers.Serializer):
    version = serializers.CharField(source="base_version")
    notes = serializers.ListField()
    transforms = TransformSerializer(many=True)
    views = ViewMethodSerializer(source="*")

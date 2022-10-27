import re

from rest_framework import serializers

from drf_versioning.transforms import Transform

"""
This is how I'd want the serialized Versions to look:
[
    {
        "version": "1.0.0",
        "views": [
            "Introduced /thing/ endpoint with actions:
                create:     POST /thing/
                retrieve:   GET /thing/{id}/"
        ]
    },
    {
        "version": "2.0.0",
        "views": [
            "Introduced /thing/ actions:
                list:   GET /thing/"
        ]
    },
    {
        "version": "2.1.0",
        "views": [
            "Introduced /thing/ actions:
                get_name:   GET /thing/{id}/get_name"
        ]
    },
]
"""


class TransformSerializer(serializers.Serializer):
    def to_representation(self, obj: Transform):
        return obj.description


class ViewSetMethodSerializer(serializers.Serializer):
    def to_representation(self, obj):
        match = re.match("<function (.*) at (.*)>", str(obj))
        method_name, _ = match.groups()
        return method_name


class ViewSetSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return obj.__name__


class ViewMethodSerializer(serializers.Serializer):
    endpoints_introduced = ViewSetSerializer(source="viewsets_introduced", many=True)
    endpoints_removed = ViewSetSerializer(source="viewsets_removed", many=True)
    actions_introduced = ViewSetMethodSerializer(source="view_methods_introduced", many=True)
    actions_removed = ViewSetMethodSerializer(source="view_methods_removed", many=True)


class VersionSerializer(serializers.Serializer):
    version = serializers.CharField(source="base_version")
    notes = serializers.ListField()
    models = TransformSerializer(source="transforms", many=True)
    views = ViewMethodSerializer(source="*")

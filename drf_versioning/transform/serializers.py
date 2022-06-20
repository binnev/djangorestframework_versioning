import inspect
from importlib import import_module

from django.http import QueryDict
from rest_framework import serializers

from drf_versioning.exceptions import TransformBaseNotDeclaredException
from . import Transform


def get_transform_classes(transform_base=None, base_version=1, reverse=False):
    module, base = transform_base.rsplit(".", 1)
    mod = import_module(module)

    transform_classes_dict = {}

    for name, transform_class in inspect.getmembers(mod):
        if name.startswith(base) and issubclass(transform_class, Transform):
            if base_version < transform_class.version:
                transform_classes_dict[transform_class.version.base_version] = transform_class

    ordered_transform_classes_list = [
        transform_classes_dict[key] for key in sorted(transform_classes_dict, reverse=reverse)
    ]

    return ordered_transform_classes_list


class VersioningSerializer(serializers.Serializer):
    transform_base = None

    def _check_transform_base_declared(self):
        if not self.transform_base:
            raise TransformBaseNotDeclaredException(
                "VersioningParser cannot correctly promote incoming resources with no transform classes."
            )

    def _get_request_version(self):
        request = self.context.get("request")
        if request and hasattr(request, "version"):
            return request.version

    def to_representation(self, instance):
        """
        Serializes the outgoing data as JSON and executes any available version transforms in backwards
        order against the serialized representation to convert the highest supported version into the
        requested version of the resource.
        """
        self._check_transform_base_declared()
        data = super().to_representation(instance)
        if instance:
            request = self.context.get("request")
            if request_version := self._get_request_version():
                # demote data until we've run the transform just above the requested version
                transforms = get_transform_classes(
                    self.transform_base, base_version=request_version, reverse=True
                )
                for transform in transforms:
                    data = transform().to_representation(data, request, instance)

        return data

    def to_internal_value(self, data: QueryDict):
        self._check_transform_base_declared()
        data = data.copy()  # immutable QueryDict to mutable dict
        request = self.context.get("request")
        if request_version := self._get_request_version():
            transforms = get_transform_classes(
                self.transform_base, base_version=request_version, reverse=False
            )
            for transform in transforms:
                data = transform().to_internal_value(data, request)

        return super().to_internal_value(data)

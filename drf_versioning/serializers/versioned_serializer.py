from django.http import QueryDict
from rest_framework import serializers

from ..exceptions import TransformsNotDeclaredError
from ..transforms import Transform
from ..versions import Version


class VersionedSerializer(serializers.Serializer):
    transforms: tuple[type[Transform]] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_transforms_declared()

    def check_transforms_declared(self):
        if not self.transforms:
            raise TransformsNotDeclaredError(
                f"{self.__class__.__name__} has not declared transforms."
            )

    def _get_request_version(self):
        request = self.context.get("request")
        if request and hasattr(request, "version"):
            return request.version

    def transforms_for_version(self, version: Version, reverse=False) -> list[type[Transform]]:
        return sorted(
            filter(lambda t: version < t.version, self.transforms),
            key=lambda t: t.version,
            reverse=reverse,
        )

    def to_representation(self, instance):
        """
        Serializes the outgoing data as JSON and executes any available version transforms in backwards
        order against the serialized representation to convert the highest supported version into the
        requested version of the resource.
        """
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request_version := self._get_request_version():
            # demote data until we've run the transform just above the requested version
            for transform in self.transforms_for_version(version=request_version, reverse=True):
                data = transform().to_representation(data, request, instance)

        return data

    def to_internal_value(self, data: QueryDict):
        data = data.copy()  # immutable QueryDict to mutable dict
        request = self.context.get("request")
        if request_version := self._get_request_version():
            for transform in self.transforms_for_version(version=request_version, reverse=False):
                data = transform().to_internal_value(data, request)

        return super().to_internal_value(data)

from .base import Transform


class AddField(Transform):
    field_name: str

    def to_internal_value(self, data, request):
        data.pop(self.field_name, None)
        return data

    def to_representation(self, data, request, instance):
        data.pop(self.field_name, None)
        return data


class RemoveField(Transform):
    field_name: str
    null_value = None  # the value to serialize for the removed field for old versions

    def to_internal_value(self, data, request):
        """No action required for to_internal_value because the serializer will ignore fields it
        doesn't have."""
        return data

    def to_representation(self, data, request, instance):
        data[self.field_name] = self.null_value
        return data

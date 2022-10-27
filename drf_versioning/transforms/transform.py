from ..versions import Version


class TransformMeta(type):
    """Detect the version attribute on a Transform subclass, and register the Transform with that
    version"""

    def __new__(cls, name, bases, dct):
        subclass = super().__new__(cls, name, bases, dct)
        if version := getattr(subclass, "version", None):
            version.transforms.append(subclass)
        return subclass


class Transform(metaclass=TransformMeta):
    """
    Mutates serializer data between different versions
    """

    description: str  # will be added to version.notes
    version: Version  # will be added to version.transforms

    def to_internal_value(self, data: dict, request):
        """Operation performed on incoming data from older request versions"""
        raise NotImplementedError

    def to_representation(self, data: dict, request, instance):
        """Operation performed on outgoing data in response to an older request version"""
        raise NotImplementedError

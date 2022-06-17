from src.drf_versioning.version import Version


class Transform:
    """
    Mutates serializer data between different versions
    """

    description: str  # will be added to version.notes
    version: Version  # set by Version.__init__

    def to_internal_value(self, data, request):
        raise NotImplementedError

    def to_representation(self, data, request, instance):
        raise NotImplementedError

from ..version import Version


class Transform:
    """
    Mutates serializer data between different versions
    """

    description: str  # will be added to version.notes
    version: Version  # set by Version.__init__

    def to_internal_value(self, data, request):
        """Operation performed on incoming data from older request versions"""
        raise NotImplementedError

    def to_representation(self, data, request, instance):
        """Operation performed on outgoing data in response to an older request version"""
        raise NotImplementedError

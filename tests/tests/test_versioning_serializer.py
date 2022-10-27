import pytest

from drf_versioning.exceptions import TransformsNotDeclaredError
from drf_versioning.serializers import VersionedSerializer


def test_versioned_serializer_checks_for_transforms_at_instantiation():
    class BadSerializer(VersionedSerializer):
        pass

    with pytest.raises(TransformsNotDeclaredError) as e:
        BadSerializer()
    assert str(e.value) == "BadSerializer has not declared transforms."

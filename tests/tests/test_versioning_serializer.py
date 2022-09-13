import pytest

from drf_versioning.exceptions import TransformsNotDeclaredError
from drf_versioning.transform.serializers import VersioningSerializer


def test_versioning_serializer_checks_for_transforms_at_instantiation():
    class BadSerializer(VersioningSerializer):
        pass

    with pytest.raises(TransformsNotDeclaredError) as e:
        BadSerializer()
    assert str(e.value) == "BadSerializer has not declared transforms."

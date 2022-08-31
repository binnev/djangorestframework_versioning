import pytest

from drf_versioning.exceptions import TransformsNotDeclaredException, TransformBaseNotDeclaredException
from drf_versioning.transform import Transform
from drf_versioning.transform.serializers import VersioningSerializer


def test_versioning_serializer_checks_for_transforms_at_instantiation():
    class BadSerializer(VersioningSerializer):
        pass

    with pytest.raises(TransformsNotDeclaredException) as e:
        BadSerializer()
    assert str(e.value) == "BadSerializer has not declared transforms."


def test_versioning_serializer_checks_for_transform_base_at_instantiation():
    class BetterButBadSerializer(VersioningSerializer):
        transforms = Transform()

    with pytest.raises(TransformBaseNotDeclaredException) as e:
        BetterButBadSerializer()
    assert str(e.value) == "BetterButBadSerializer has not declared transform base."
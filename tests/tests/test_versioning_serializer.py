import pytest

from drf_versioning.exceptions import TransformBaseNotDeclaredException
from drf_versioning.transform.serializers import VersioningSerializer


def test_versioning_serializer_checks_for_transform_base():
    class BadSerializer(VersioningSerializer):
        pass

    with pytest.raises(TransformBaseNotDeclaredException) as e:
        BadSerializer().to_representation({})
    assert str(e.value) == "BadSerializer has not declared a transform_base."

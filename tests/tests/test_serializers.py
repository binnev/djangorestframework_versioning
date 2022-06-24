from dataclasses import dataclass

import pytest
from mixer.backend.django import mixer

from drf_versioning.version import Version
from tests import versions
from tests.models import Thing
from tests.serializers import ThingSerializer

pytestmark = pytest.mark.django_db


@dataclass
class MockRequest:
    version: Version


@pytest.mark.parametrize(
    "version, expected_data",
    [
        (
            versions.VERSION_1_0_0,
            dict(
                id=1,
                name="bar",
            ),
        )
    ],
)
def test_thing_serializer_to_representation(version, expected_data):
    request = MockRequest(version=version)
    thing = mixer.blend(
        Thing,
        id=1,
        name="bar",
    )
    serializer = ThingSerializer(instance=thing, context={"request": request})
    expected_data = expected_data
    assert serializer.data == expected_data


@pytest.mark.parametrize(
    "version, post_data, expected_field_values",
    [
        (
            versions.VERSION_1_0_0,
            dict(name="bar"),
            dict(name="bar"),
        )
    ],
)
def test_thing_serializer_to_internal_value(version, post_data, expected_field_values):
    request = MockRequest(version=version)
    serializer = ThingSerializer(data=post_data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    thing = serializer.save()

    for field_name, expected_value in expected_field_values.items():
        assert getattr(thing, field_name) == expected_value

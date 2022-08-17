from dataclasses import dataclass

import pytest
from mixer.backend.django import mixer

from drf_versioning.version import Version
from drf_versioning.version.serializers import VersionSerializer
from tests import versions, views, transforms
from tests.models import Thing
from tests.serializers import ThingSerializer
from tests.views import ThingViewSet

pytestmark = pytest.mark.django_db


@dataclass
class MockRequest:
    version: Version


@pytest.mark.parametrize(
    "version, expected_data",
    [
        (
            versions.VERSION_1_0_0,  # todo: should raise 404 as Thing model not introduced yet.
            dict(
                id=1,
                name="bar",
            ),
        ),
        (
            versions.VERSION_2_0_0,
            dict(
                id=1,
                name="bar",
            ),
        ),
        (
            versions.VERSION_2_1_0,
            dict(
                id=1,
                name="bar",
                number=420,
            ),
        ),
    ],
)
def test_thing_serializer_to_representation(version, expected_data):
    request = MockRequest(version=version)
    thing = mixer.blend(
        Thing,
        id=1,
        name="bar",
        number=420,
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
        ),
        (
            versions.VERSION_2_0_0,
            dict(name="bar"),
            dict(name="bar"),
        ),
        (
            versions.VERSION_2_1_0,
            dict(name="bar"),
            dict(name="bar", number=0),
        ),
        (
            versions.VERSION_2_1_0,
            dict(name="bar", number=420),
            dict(name="bar", number=420),
        ),
    ],
)
def test_thing_serializer_to_internal_value(version, post_data, expected_field_values):
    request = MockRequest(version=version)
    serializer = ThingSerializer(data=post_data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    thing = serializer.save()

    for field_name, expected_value in expected_field_values.items():
        assert getattr(thing, field_name) == expected_value


def test_version_serializer():
    v = Version("6.9")
    v.viewsets_introduced = [views.ThingViewSet]
    v.viewsets_removed = [views.OtherThingViewSet]
    v.view_methods_introduced = [views.ThingViewSet.list]
    v.view_methods_removed = [views.OtherThingViewSet.get_name]
    v.transforms = [transforms.ThingTransformAddNumber]
    data = VersionSerializer(instance=v).data
    assert data == {
        "version": "6.9",
        "notes": [],
        "models": ["Added Thing.number field."],
        "views": {
            "endpoints_introduced": ["ThingViewSet"],
            "endpoints_removed": ["OtherThingViewSet"],
            "actions_introduced": ["ThingViewSet.list"],
            "actions_removed": ["OtherThingViewSet.get_name"],
        },
    }

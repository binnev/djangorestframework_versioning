from dataclasses import dataclass

import pytest
from dateutil.parser import parse
from django.utils import timezone
from rest_framework import serializers

from drf_versioning.transform import Transform, AddField
from drf_versioning.transform.serializers import VersioningSerializer
from drf_versioning.version import Version
from drf_versioning.version.serializers import VersionSerializer
from tests import versions, views, transforms
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
        (
            versions.VERSION_2_2_0,
            dict(
                id=1,
                name="bar",
                number=420,
                status="OK",
                date_updated="2010-01-01T01:01:01Z",
            ),
        ),
    ],
)
def test_thing_serializer_to_representation(version, expected_data):
    request = MockRequest(version=version)
    thing = Thing.objects.create(
        id=1,
        name="bar",
        number=420,
        date_updated=timezone.now(),
    )
    assert thing.date_updated.year == timezone.now().year == 2010
    serializer = ThingSerializer(instance=thing, context={"request": request})
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
            dict(name="bar", number=420, status="OK"),
            dict(name="bar", number=420),
        ),
        (
            versions.VERSION_2_2_0,
            dict(name="bar", number=420, status="OK", date_updated="2022-09-02T12:00:00"),
            dict(name="bar", number=420, status="OK", date_updated=parse("2022-09-02T12:00:00Z")),
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
    v = Version("6.9", notes=["some text"])
    v.viewsets_introduced = [views.ThingViewSet]
    v.viewsets_removed = [views.OtherThingViewSet]
    v.view_methods_introduced = [views.ThingViewSet.list]
    v.view_methods_removed = [views.OtherThingViewSet.get_name]
    v.transforms = [transforms.ThingTransformAddNumber]
    data = VersionSerializer(instance=v).data
    assert data == {
        "version": "6.9",
        "notes": ["some text"],
        "models": ["Added Thing.number field."],
        "views": {
            "endpoints_introduced": ["ThingViewSet"],
            "endpoints_removed": ["OtherThingViewSet"],
            "actions_introduced": ["ThingViewSet.list"],
            "actions_removed": ["OtherThingViewSet.get_name"],
        },
    }


@pytest.mark.parametrize(
    "request_version, expected_data_parent, expected_data_child",
    [
        (
            Version("1"),
            {
                "name": "Jane",
                "child": {"name": "Billy"},
            },
            {"name": "Billy"},
        ),
        (
            None,
            {
                "name": "Jane",
                "age": 69,
                "child": {"name": "Billy", "age": 12},
            },
            {"name": "Billy", "age": 12},
        ),
        (
            Version("2"),
            {
                "name": "Jane",
                "age": 69,
                "child": {"name": "Billy", "age": 12},
            },
            {"name": "Billy", "age": 12},
        ),
        (
            Version("3"),
            {
                "name": "Jane",
                "age": 69,
                "child": {"name": "Billy", "age": 12},
            },
            {"name": "Billy", "age": 12},
        ),
    ],
)
def test_inline_serialization(request_version, expected_data_parent, expected_data_child):
    class AddAgeFieldEverywhere(AddField):
        """The 'age' field was added in v2. This transform removes it for versions < 2"""

        field_name = "age"
        version = Version("2")

    @dataclass
    class Child:
        name: str
        age: int

    @dataclass
    class Parent:
        name: str
        age: int
        child: Child

    class ChildSerializer(VersioningSerializer):
        name = serializers.CharField()
        age = serializers.IntegerField()
        transforms = [AddAgeFieldEverywhere]

    class ParentSerializer(VersioningSerializer):
        name = serializers.CharField()
        age = serializers.IntegerField()
        child = ChildSerializer()
        transforms = [AddAgeFieldEverywhere]

    child = Child(name="Billy", age=12)
    parent = Parent(name="Jane", age=69, child=child)
    request = MockRequest(version=request_version)
    assert ChildSerializer(child, context={"request": request}).data == expected_data_child
    assert ParentSerializer(parent, context={"request": request}).data == expected_data_parent


def test_inline_serialization_without_context_results_in_most_recent_data():
    class AddAgeFieldEverywhere(AddField):
        """The 'age' field was added in v2. This transform removes it for versions < 2"""

        field_name = "age"
        version = Version("2")

    @dataclass
    class Child:
        name: str
        age: int

    @dataclass
    class Parent:
        name: str
        age: int
        child: Child

    class ChildSerializer(VersioningSerializer):
        name = serializers.CharField()
        age = serializers.IntegerField()
        transforms = [AddAgeFieldEverywhere]

    class ParentSerializer(VersioningSerializer):
        name = serializers.CharField()
        age = serializers.IntegerField()
        child = ChildSerializer()
        transforms = [AddAgeFieldEverywhere]

    child = Child(name="Billy", age=12)
    parent = Parent(name="Jane", age=69, child=child)

    # passing no context should result in the most up-to-date output
    assert ChildSerializer(instance=child).data == {"name": "Billy", "age": 12}
    assert ParentSerializer(instance=parent).data == {
        "name": "Jane",
        "age": 69,
        "child": {"name": "Billy", "age": 12},
    }

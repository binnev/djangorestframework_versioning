from dataclasses import dataclass

import pytest
from dateutil.parser import parse
from django.utils import timezone
from redbreast.testing import parametrize, testparams, assert_dicts_equal
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


@dataclass
class Child:
    name: str
    age: int


@dataclass
class Parent:
    name: str
    age: int
    child: Child


class AddAge(AddField):
    """The 'age' field was added in v2. This transform removes it for versions < 2"""

    field_name = "age"
    version = Version("2")


class ChildSerializer(VersioningSerializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    transforms = [AddAge]


class ParentSerializer(VersioningSerializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    child = ChildSerializer()
    transforms = [AddAge]


@parametrize(
    param := testparams("version", "expected_data"),
    [
        param(
            version=versions.VERSION_1_0_0,
            expected_data=dict(id=1, name="bar"),
        ),
        param(
            version=versions.VERSION_2_0_0,
            expected_data=dict(id=1, name="bar"),
        ),
        param(
            version=versions.VERSION_2_1_0,
            expected_data=dict(id=1, name="bar", number=420),
        ),
        param(
            version=versions.VERSION_2_2_0,
            expected_data=dict(
                id=1, name="bar", number=420, status="OK", date_updated="2010-01-01T01:01:01Z"
            ),
        ),
    ],
)
def test_thing_serializer_to_representation(param):
    request = MockRequest(version=param.version)
    thing = Thing.objects.create(
        id=1,
        name="bar",
        number=420,
        date_updated=timezone.now(),
    )
    assert thing.date_updated.year == timezone.now().year == 2010
    serializer = ThingSerializer(instance=thing, context={"request": request})
    assert serializer.data == param.expected_data


@parametrize(
    param := testparams("version", "post_data", "expected_field_values"),
    [
        param(
            version=versions.VERSION_1_0_0,
            post_data=dict(name="bar"),
            expected_field_values=dict(name="bar"),
        ),
        param(
            version=versions.VERSION_2_0_0,
            post_data=dict(name="bar"),
            expected_field_values=dict(name="bar"),
        ),
        param(
            version=versions.VERSION_2_1_0,
            post_data=dict(name="bar"),
            expected_field_values=dict(name="bar", number=0),
        ),
        param(
            version=versions.VERSION_2_1_0,
            post_data=dict(name="bar", number=420, status="OK"),
            expected_field_values=dict(name="bar", number=420),
        ),
        param(
            version=versions.VERSION_2_2_0,
            post_data=dict(name="bar", number=420, status="OK", date_updated="2022-09-02T12:00:00"),
            expected_field_values=dict(
                name="bar", number=420, status="OK", date_updated=parse("2022-09-02T12:00:00Z")
            ),
        ),
    ],
)
def test_thing_serializer_to_internal_value(param):
    request = MockRequest(version=param.version)
    serializer = ThingSerializer(data=param.post_data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    thing = serializer.save()

    for field_name, expected_value in param.expected_field_values.items():
        assert getattr(thing, field_name) == expected_value


def test_version_serializer():
    v = Version("6.9", notes=["some text"])
    v.viewsets_introduced = [views.ThingViewSet]
    v.viewsets_removed = [views.OtherThingViewSet]
    v.view_methods_introduced = [views.ThingViewSet.list]
    v.view_methods_removed = [views.OtherThingViewSet.get_name]
    v.transforms = [transforms.ThingTransformAddNumber]
    data = VersionSerializer(instance=v).data
    assert_dicts_equal(
        data,
        {
            "version": "6.9",
            "notes": ["some text"],
            "models": ["Added Thing.number field."],
            "views": {
                "endpoints_introduced": ["ThingViewSet"],
                "endpoints_removed": ["OtherThingViewSet"],
                "actions_introduced": ["ThingViewSet.list"],
                "actions_removed": ["OtherThingViewSet.get_name"],
            },
        },
    )


@parametrize(
    param := testparams("request_version", "expected_data"),
    [
        param(
            request_version=None,
            expected_data={
                "name": "Jane",
                "age": 69,
                "child": {"name": "Billy", "age": 12},
            },
        ),
        param(
            request_version=Version("1"),
            expected_data={
                "name": "Jane",
                "child": {"name": "Billy"},
            },
        ),
        param(
            request_version=Version("2"),
            expected_data={
                "name": "Jane",
                "age": 69,
                "child": {"name": "Billy", "age": 12},
            },
        ),
        param(
            request_version=Version("3"),
            expected_data={
                "name": "Jane",
                "age": 69,
                "child": {"name": "Billy", "age": 12},
            },
        ),
    ],
)
def test_inline_serialization(param):

    child = Child(name="Billy", age=12)
    parent = Parent(name="Jane", age=69, child=child)
    request = MockRequest(version=param.request_version)
    assert ParentSerializer(parent, context={"request": request}).data == param.expected_data


@parametrize(
    param := testparams("request_version", "expected_data"),
    [
        param(
            request_version=Version("1"),
            expected_data={
                "age": 69,
                "name": "Jane",
                "child": {"name": "Billy"},
            },
        ),
        param(
            request_version=None,
            expected_data={
                "name": "Jane",
                "age": 69,
                "child": {"name": "Billy", "age": 12},
            },
        ),
        param(
            request_version=Version("2"),
            expected_data={
                "name": "Jane",
                "age": 69,
                "child": {"name": "Billy", "age": 12},
            },
        ),
        param(
            request_version=Version("3"),
            expected_data={
                "name": "Jane",
                "age": 69,
                "child": {"name": "Billy", "age": 12},
            },
        ),
    ],
)
def test_inline_serialization_when_parent_serializer_is_not_a_versioningserializer(param):
    class ParentSerializer(serializers.Serializer):
        name = serializers.CharField()
        age = serializers.IntegerField()
        child = ChildSerializer()

    child = Child(name="Billy", age=12)
    parent = Parent(name="Jane", age=69, child=child)
    request = MockRequest(version=param.request_version)
    assert ParentSerializer(parent, context={"request": request}).data == param.expected_data


@parametrize(
    param := testparams("request_version", "expected_data"),
    [
        param(
            request_version=Version("1"),
            expected_data={
                "name": "Jane",
                "children": [
                    {"name": "Jimmy"},
                    {"name": "Billy"},
                ],
            },
        ),
        param(
            request_version=None,
            expected_data={
                "name": "Jane",
                "age": 69,
                "children": [
                    {"name": "Jimmy", "age": 13},
                    {"name": "Billy", "age": 12},
                ],
            },
        ),
        param(
            request_version=Version("2"),
            expected_data={
                "name": "Jane",
                "age": 69,
                "children": [
                    {"name": "Jimmy", "age": 13},
                    {"name": "Billy", "age": 12},
                ],
            },
        ),
        param(
            request_version=Version("3"),
            expected_data={
                "name": "Jane",
                "age": 69,
                "children": [
                    {"name": "Jimmy", "age": 13},
                    {"name": "Billy", "age": 12},
                ],
            },
        ),
    ],
)
def test_inline_serialization_with_many(param):
    @dataclass
    class Parent:
        name: str
        age: int
        children: list[Child]

    class ParentSerializer(VersioningSerializer):
        name = serializers.CharField()
        age = serializers.IntegerField()
        children = ChildSerializer(many=True)
        transforms = [AddAge]

    billy = Child(name="Billy", age=12)
    jimmy = Child(name="Jimmy", age=13)
    parent = Parent(name="Jane", age=69, children=[jimmy, billy])

    request = MockRequest(version=param.request_version)
    assert ParentSerializer(parent, context={"request": request}).data == param.expected_data


def test_inline_serialization_without_context_results_in_most_recent_data():
    child = Child(name="Billy", age=12)
    parent = Parent(name="Jane", age=69, child=child)

    # passing no context should result in the most up-to-date output
    assert ParentSerializer(instance=parent).data == {
        "name": "Jane",
        "age": 69,
        "child": {"name": "Billy", "age": 12},
    }

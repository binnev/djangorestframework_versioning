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
from tests.models import Thing, Person
from tests.serializers import ThingSerializer, PersonSerializer

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
                id=1, name="bar", number=420, status="OK", date_updated="2010-01-02T03:04:05Z"
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


@parametrize(
    param := testparams("name", "request_version", "expected_output"),
    [
        param(
            name="charles",
            request_version=Version("2"),
            expected_output=dict(
                name="charles",
                father=dict(name="david"),
                mother=dict(name="ada"),
                children=[],
            ),
        ),
        param(
            name="charles",
            request_version=Version("3"),
            expected_output=dict(
                name="charles",
                birthday="1989-08-25",
                father=dict(name="david", birthday="1957-03-03"),
                mother=dict(name="ada", birthday="1960-05-23"),
                children=[],
            ),
        ),
        param(
            name="david",
            request_version=Version("2"),
            expected_output=dict(
                name="david",
                father=dict(name="tommy"),
                mother=dict(name="grace"),
                children=[
                    dict(name="charles", children=[]),
                    dict(name="john", children=[]),
                    dict(name="finn", children=[]),
                ],
            ),
        ),
        param(
            name="david",
            request_version=Version("3"),
            expected_output=dict(
                name="david",
                birthday="1957-03-03",
                father=dict(name="tommy", birthday="1920-01-01"),
                mother=dict(name="grace", birthday="1919-01-01"),
                children=[
                    dict(name="charles", birthday="1989-08-25", children=[]),
                    dict(name="john", birthday="1991-10-22", children=[]),
                    dict(name="finn", birthday="1994-06-24", children=[]),
                ],
            ),
        ),
        param(
            name="tommy",
            request_version=Version("2"),
            expected_output=dict(
                name="tommy",
                father=None,
                mother=None,
                children=[
                    dict(
                        name="david",
                        children=[
                            dict(name="charles"),
                            dict(name="john"),
                            dict(name="finn"),
                        ],
                    ),
                    dict(name="arthur", children=[]),
                    dict(name="polly", children=[]),
                ],
            ),
        ),
        param(
            name="tommy",
            request_version=Version("3"),
            expected_output=dict(
                name="tommy",
                birthday="1920-01-01",
                father=None,
                mother=None,
                children=[
                    dict(
                        name="david",
                        birthday="1957-03-03",
                        children=[
                            dict(name="charles", birthday="1989-08-25"),
                            dict(name="john", birthday="1991-10-22"),
                            dict(name="finn", birthday="1994-06-24"),
                        ],
                    ),
                    dict(name="arthur", birthday="1955-01-01", children=[]),
                    dict(name="polly", birthday="1960-01-01", children=[]),
                ],
            ),
        ),
    ],
)
@pytest.mark.django_db
def test_inline_serialization2(param):
    tommy = Person.objects.create(name="tommy", birthday="1920-01-01")
    grace = Person.objects.create(name="grace", birthday="1919-01-01")
    david = Person.objects.create(name="david", birthday="1957-03-03", father=tommy, mother=grace)
    arthur = Person.objects.create(name="arthur", birthday="1955-01-01", father=tommy, mother=grace)
    polly = Person.objects.create(name="polly", birthday="1960-01-01", father=tommy, mother=grace)
    ada = Person.objects.create(name="ada", birthday="1960-05-23")
    charles = Person.objects.create(name="charles", birthday="1989-08-25", father=david, mother=ada)
    john = Person.objects.create(name="john", birthday="1991-10-22", father=david, mother=ada)
    finn = Person.objects.create(name="finn", birthday="1994-06-24", father=david, mother=ada)

    person = Person.objects.get(name=param.name)
    request = MockRequest(version=param.request_version)
    assert_dicts_equal(
        PersonSerializer(person, context={"request": request}).data,
        param.expected_output,
    )

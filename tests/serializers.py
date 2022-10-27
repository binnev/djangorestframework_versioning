from rest_framework import serializers
from tests import transforms
from drf_versioning.transforms.serializers import VersionedSerializer, import_transforms
from tests.models import Thing, Person


class ThingSerializer(VersionedSerializer, serializers.ModelSerializer):
    transforms = [
        transforms.ThingTransformAddNumber,
        transforms.ThingAddDateUpdated,
        transforms.ThingAddStatus,
    ]

    class Meta:
        model = Thing
        fields = [
            "id",
            "name",
            "number",
            "status",
            "date_updated",
        ]


class GrandChildSerializer(VersionedSerializer, serializers.ModelSerializer):
    transforms = [
        transforms.PersonAddBirthday,
    ]

    class Meta:
        model = Person
        fields = [
            "name",
            "birthday",
        ]


class ChildSerializer(VersionedSerializer, serializers.ModelSerializer):
    children = GrandChildSerializer(many=True)
    transforms = [
        transforms.PersonAddBirthday,
    ]

    class Meta:
        model = Person
        fields = [
            "name",
            "birthday",
            "children",
        ]


class ParentSerializer(VersionedSerializer, serializers.ModelSerializer):
    transforms = [
        transforms.PersonAddBirthday,
    ]

    class Meta:
        model = Person
        fields = [
            "name",
            "birthday",
        ]


class PersonSerializer(VersionedSerializer, serializers.ModelSerializer):
    father = ParentSerializer()
    mother = ParentSerializer()
    children = ChildSerializer(many=True)
    transforms = [
        transforms.PersonAddBirthday,
    ]

    class Meta:
        model = Person
        fields = [
            "name",
            "birthday",
            "father",
            "mother",
            "children",
        ]

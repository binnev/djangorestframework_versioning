from rest_framework import serializers
from tests import transforms
from drf_versioning.transform.serializers import VersioningSerializer, import_transforms
from tests.models import Thing, Person


class ThingSerializer(VersioningSerializer, serializers.ModelSerializer):
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


class GrandChildSerializer(VersioningSerializer, serializers.ModelSerializer):
    transforms = [
        transforms.PersonAddBirthday,
    ]

    class Meta:
        model = Person
        fields = [
            "name",
            "birthday",
        ]


class ChildSerializer(VersioningSerializer, serializers.ModelSerializer):
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


class ParentSerializer(VersioningSerializer, serializers.ModelSerializer):
    transforms = [
        transforms.PersonAddBirthday,
    ]

    class Meta:
        model = Person
        fields = [
            "name",
            "birthday",
        ]


class PersonSerializer(VersioningSerializer, serializers.ModelSerializer):
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

# Versioning models / serializers

At some point we will need to make changes to our models in order to add new features. But we also want to keep supporting older API versions.

drf_versioning acts as a "versioning layer" in this regard.

## Adding a new field

Let's add a new `age` property to the Dog model.

```python
from django.db import models
from datetime import date

from django.utils import timezone


class Dog(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField(default=date.today)

    def __str__(self):
        return self.name.title()

    @property
    def age(self):
        return (timezone.now().date() - self.birthday).days // 365
```

And add the `age` field to the `DogSerializer` in `doggies/serializers.py`:

```python
class DogSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField()

    class Meta:
        model = Dog
        fields = (
            "id",
            "name",
            "birthday",
            "age",
        )
```

But we don't want to break old API versions with this unexpected new field. So we create a new Version and only serialize this field if the request.version is greater.

in `versions.py`:

```python
VERSION_2_1_0 = Version(
    "2.1.0",
    notes=["Added Dog.age property"],
)
```

Now create a new file `doggies/transforms.py`, with the following content:

```python
from drf_versioning.transforms import Transform

from versioning import versions


class AddAge(Transform):
    version = versions.VERSION_2_1_0
    description = "Added Dog.age which is auto-calculated based on the Dog's birthday."

    def to_representation(self, data: dict, request, instance):
        """
        Here we downgrade the serializer's output data to make it match older API versions.
        In this case that means removing the new 'age' field.
        """
        data.pop("age", None)
        return data

    def to_internal_value(self, data: dict, request):
        """
        Here we upgrade the request.data to make it match the latest API version.
        In this case the 'age' field is read-only, so no action is required.
        """
        pass
```

And update the `DogSerializer` in `doggies/serializers.py`:

```python
from drf_versioning.serializers import VersionedSerializer
from rest_framework import serializers

from doggies.models import Dog
from . import transforms


class DogSerializer(VersionedSerializer, serializers.ModelSerializer):
    age = serializers.IntegerField()

    transforms = (
        transforms.AddAge,
    )

    class Meta:
        model = Dog
        fields = (
            "id",
            "name",
            "birthday",
            "age",
        )
```

Here we have done:

- DogSerializer now inherits from VersionedSerializer
- We have declared a tuple of Transform objects that apply to this serializer
- The serializer code reflects the latest behaviour
- The Transforms downgrade the output for older request versions

In Postman: `GET /doggies/1/` with version = 2.0.0:

```json
{
  "id": 1,
  "name": "Biko",
  "birthday": "2014-05-06"
}
```

In Postman: `GET /doggies/1/` with version = 2.1.0:

```json
{
  "id": 1,
  "name": "Biko",
  "birthday": "2014-05-06",
  "age": 8
}
```

Because adding a new field is bound to a relatively common operation, DRF Versioning provides a special AddField class. Instead of our Transform subclass above, we could also have done this:

```python
from drf_versioning.transforms import AddField

from versioning import versions


class AddAge(AddField):
    version = versions.VERSION_2_1_0
    field_name = "age"
    description = "Added Dog.age which is auto-calculated based on the Dog's birthday."
```

and it would have had the same effect.

The Transform object adds its `description` field to the Version instance's `models` changelog:

```json
    {
  "version": "2.1.0",
  "notes": [],
  "models": [
    "Added Dog.age which is auto-calculated based on the Dog's birthday."
  ],
  "views": {
    "endpoints_introduced": [],
    "endpoints_removed": [],
    "actions_introduced": [],
    "actions_removed": []
  }
},
```

## Mutating fields

Let's say we want to update the Dog model to provide a `dog_years` property:

```python
class Dog(models.Model):
    ...

    @property
    def dog_years(self):
        return self.age * 7
```

and we want to group this together with the `age` property like this:

```json
{
  "age": {
    "human_years": 8,
    "dog_years": 56
  }
}
```

First let's update the serializers in `doggies/serializers.py`:

```python
from drf_versioning.serializers import VersionedSerializer
from rest_framework import serializers

from doggies.models import Dog
from . import transforms


class DogAgeSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {"human_years": instance.age, "dog_years": instance.dog_years}


class DogSerializer(VersionedSerializer, serializers.ModelSerializer):
    age = DogAgeSerializer(source="*")

    transforms = (
        transforms.AddAge,
    )

    class Meta:
        model = Dog
        fields = (
            "id",
            "name",
            "birthday",
            "age",
        )
```

Our serializer now produces the desired output:

```json
{
  "id": 1,
  "name": "Biko",
  "birthday": "2014-05-06",
  "age": {
    "human_years": 8,
    "dog_years": 56
  }
}
```

But we need a transform to downgrade this data for older API versions. In `doggies/transforms.py`, we add:

```python
class GroupAgeAndDogYears(Transform):
    version = versions.VERSION_3_0_0
    description = (
        "Added Dog.dog_years and grouped Dog.age and Dog.dog_years into one 'age' property"
    )

    def to_representation(self, data: dict, request, instance):
        """
        Here we downgrade the serializer's output data to make it match older API versions.
        In this case that means returning the Dog.age value instead of the whole
        {"human_years": 1, "dog_years": 7} dict.
        """
        data["age"] = data["age"]["human_years"]
        return data

    def to_internal_value(self, data: dict, request):
        """
        Here we upgrade the request.data to make it match the latest API version.
        In this case the 'age' field is read-only, so no action is required.
        """
        pass
```

We add this transform to the DogSerializer:

```python
class DogSerializer(VersionedSerializer, serializers.ModelSerializer):
    age = DogAgeSerializer(source="*")

    transforms = (
        transforms.AddAge,
        transforms.GroupAgeAndDogYears,
    )

    class Meta:
        model = Dog
        fields = (
            "id",
            "name",
            "birthday",
            "age",
        )
```

Let's test the endpoint's behaviour.

In Postman: `GET /doggies/1/` with version = 2.1.0:

```json
{
  "id": 1,
  "name": "Biko",
  "birthday": "2014-05-06",
  "age": 8
}
```

In Postman: `GET /doggies/1/` with version = 3.0.0:

```json
{
  "id": 1,
  "name": "Biko",
  "birthday": "2014-05-06",
  "age": {
    "human_years": 8,
    "dog_years": 56
  }
}
```

## Removing a field

Let's say we've decided to remove the age field altogether, and let the API consumer work it out for themselves based on the birthday field.

In `doggies/transforms.py`:

```python
class RemoveAge(Transform):
    version = versions.VERSION_4_0_0
    description = "Removed Dog.age field"

    def to_representation(self, data: dict, request, instance):
        """
        Here we downgrade the serializer's output data to make it match older API versions.
        We have removed the field, but older versions are still expecting it. So we add it to the
        serializer output for older versions here.
        """
        data["age"] = {
            "human_years": instance.age,
            "dog_years": instance.dog_years,
        }
        return data
```

In `doggies/serializers.py`:

```python
from drf_versioning.serializers import VersionedSerializer
from rest_framework import serializers

from doggies.models import Dog
from . import transforms


class DogSerializer(VersionedSerializer, serializers.ModelSerializer):
    transforms = (
        transforms.AddAge,
        transforms.GroupAgeAndDogYears,
        transforms.RemoveAge,
    )

    class Meta:
        model = Dog
        fields = (
            "id",
            "name",
            "birthday",
            # "age",  # <---- remove this field 
        )
```

The resulting behaviour of the API is:

In Postman: `GET /doggies/1/` with version = 3.0.0:

```json
{
  "id": 1,
  "name": "Biko",
  "birthday": "2014-05-06",
  "age": {
    "human_years": 8,
    "dog_years": 56
  }
}
```

In Postman: `GET /doggies/1/` with version = 4.0.0:

```json
{
  "id": 1,
  "name": "Biko",
  "birthday": "2014-05-06"
}
```

In this example, we still have access to the `Dog.age` and `Dog.dog_years` properties, so we can continue serializing real values for older request versions.

But let's say the property has been removed, and we completely lose access to the source data. We can no longer serialize the dog's age for older versions. In this case we can instead serialize a "null value" that satisfies the type and structure that the older version is expecting. For Dog.age, we could use `-1`, for example.

DRF Versioning provides another built in Transform subclass for this case: `RemoveField`. We can recreate the behaviour of our `RemoveAge` transform like this:

```python
class RemoveAge(RemoveField):
    version = versions.VERSION_4_0_0
    field_name = "age"
    description = "Removed Dog.age field"
    null_value = {"human_years": -1, "dog_years": -1}
```

Now is a good time to check that our Transforms correctly cascade their changes through all API versions.

In Postman: `GET /doggies/1/` with version = 1.0.0:

```json
{
  "detail": "Not found."
}
```

In Postman: `GET /doggies/1/` with version = 2.0.0:

```json
{
  "id": 1,
  "name": "Biko",
  "birthday": "2014-05-06"
}
```

In Postman: `GET /doggies/1/` with version = 2.1.0:

```json
{
  "id": 1,
  "name": "Biko",
  "birthday": "2014-05-06",
  "age": -1
}
```

In Postman: `GET /doggies/1/` with version = 3.0.0:

```json
{
  "id": 1,
  "name": "Biko",
  "birthday": "2014-05-06",
  "age": {
    "human_years": -1,
    "dog_years": -1
  }
}
```

In Postman: `GET /doggies/1/` with version = 4.0.0:

```json
{
  "id": 1,
  "name": "Biko",
  "birthday": "2014-05-06"
}
```


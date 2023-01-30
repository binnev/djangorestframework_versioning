# Django Rest Framework Versioning

## Project description 
This project aims to make it easy to support many different API versions in a Django REST Framework (DRF) project.

DRF [supports several versioning schemes](https://www.django-rest-framework.org/api-guide/versioning/) but (perhaps wisely) completely sidesteps the issue of how to deal with the different versions in your code. To quote the docs: "How you vary the API behavior is up to you". 

Django Rest Framework Versioning aims to provide some out-of-the box tools to handle versioning in the code. It is inspired by Stripe's API version "compatibility layer", as described in blog posts by [Brandur Leach](https://stripe.com/blog/api-versioning) and [Amber Feng](https://amberonrails.com/move-fast-dont-break-your-api). I used [Ryan Kaneshiro's](https://rescale.com/blog/api-versioning-with-the-django-rest-framework/) excellent Django sketch as a starting point. 

## Installation quick start

This section is intended for those who want to install DRF Versioning into an existing Django project.

**1. Create a versioning module: `./manage.py startapp versioning` or `mkdir versioning`**

Suggested structure:

```
└── versioning
    ├── __init__.py
    ├── version_list.py    # maintain the list of supported Versions here
    └── versions.py        # define your Version instances here
```

with `versions.py` containing:

```python
from drf_versioning.versions import Version

VERSION_1_0_0 = Version(
    "1.0.0",
    notes=["Initial version"],
)
```

and `version_list.py` containing:

```python
from . import versions

VERSIONS = [
    versions.VERSION_1_0_0,
]
```

**2. Update project settings**

In your project `settings.py` add:

```python
REST_FRAMEWORK = {
    ...,  # any other rest_framework settings
    "DEFAULT_VERSIONING_CLASS": "drf_versioning.middleware.AcceptHeaderVersioning",
}

DRF_VERSIONING_SETTINGS = {
    "VERSION_LIST": "versioning.version_list.VERSIONS",
    "DEFAULT_VERSION": "latest",
}
```

**3. (Optional) add versioning urls**

In your project `urls.py`:

```python
urlpatterns = [
    ...,  # your other urls
    path("version/", include("drf_versioning.urls")),
]
```

## Tutorial

### Django project setup

To showcase the features of this library, we will set up a basic Django Rest Framework project. If you want to install DRF Versioning into an existing project, feel free to skip to the **[DRF versioning installation](#drf-versioning-installation)** section. The [Django tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/) may also be helpful if you are doing this for the first time.

[Create a project directory and a virtual environment](https://realpython.com/python-virtual-environments-a-primer/), and inside it create `requirements.txt` with the following contents:

```
django
djangorestframework
djangorestframework-versioning
```

and run

```shell
pip install -r requirements.txt
```

```shell
django-admin startproject mysite
```

start doggies app

```shell
./manage.py startapp doggies
```

Add `"doggies"` to `settings.INSTALLED_APPS`

Create `doggies/models.py` with contents:

```python
from django.db import models
from datetime import date


class Dog(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField(default=date.today)

    def __str__(self):
        return self.name.title()
```

Create `doggies/serializers.py` with contents:

```python
from rest_framework import serializers

from doggies.models import Dog


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = (
            "id",
            "name",
            "birthday",
        )
```

Create `doggies/admin.py` with contents:

```python
from django.contrib import admin
from doggies.models import Dog


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    pass
```

Create `doggies/views.py` with contents:

```python
from rest_framework import viewsets, mixins

from doggies.models import Dog
from doggies.serializers import DogSerializer


class DoggieViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = DogSerializer
    queryset = Dog.objects.all()
```

Create `doggies/urls.py` with contents:

```python
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register("", views.DoggieViewSet, basename="doggies")

urlpatterns = router.urls
```

Register our doggies app urls in the global project urls `mysite/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("doggies/", include("doggies.urls")),
]
```

Your project directory should now look like this:

```
├── db.sqlite3
├── doggies
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └──  __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── mysite
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── requirements.txt
```

Create the new Dog table in the database:

```shell
./manage.py makemigrations
```

```shell
./manage.py migrate
```

create superuser

```shell
./manage.py createsuperuser
```

create some dogs in the admin site

Now if we navigate to `localhost:8000/doggies/` we should see the following output:

### DRF versioning installation

Create a versioning module. This can be a django app, but it doesn't have to be, since we don't require any models.

In the project root, do:

```shell
mkdir versioning
```

In `versioning/versions.py`:

```python
from drf_versioning.versions import Version

VERSION_1_0_0 = Version(
    "1.0.0",
    notes=["Initial version :)"],
)
```

in `versioning.version_list.py`:

```python
from . import versions

VERSIONS = [
    versions.VERSION_1_0_0,
]
```

Add the following line to your `mysite/settings.py`.

```python
# Here we are telling rest_framework to use drf_versioning's AcceptHeaderVersioning class. It
# inherits from rest_framework's AcceptHeaderVersioning class, and does almost the same thing,
# but it adds the ability to choose a default version if the version is not specified in the
# request.
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "drf_versioning.middleware.AcceptHeaderVersioning",
}

# Here we are telling drf_versioning where to find our list of supported versions (
# `VERSION_LIST`). We also specify a default version that we would like to attach to requests
# that do not specify a version. We have selected "latest" which will use the most recent Version
# it can find in the supported versions list. Other acceptable values are "earliest" or a version
# string e.g. "1.0.0"
DRF_VERSIONING_SETTINGS = {
    "VERSION_LIST": "versioning.version_list.VERSIONS",
    "DEFAULT_VERSION": "latest",
}
```

In `mysite/urls.py`, add `drf_versioning`s default urls. Your `urlpatterns` should now look like this:

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("doggies/", include("doggies.urls")),
    path("version/", include("drf_versioning.urls")),
]
```

If we navigate to `http://localhost:8000/version/`, we should see a list of available versions, with a description of the changes in each version. The `notes` that we passed to the Version instance are also serialized here.

```json
[
  {
    "version": "1.0.0",
    "notes": [
      "Initial version :)"
    ],
    "models": [],
    "views": {
      "endpoints_introduced": [],
      "endpoints_removed": [],
      "actions_introduced": [],
      "actions_removed": []
    }
  }
]
```

If we navigate to `http://localhost:8000/version/my_version/`, we should see which version was assigned to our request. Since we did not specify a versoin, we have been assigned the latest version -- 1.0.0 (which is also the only version).

```json
{
  "version": "1.0.0",
  "notes": [
    "Initial version :)"
  ],
  "models": [],
  "views": {
    "endpoints_introduced": [],
    "endpoints_removed": [],
    "actions_introduced": [],
    "actions_removed": []
  }
}
```

### The tutorial begins in earnest

Now that we have completed the setup, we can start the interesting part -- making changes to our API and supporting multiple versions!

#### Versioning views

##### View actions / methods

Let's say we want to add a new action to the Dogs viewset -- a view for individual dogs. Paste the following code into your `doggies/views.py`:

```python
from drf_versioning.decorators import versioned_view
from rest_framework import viewsets, mixins

from doggies.models import Dog
from doggies.serializers import DogSerializer
from versioning import versions


class DoggieViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = DogSerializer
    queryset = Dog.objects.all()

    @versioned_view(introduced_in=versions.VERSION_2_0_0)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
```

Here we have

- Added the RetrieveModelMixin to the viewset, which allows us to see the detail view at `/doggies/<dog-id>/`
- Overridden the `retrieve` method and applied the `versioned_view` decorator, specifying the version from which this view should become available.

Version 2.0.0 doesn't exist yet, so let's create it. Add this to your `versioning/versions.py`:

```python
VERSION_2_0_0 = Version(
    "2.0.0",
    notes=["Added doggie detail view"],
)
```

and add it to the list of supported versions in `versioning/version_list.py`:

```python
VERSIONS = [
    versions.VERSION_2_0_0,
    versions.VERSION_1_0_0,
]
```

Now if we ping the `/version/` endpoint, we should see the new Version. Note that in addition to the `notes` which we added to the Version instance by hand, the `versioned_view` decorator has also informed the Version instance about the new view, and it is described in the `views.actions_introduced` list.

```json
[
  {
    "version": "2.0.0",
    "notes": [
      "Added doggie detail view"
    ],
    "models": [],
    "views": {
      "endpoints_introduced": [],
      "endpoints_removed": [],
      "actions_introduced": [
        "DoggieViewSet.retrieve"
      ],
      "actions_removed": []
    }
  },
  {
    "version": "1.0.0",
    "notes": [
      "Initial version :)"
    ],
    "models": [],
    "views": {
      "endpoints_introduced": [],
      "endpoints_removed": [],
      "actions_introduced": [],
      "actions_removed": []
    }
  }
]
```

The `versioned_view` decorator hides the view for requests with version < 2.0.0. We can demonstrate this by requesting `GET /doggies/1/` with `Accept: application/json; version=1.0.0` in Postman. We get a 404 response with the following body:

```json
{
  "detail": "Not found."
}
```

If we repeat the same request with `Accept: application/json; version=2.0.0`, we are given access to the view:

```json
{
  "id": 1,
  "name": "Biko",
  "birthday": "2023-01-30"
}
```

The `versioned_view` decorator also accepts a `removed_in` argument. If this is present, the view will be hidden for all requests whose version is greater.

##### ViewSets

If we want to introduce / remove a whole endpoint, we can achieve this by inheriting from the `VersionedViewSet` class. In this case the `introduced_in` and `removed_in` versions are set as class attributes, which also apply to any of the ViewSet's methods:

```python
class CatViewSet(VersionedViewSet, viewsets.ReadOnlyModelViewSet):
    serializer_class = CatSerializer
    queryset = Cat.objects.all()
    introduced_in = versions.VERSION_1_0_0
    removed_in = versions.VERSION_5_0_0

    @versioned_view(introduced_in=versions.VERSION_3_0_0)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @versioned_view(removed_in=versions.VERSION_4_0_0)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
```

However, individual methods can be further limited by using the `versioned_view` decorator. The most restrictive combination of viewset / method versions will be chosen. In this example this results in:

- `CatViewSet` is available from 1.0.0 to 5.0.0
- `retrieve` is available from 3.0.0 to 5.0.0
- `list` is available from 1.0.0 to 4.0.0

The `VersionedViewSet` class also informs the relevant Version instances about its introduction and removal. It appears under `views.endpoints_introduced` / `views.endpoints_removed` in a serialized Version:

```json
{
  "version": "1.0.0",
  "notes": [
    "Initial version :)"
  ],
  "models": [],
  "views": {
    "endpoints_introduced": [
      "CatViewSet"
    ],
    "endpoints_removed": [],
    "actions_introduced": [],
    "actions_removed": []
  }
}
```

#### Versioning models / serializers

At some point we will need to make changes to our models in order to add new features. But we also want to keep supporting older API versions.

drf_versioning acts as a "versioning layer" in this regard (TODO: link Stripe article).

##### Adding a new field

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

##### Mutating fields

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

##### Removing a field

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


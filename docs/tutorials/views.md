# Versioning views

## View actions / methods

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

## ViewSets

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

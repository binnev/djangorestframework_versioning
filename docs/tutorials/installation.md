# Installation

Add `djangorestframework-versioning` to your requirements.txt.

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


Now that we have completed the setup, we can start the interesting part -- making changes to our API and supporting multiple versions!

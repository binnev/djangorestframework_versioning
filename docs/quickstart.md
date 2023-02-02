# Quick start

This section is intended as a quick reference for those who want to install DRF Versioning into an existing Django project. If you are starting from scratch, I recommend following the tutorial, which includes setting up a sample Django REST project.

## Create a versioning module

```
./manage.py startapp versioning
``` 

or

```
mkdir versioning
```

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

## Update project settings

In your project `settings.py` add:

```python
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "drf_versioning.middleware.AcceptHeaderVersioning",
}

DRF_VERSIONING_SETTINGS = {
    "VERSION_LIST": "versioning.version_list.VERSIONS",
    "DEFAULT_VERSION": "latest",
}
```

## (Optional) add versioning urls

In your project `urls.py`:

```python
urlpatterns = [
    ...,  # your other urls
    path("version/", include("drf_versioning.urls")),
]
```

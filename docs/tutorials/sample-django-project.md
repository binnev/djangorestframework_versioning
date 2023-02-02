# Sample Django project setup

To showcase the features of this library, we will set up a basic Django Rest Framework project. If you want to install DRF Versioning into an existing project, or if you just need a quick reference, feel free to skip this and use the Quick Start page instead. 

The [Django tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/) may also be helpful if you are doing this for the first time.

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

from django.db import models
from django.utils import timezone


class ThingStatus(models.TextChoices):
    OK = "OK"
    NOT_OK = "NOT_OK"


class Thing(models.Model):
    name = models.CharField(max_length=50)
    number = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=ThingStatus.choices, default=ThingStatus.OK)
    date_updated = models.DateTimeField(auto_created=True, default=timezone.now)


class Person(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField(default=timezone.now)
    father = models.ForeignKey(
        "tests.Person", related_name="fathered_children", on_delete=models.CASCADE, null=True
    )
    mother = models.ForeignKey(
        "tests.Person", related_name="mothered_children", on_delete=models.CASCADE, null=True
    )

    @property
    def children(self):
        return self.mothered_children.all() or self.fathered_children.all()

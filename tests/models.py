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

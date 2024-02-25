from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    notify = models.BooleanField(default=True)

    class Meta:
        db_table = "users"


class Event(models.Model):
    name = models.CharField(max_length=30, unique=False, null=False)
    meeting_time = models.DateTimeField()
    description = models.TextField()
    users = models.ManyToManyField(get_user_model(), related_name="events")

    class Meta:
        db_table = "events"
        ordering = ['-meeting_time']

    def __str__(self):
        return self.name

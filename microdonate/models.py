import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# TODO: Create your models here.

class Profile(models.Model):
    account = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # check User.name
    user_name = models.CharField(max_length=25, null=True)
    xp = models.IntegerField(default=0)


class Donate(models.Model):
    donate_name = models.CharField(max_length=200)

    donate_users = models.ManytoManyField(Profile)
    # ...

class Volunteer(models.Model):
    volunteer_name = models.CharField(max_length=200)

    volunteer_users = models.ManytoManyField(Profile)
    # ...



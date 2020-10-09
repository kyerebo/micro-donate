import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# TODO: Create your models here.

class Donate(models.Model):
    donate_name = models.CharField(max_length=200)

    donate_user = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
    )
    # ...

class Volunteer(models.Model):
    volunteer_name = models.CharField(max_length=200)

    volunteer_user = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
    )
    # ...


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # check User.name
    user_name = models.CharField(User.username, null=True, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)
    opportunities = models.OneToOneField(Donate.donate_name, null=True, on_delete=models.CASCADE)
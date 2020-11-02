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
    def __str__(self):
        return self.user_name

class Donate(models.Model):
    donate_name = models.CharField(max_length=200)

    donate_users = models.ManyToManyField(Profile)
    # ...

class Volunteer(models.Model):
    # name of specific volunteer
    volunteer_name = models.CharField(max_length=200)
    # name of overall organization
    organization_name = models.CharField(max_length=200, default='')
    # goal
    goal = models.IntegerField(default=100)
    # description
    description = models.CharField(max_length=1000, default='')


    volunteer_users = models.ManyToManyField(Profile)
    # ...

class Comments(models.Model):
    comments_title = models.CharField(max_length=200)
    comments_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

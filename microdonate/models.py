from datetime import datetime

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

class Comments(models.Model):
    # title
    comments_title = models.CharField(max_length=200, default='<No Title>')
    # body
    comments_text = models.CharField(max_length=200, default='<No Body>')
    # date
    pub_date = models.DateTimeField('date published', auto_now_add=True, blank=True)

class Donate(models.Model):
    donate_name = models.CharField(max_length=200)

    organization_name = models.CharField(max_length=200, default='')

    goal = models.IntegerField(default=100)

    description = models.CharField(max_length=1000, default='')

    donate_users = models.ManyToManyField(Profile)

    comments = models.ManyToManyField(Comments)

    donate_amount = models.IntegerField(default=0)
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
    # participants
    volunteer_users = models.ManyToManyField(Profile)
    # comments
    comments = models.ManyToManyField(Comments)
    # location in simple terms, "google search" location name, not formal address
    location = models.CharField(max_length=200, default = 'no such road')
    # date of event
    date = models.DateTimeField('Date of Event', default = timezone.now)
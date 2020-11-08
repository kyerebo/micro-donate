# Generated by Django 3.0.2 on 2020-11-08 19:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('microdonate', '0005_auto_20201101_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='donate',
            name='donate_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 8, 19, 57, 36, 818489, tzinfo=utc), verbose_name='Date of Event'),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='location',
            field=models.CharField(default='no such road', max_length=200),
        ),
    ]

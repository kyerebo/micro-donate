# Generated by Django 3.0.2 on 2020-10-19 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microdonate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volunteer_name', models.CharField(max_length=200)),
                ('volunteer_users', models.ManyToManyField(to='microdonate.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Donate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donate_name', models.CharField(max_length=200)),
                ('donate_users', models.ManyToManyField(to='microdonate.Profile')),
            ],
        ),
    ]

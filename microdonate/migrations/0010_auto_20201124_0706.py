# Generated by Django 3.0.5 on 2020-11-24 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microdonate', '0009_comments_volunteer_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='volunteer_users',
        ),
        migrations.CreateModel(
            name='DonateComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.ManyToManyField(to='microdonate.Comments')),
            ],
        ),
    ]

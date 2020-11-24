# Generated by Django 3.0.5 on 2020-11-24 10:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('microdonate', '0007_auto_20201108_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comments_text',
            field=models.CharField(default='<No Body>', max_length=200),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comments_title',
            field=models.CharField(default='<No Title>', max_length=200),
        ),
        migrations.AlterField(
            model_name='comments',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date of Event'),
        ),
    ]

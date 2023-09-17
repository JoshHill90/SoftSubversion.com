# Generated by Django 4.2.3 on 2023-09-17 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0014_projectevents'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='details',
            field=models.CharField(blank=True, max_length=3000, verbose_name='Project Details'),
        ),
        migrations.AddField(
            model_name='project',
            name='location',
            field=models.CharField(blank=True, max_length=255, verbose_name='Location type'),
        ),
        migrations.AddField(
            model_name='project',
            name='scope',
            field=models.CharField(blank=True, max_length=255, verbose_name='Project-Type/Scope'),
        ),
    ]

# Generated by Django 4.2.3 on 2023-10-05 03:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gallery', '0020_alter_projectevents_date_notes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='notes',
            new_name='Note',
        ),
    ]

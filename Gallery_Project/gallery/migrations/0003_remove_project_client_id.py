# Generated by Django 4.2.3 on 2023-07-29 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_print_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='client_id',
        ),
    ]
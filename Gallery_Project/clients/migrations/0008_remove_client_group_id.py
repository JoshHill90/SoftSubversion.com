# Generated by Django 4.2.3 on 2023-09-02 01:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_invite_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='group_id',
        ),
    ]

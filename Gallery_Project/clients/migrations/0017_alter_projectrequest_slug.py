# Generated by Django 4.2.3 on 2023-09-06 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0016_alter_projectrequest_slug_requestreply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectrequest',
            name='slug',
            field=models.SlugField(default='ff46', unique=True),
        ),
    ]

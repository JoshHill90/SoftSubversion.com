# Generated by Django 4.2.3 on 2023-10-05 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0047_alter_projectterms_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectterms',
            name='slug',
            field=models.SlugField(default='cbd0', unique=True),
        ),
    ]

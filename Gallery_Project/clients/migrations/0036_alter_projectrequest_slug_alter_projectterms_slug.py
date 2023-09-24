# Generated by Django 4.2.3 on 2023-09-17 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0035_alter_projectrequest_slug_alter_projectterms_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectrequest',
            name='slug',
            field=models.SlugField(default='8b42', unique=True),
        ),
        migrations.AlterField(
            model_name='projectterms',
            name='slug',
            field=models.SlugField(default='d3fb', unique=True),
        ),
    ]
# Generated by Django 4.2.3 on 2023-09-05 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0013_alter_projectrequest_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectrequest',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]

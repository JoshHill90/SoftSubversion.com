# Generated by Django 4.2.3 on 2023-09-05 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0012_remove_projectrequest_first_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectrequest',
            name='date',
            field=models.CharField(max_length=10),
        ),
    ]

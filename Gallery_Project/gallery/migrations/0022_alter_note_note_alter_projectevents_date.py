# Generated by Django 4.2.3 on 2023-10-06 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0021_rename_notes_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note',
            field=models.TextField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='projectevents',
            name='date',
            field=models.DateField(default='2023-10-06'),
        ),
    ]

# Generated by Django 4.2.3 on 2023-10-08 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0022_alter_note_note_alter_projectevents_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectevents',
            name='date',
            field=models.DateField(default='2023-10-08'),
        ),
    ]
# Generated by Django 4.2.3 on 2023-09-24 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0025_alter_billing_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='due_date',
            field=models.DateField(blank=True, default='2023-09-24'),
        ),
    ]
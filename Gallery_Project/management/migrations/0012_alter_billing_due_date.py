# Generated by Django 4.2.3 on 2023-09-05 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0011_alter_billing_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='due_date',
            field=models.DateField(blank=True, default='2023-09-05'),
        ),
    ]

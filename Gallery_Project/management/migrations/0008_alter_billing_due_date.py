# Generated by Django 4.2.3 on 2023-09-01 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0007_credit_remove_billing_client_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='due_date',
            field=models.DateField(blank=True, default='2023-08-31'),
        ),
    ]
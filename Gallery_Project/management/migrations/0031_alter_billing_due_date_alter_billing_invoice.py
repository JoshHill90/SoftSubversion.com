# Generated by Django 4.2.3 on 2023-10-09 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0030_alter_billing_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='due_date',
            field=models.DateField(blank=True, default='2023-10-09'),
        ),
        migrations.AlterField(
            model_name='billing',
            name='invoice',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
# Generated by Django 4.2.3 on 2023-09-14 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0020_alter_billing_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payments',
            name='invoice_id',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='billing',
            name='invoice',
            field=models.CharField(max_length=100),
        ),
    ]
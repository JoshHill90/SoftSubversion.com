# Generated by Django 4.2.3 on 2023-08-31 03:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_client_crew_id'),
        ('gallery', '0011_alter_image_display_alter_print_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='client_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clients.client'),
        ),
    ]
# Generated by Django 4.2.3 on 2023-08-11 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_remove_project_client_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='disaply',
            field=models.CharField(choices=[('home1', 'home1'), ('home4', 'home4'), ('home2', 'home2'), ('project', 'project'), ('home3', 'home3'), ('gallery2', 'gallery2'), ('gallery1', 'gallery1'), ('client', 'client'), ('none', 'none')], default='none', max_length=20),
        ),
    ]

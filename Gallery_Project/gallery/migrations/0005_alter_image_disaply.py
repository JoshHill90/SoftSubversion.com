# Generated by Django 4.2.3 on 2023-08-11 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_image_disaply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='disaply',
            field=models.CharField(choices=[('none', 'none'), ('home1', 'home1'), ('home2', 'home2'), ('home3', 'home3'), ('home4', 'home4'), ('gallery1', 'gallery1'), ('gallery2', 'gallery2'), ('project', 'project'), ('client', 'client')], default='none', max_length=20),
        ),
    ]
# Generated by Django 5.1.2 on 2024-11-05 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_alter_service_team'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='thumnail_image',
            new_name='thumbnail_image',
        ),
    ]

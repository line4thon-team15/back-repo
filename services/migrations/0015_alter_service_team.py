# Generated by Django 5.1.2 on 2024-11-09 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0014_alter_service_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='team',
            field=models.IntegerField(unique=True),
        ),
    ]

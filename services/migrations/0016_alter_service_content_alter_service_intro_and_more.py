# Generated by Django 5.1.2 on 2024-11-13 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0015_alter_service_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='intro',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_name',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]

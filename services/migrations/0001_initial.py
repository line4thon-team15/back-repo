# Generated by Django 5.1.2 on 2024-11-04 23:35

import django.db.models.deletion
import services.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('service_name', models.CharField(blank=True, max_length=30, null=True)),
                ('team', models.IntegerField()),
                ('content', models.CharField(blank=True, max_length=300, null=True)),
                ('site_url', models.CharField(blank=True, max_length=100, null=True)),
                ('thumnail_image', models.ImageField(blank=True, null=True, upload_to=services.models.image_upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'service',
            },
        ),
        migrations.CreateModel(
            name='PresentationImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to=services.models.image_upload_path)),
                ('service_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='services.service')),
            ],
            options={
                'db_table': 'presentation_image',
            },
        ),
    ]

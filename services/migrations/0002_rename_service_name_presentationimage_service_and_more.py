# Generated by Django 5.1.2 on 2024-11-04 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='presentationimage',
            old_name='service_name',
            new_name='service',
        ),
        migrations.AlterModelTable(
            name='presentationimage',
            table=None,
        ),
        migrations.AlterModelTable(
            name='service',
            table=None,
        ),
    ]
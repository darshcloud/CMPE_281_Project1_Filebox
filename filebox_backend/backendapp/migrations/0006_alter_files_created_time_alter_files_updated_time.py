# Generated by Django 4.1.1 on 2022-09-30 08:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0005_alter_files_created_time_alter_files_updated_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 30, 1, 9, 11, 425478)),
        ),
        migrations.AlterField(
            model_name='files',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 30, 1, 9, 11, 425478)),
        ),
    ]

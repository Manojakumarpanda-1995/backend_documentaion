# Generated by Django 3.2.3 on 2021-08-06 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_projectinfo_description'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='activitylogs',
            table='Project ActivityLogs',
        ),
        migrations.AlterModelTable(
            name='downloadfile',
            table='Download Files',
        ),
        migrations.AlterModelTable(
            name='fileupload',
            table='Files Uploaded',
        ),
        migrations.AlterModelTable(
            name='getprogress',
            table='GetProgress',
        ),
        migrations.AlterModelTable(
            name='projectinfo',
            table='ProjectInfo',
        ),
        migrations.AlterModelTable(
            name='projectusers',
            table='Project Users',
        ),
    ]
